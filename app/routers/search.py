from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

import asyncpg
from fastapi import APIRouter, Depends, Query

from app.api.db import get_conn
from app.models.schemas import SearchResponse, RouteResult, TransferResult, StageMatch

router = APIRouter(prefix="/search", tags=["Search"])


async def _resolve_stage(
    conn: asyncpg.Connection, text: str
) -> Optional[asyncpg.Record]:
    """
    Fuzzy-match a stage by name or area using ILIKE.
    Priority: exact name > name starts-with > area match.
    """
    row = await conn.fetchrow(
        """
        SELECT id, name, area, stage_type, landmark
        FROM   stages
        WHERE  is_active = true
        AND (
            name ILIKE $1
            OR name ILIKE $2
            OR area ILIKE $2
            OR landmark ILIKE $2
        )
        ORDER BY
            CASE WHEN name ILIKE $1 THEN 0
                 WHEN name ILIKE $2 THEN 1
                 ELSE 2
            END
        LIMIT 1
        """,
        text,
        f"%{text}%",
    )
    return row


async def _fetch_routes_between(
    conn: asyncpg.Connection,
    origin_id: str,
    dest_id: str,
) -> list[asyncpg.Record]:
    return await conn.fetch(
        """
        SELECT
            r.id                        AS route_id,
            s.name                      AS sacco_name,
            orig.name                   AS origin,
            dest.name                   AS destination,
            r.via_description           AS via,
            r.is_express,
            orig.stage_type             AS origin_type,
            dest.stage_type             AS dest_type,
            r.departure_frequency_mins,
            r.avg_duration_mins,
            r.route_status,
            COALESCE(
                (SELECT amount_kes FROM fares
                 WHERE route_id = r.id AND fare_type = 'peak'
                 AND day_type = 0 LIMIT 1), NULL
            ) AS peak_fare_kes,
            COALESCE(
                (SELECT amount_kes FROM fares
                 WHERE route_id = r.id AND fare_type = 'off_peak'
                 AND day_type = 0 LIMIT 1), NULL
            ) AS off_peak_fare_kes,
            ARRAY(
                SELECT method::text FROM payment_methods
                WHERE route_id = r.id
            ) AS payment_methods
        FROM routes r
        JOIN saccos  s    ON s.id = r.sacco_id
        JOIN stages  orig ON orig.id = r.origin_stage_id
        JOIN stages  dest ON dest.id = r.dest_stage_id
        WHERE r.route_status != 'suspended'
        AND (
            -- direct origin→dest
            (r.origin_stage_id = $1 AND r.dest_stage_id = $2)
            OR
            -- route path passes through both in order
            EXISTS (
                SELECT 1 FROM route_paths rp1
                JOIN   route_paths rp2 ON rp2.route_id = rp1.route_id
                WHERE  rp1.route_id = r.id
                AND    rp1.stage_id = $1
                AND    rp2.stage_id = $2
                AND    rp1.stop_order < rp2.stop_order
            )
        )
        ORDER BY r.is_express DESC, r.avg_duration_mins ASC NULLS LAST
        """,
        str(origin_id),
        str(dest_id),
    )


def _record_to_route_result(row: asyncpg.Record) -> RouteResult:
    return RouteResult(
        route_id=row["route_id"],
        sacco_name=row["sacco_name"],
        origin=row["origin"],
        destination=row["destination"],
        via=row["via"],
        is_express=row["is_express"],
        is_panya=(
            row["origin_type"] == "informal"
            or row["dest_type"] == "informal"
        ),
        departure_frequency_mins=row["departure_frequency_mins"],
        avg_duration_mins=row["avg_duration_mins"],
        peak_fare_kes=row["peak_fare_kes"],
        off_peak_fare_kes=row["off_peak_fare_kes"],
        payment_methods=list(row["payment_methods"]),
        route_status=row["route_status"],
    )


async def _fetch_transfers(
    conn: asyncpg.Connection,
    origin_id: str,
    dest_id: str,
) -> list[asyncpg.Record]:
    """One-transfer journeys via the transfers table."""
    return await conn.fetch(
        """
        SELECT
            t.id,
            t.avg_wait_mins,
            t.total_fare_kes,
            ts.name  AS transfer_stage_name,
            r1.id    AS leg1_route_id,
            s1.name  AS leg1_sacco,
            o1.name  AS leg1_origin,
            d1.name  AS leg1_dest,
            r1.via_description  AS leg1_via,
            r1.is_express       AS leg1_express,
            o1.stage_type       AS leg1_orig_type,
            d1.stage_type       AS leg1_dest_type,
            r1.departure_frequency_mins AS leg1_freq,
            r1.avg_duration_mins        AS leg1_dur,
            r1.route_status             AS leg1_status,
            COALESCE((SELECT amount_kes FROM fares
                      WHERE route_id=r1.id AND fare_type='peak' AND day_type=0 LIMIT 1),NULL) AS leg1_peak,
            COALESCE((SELECT amount_kes FROM fares
                      WHERE route_id=r1.id AND fare_type='off_peak' AND day_type=0 LIMIT 1),NULL) AS leg1_offpeak,
            ARRAY(SELECT method::text FROM payment_methods WHERE route_id=r1.id) AS leg1_pay,
            r2.id    AS leg2_route_id,
            s2.name  AS leg2_sacco,
            o2.name  AS leg2_origin,
            d2.name  AS leg2_dest,
            r2.via_description  AS leg2_via,
            r2.is_express       AS leg2_express,
            o2.stage_type       AS leg2_orig_type,
            d2.stage_type       AS leg2_dest_type,
            r2.departure_frequency_mins AS leg2_freq,
            r2.avg_duration_mins        AS leg2_dur,
            r2.route_status             AS leg2_status,
            COALESCE((SELECT amount_kes FROM fares
                      WHERE route_id=r2.id AND fare_type='peak' AND day_type=0 LIMIT 1),NULL) AS leg2_peak,
            COALESCE((SELECT amount_kes FROM fares
                      WHERE route_id=r2.id AND fare_type='off_peak' AND day_type=0 LIMIT 1),NULL) AS leg2_offpeak,
            ARRAY(SELECT method::text FROM payment_methods WHERE route_id=r2.id) AS leg2_pay
        FROM transfers t
        JOIN routes r1 ON r1.id = t.leg1_route_id
        JOIN routes r2 ON r2.id = t.leg2_route_id
        JOIN stages ts ON ts.id = t.transfer_stage_id
        JOIN saccos s1 ON s1.id = r1.sacco_id
        JOIN saccos s2 ON s2.id = r2.sacco_id
        JOIN stages o1 ON o1.id = r1.origin_stage_id
        JOIN stages d1 ON d1.id = r1.dest_stage_id
        JOIN stages o2 ON o2.id = r2.origin_stage_id
        JOIN stages d2 ON d2.id = r2.dest_stage_id
        WHERE t.is_active = true
        AND r1.route_status != 'suspended'
        AND r2.route_status != 'suspended'
        AND (r1.origin_stage_id = $1 OR EXISTS (
            SELECT 1 FROM route_paths rp WHERE rp.route_id=r1.id AND rp.stage_id=$1
        ))
        AND (r2.dest_stage_id = $2 OR EXISTS (
            SELECT 1 FROM route_paths rp WHERE rp.route_id=r2.id AND rp.stage_id=$2
        ))
        ORDER BY COALESCE(t.avg_wait_mins, 99)
        LIMIT 5
        """,
        str(origin_id),
        str(dest_id),
    )


async def _log_search(
    conn: asyncpg.Connection,
    origin_text: str,
    dest_text: str,
    origin_id: Optional[str],
    dest_id: Optional[str],
    result_count: int,
    had_transfer: bool,
    session_id: Optional[str],
) -> None:
    await conn.execute(
        """
        INSERT INTO search_logs
            (id, origin_text, destination_text, resolved_origin_id,
             resolved_dest_id, result_count, had_transfer, session_id, queried_at)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
        """,
        str(uuid.uuid4()),
        origin_text, dest_text,
        origin_id, dest_id,
        result_count, had_transfer, session_id,
        datetime.now(tz=timezone.utc),
    )



@router.get("", response_model=SearchResponse, summary="Find matatu routes")
async def search_routes(
    origin:      str = Query(..., description="Origin stage name or area, e.g. 'pangani'"),
    destination: str = Query(..., description="Destination stage name or area, e.g. 'githurai 45'"),
    session_id:  Optional[str] = Query(None, max_length=64),
    conn: asyncpg.Connection = Depends(get_conn),
):
    origin_row = await _resolve_stage(conn, origin)
    dest_row   = await _resolve_stage(conn, destination)

    direct    = []
    transfers = []

    if origin_row and dest_row:
        raw_direct = await _fetch_routes_between(
            conn, str(origin_row["id"]), str(dest_row["id"])
        )
        direct = [_record_to_route_result(r) for r in raw_direct]

        raw_transfers = await _fetch_transfers(
            conn, str(origin_row["id"]), str(dest_row["id"])
        )
        transfers = [
            TransferResult(
                leg1=RouteResult(
                    route_id=r["leg1_route_id"], sacco_name=r["leg1_sacco"],
                    origin=r["leg1_origin"], destination=r["leg1_dest"],
                    via=r["leg1_via"], is_express=r["leg1_express"],
                    is_panya=r["leg1_orig_type"]=="informal" or r["leg1_dest_type"]=="informal",
                    departure_frequency_mins=r["leg1_freq"],
                    avg_duration_mins=r["leg1_dur"],
                    peak_fare_kes=r["leg1_peak"],
                    off_peak_fare_kes=r["leg1_offpeak"],
                    payment_methods=list(r["leg1_pay"]),
                    route_status=r["leg1_status"],
                ),
                leg2=RouteResult(
                    route_id=r["leg2_route_id"], sacco_name=r["leg2_sacco"],
                    origin=r["leg2_origin"], destination=r["leg2_dest"],
                    via=r["leg2_via"], is_express=r["leg2_express"],
                    is_panya=r["leg2_orig_type"]=="informal" or r["leg2_dest_type"]=="informal",
                    departure_frequency_mins=r["leg2_freq"],
                    avg_duration_mins=r["leg2_dur"],
                    peak_fare_kes=r["leg2_peak"],
                    off_peak_fare_kes=r["leg2_offpeak"],
                    payment_methods=list(r["leg2_pay"]),
                    route_status=r["leg2_status"],
                ),
                transfer_stage=r["transfer_stage_name"],
                avg_wait_mins=r["avg_wait_mins"],
                total_fare_kes=r["total_fare_kes"],
            )
            for r in raw_transfers
        ]

    await _log_search(
        conn, origin, destination,
        str(origin_row["id"]) if origin_row else None,
        str(dest_row["id"])   if dest_row   else None,
        len(direct) + len(transfers),
        bool(transfers),
        session_id,
    )

    return SearchResponse(
        direct_routes=direct,
        transfers=transfers,
        origin_resolved=StageMatch(**dict(origin_row)) if origin_row else None,
        destination_resolved=StageMatch(**dict(dest_row)) if dest_row else None,
    )