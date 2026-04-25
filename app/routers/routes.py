from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.db import get_conn
from app.models.schemas import (
    RouteCreate, RouteOut,
    RoutePathCreate, RoutePathOut,
    FareCreate, FareOut,
    PaymentMethodCreate, PaymentMethodOut,
    MessageOut,
)

router = APIRouter(prefix="/routes", tags=["Routes"])


@router.get("", response_model=list[RouteOut], summary="List routes")
async def list_routes(
    corridor_id:  Optional[uuid.UUID] = Query(None),
    sacco_id:     Optional[uuid.UUID] = Query(None),
    is_express:   Optional[bool]      = Query(None),
    route_status: Optional[str]       = Query(None),
    limit:  int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    conn: asyncpg.Connection = Depends(get_conn),
):
    filters = ["1=1"]
    params: list = []

    if corridor_id:
        params.append(str(corridor_id)); filters.append(f"corridor_id = ${len(params)}")
    if sacco_id:
        params.append(str(sacco_id));    filters.append(f"sacco_id = ${len(params)}")
    if is_express is not None:
        params.append(is_express);       filters.append(f"is_express = ${len(params)}")
    if route_status:
        params.append(route_status);     filters.append(f"route_status = ${len(params)}::routestatus")

    where = " AND ".join(filters)
    params += [limit, offset]

    rows = await conn.fetch(
        f"""
        SELECT id, sacco_id, corridor_id, origin_stage_id, dest_stage_id,
               via_description, via_description_sw, distance_km, is_express,
               route_status, departure_frequency_mins, avg_duration_mins,
               peak_duration_mins, fare_last_verified_at,
               last_confirmed_at, created_at
        FROM   routes
        WHERE  {where}
        ORDER  BY created_at DESC
        LIMIT  ${len(params)-1} OFFSET ${len(params)}
        """,
        *params,
    )
    return [dict(r) for r in rows]



@router.get("/{route_id}", response_model=RouteOut, summary="Get a route")
async def get_route(
    route_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    row = await conn.fetchrow(
        """
        SELECT id, sacco_id, corridor_id, origin_stage_id, dest_stage_id,
               via_description, via_description_sw, distance_km, is_express,
               route_status, departure_frequency_mins, avg_duration_mins,
               peak_duration_mins, fare_last_verified_at,
               last_confirmed_at, created_at
        FROM   routes WHERE id = $1
        """,
        str(route_id),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Route not found")
    return dict(row)



@router.post("", response_model=RouteOut, status_code=status.HTTP_201_CREATED,
             summary="Add a new route")
async def create_route(
    body: RouteCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    new_id = str(uuid.uuid4())
    now    = datetime.now(tz=timezone.utc)
    await conn.execute(
        """
        INSERT INTO routes
            (id, sacco_id, corridor_id, origin_stage_id, dest_stage_id,
             via_description, via_description_sw, distance_km, is_express,
             route_status, departure_frequency_mins, avg_duration_mins,
             peak_duration_mins, created_at)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
        """,
        new_id,
        str(body.sacco_id),
        str(body.corridor_id) if body.corridor_id else None,
        str(body.origin_stage_id), str(body.dest_stage_id),
        body.via_description, body.via_description_sw,
        body.distance_km, body.is_express,
        body.route_status.value,
        body.departure_frequency_mins, body.avg_duration_mins,
        body.peak_duration_mins, now,
    )
    return {
        **body.model_dump(),
        "id": new_id, "created_at": now,
        "fare_last_verified_at": None, "last_confirmed_at": None,
    }


@router.patch("/{route_id}", response_model=RouteOut, summary="Update a route")
async def update_route(
    route_id: uuid.UUID,
    body: RouteCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    result = await conn.execute(
        """
        UPDATE routes
        SET sacco_id=$1, corridor_id=$2, origin_stage_id=$3, dest_stage_id=$4,
            via_description=$5, via_description_sw=$6, distance_km=$7,
            is_express=$8, route_status=$9, departure_frequency_mins=$10,
            avg_duration_mins=$11, peak_duration_mins=$12
        WHERE id=$13
        """,
        str(body.sacco_id),
        str(body.corridor_id) if body.corridor_id else None,
        str(body.origin_stage_id), str(body.dest_stage_id),
        body.via_description, body.via_description_sw,
        body.distance_km, body.is_express,
        body.route_status.value,
        body.departure_frequency_mins, body.avg_duration_mins,
        body.peak_duration_mins, str(route_id),
    )
    if result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="Route not found")

    row = await conn.fetchrow("SELECT * FROM routes WHERE id=$1", str(route_id))
    
    if not row:
        raise HTTPException(status_code=404, detail="Record disappeared after update")

    return dict(row.items())



@router.delete("/{route_id}", response_model=MessageOut, summary="Suspend a route")
async def suspend_route(
    route_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    result = await conn.execute(
        "UPDATE routes SET route_status='suspended' WHERE id=$1",
        str(route_id),
    )
    if result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="Route not found")
    return {"message": f"Route {route_id} suspended"}



@router.get("/{route_id}/path", response_model=list[RoutePathOut],
            summary="Get ordered stop sequence for a route")
async def get_route_path(
    route_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    rows = await conn.fetch(
        """
        SELECT rp.id, rp.route_id, rp.stage_id, rp.stop_order,
               s.name AS stage_name, s.stage_type, s.area
        FROM   route_paths rp
        JOIN   stages s ON s.id = rp.stage_id
        WHERE  rp.route_id = $1
        ORDER  BY rp.stop_order
        """,
        str(route_id),
    )
    return [dict(r) for r in rows]


@router.post("/{route_id}/path", response_model=RoutePathOut,
             status_code=status.HTTP_201_CREATED,
             summary="Append a stop to a route's path")
async def add_route_path(
    route_id: uuid.UUID,
    body: RoutePathCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    new_id = str(uuid.uuid4())
    await conn.execute(
        """
        INSERT INTO route_paths (id, route_id, stage_id, stop_order)
        VALUES ($1, $2, $3, $4)
        """,
        new_id, str(route_id), str(body.stage_id), body.stop_order,
    )
    return {**body.model_dump(), "id": new_id, "route_id": route_id}



@router.get("/{route_id}/fares", response_model=list[FareOut],
            summary="Get fares for a route")
async def list_fares(
    route_id: uuid.UUID,
    fare_type: Optional[str] = Query(None, description="peak | off_peak | late_night | weekend | public_holiday"),
    conn: asyncpg.Connection = Depends(get_conn),
):
    params: list = [str(route_id)]
    extra = ""
    if fare_type:
        params.append(fare_type)
        extra = f"AND fare_type = ${len(params)}::faretype"

    rows = await conn.fetch(
        f"""
        SELECT id, route_id, fare_type, day_type, amount_kes, valid_from, valid_until
        FROM   fares
        WHERE  route_id = $1 {extra}
        ORDER  BY day_type, valid_from
        """,
        *params,
    )
    return [dict(r) for r in rows]


@router.post("/{route_id}/fares", response_model=FareOut,
             status_code=status.HTTP_201_CREATED,
             summary="Add a fare to a route")
async def add_fare(
    route_id: uuid.UUID,
    body: FareCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    new_id = str(uuid.uuid4())
    await conn.execute(
        """
        INSERT INTO fares (id, route_id, fare_type, day_type, amount_kes, valid_from, valid_until)
        VALUES ($1,$2,$3,$4,$5,$6,$7)
        """,
        new_id, str(route_id), body.fare_type.value,
        body.day_type, body.amount_kes, body.valid_from, body.valid_until,
    )
    return {**body.model_dump(), "id": new_id}


@router.delete("/{route_id}/fares/{fare_id}", response_model=MessageOut,
               summary="Remove a fare")
async def delete_fare(
    route_id: uuid.UUID,
    fare_id:  uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    result = await conn.execute(
        "DELETE FROM fares WHERE id=$1 AND route_id=$2",
        str(fare_id), str(route_id),
    )
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Fare not found")
    return {"message": f"Fare {fare_id} deleted"}



@router.get("/{route_id}/payment-methods", response_model=list[PaymentMethodOut],
            summary="Get accepted payment methods for a route")
async def list_payment_methods(
    route_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    rows = await conn.fetch(
        "SELECT id, route_id, method FROM payment_methods WHERE route_id=$1",
        str(route_id),
    )
    return [dict(r) for r in rows]


@router.post("/{route_id}/payment-methods", response_model=PaymentMethodOut,
             status_code=status.HTTP_201_CREATED,
             summary="Add a payment method to a route")
async def add_payment_method(
    route_id: uuid.UUID,
    body: PaymentMethodCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    new_id = str(uuid.uuid4())
    await conn.execute(
        "INSERT INTO payment_methods (id, route_id, method) VALUES ($1,$2,$3)",
        new_id, str(route_id), body.method.value,
    )
    return {**body.model_dump(), "id": new_id}


@router.delete("/{route_id}/payment-methods/{pm_id}", response_model=MessageOut,
               summary="Remove a payment method from a route")
async def delete_payment_method(
    route_id: uuid.UUID,
    pm_id:    uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    result = await conn.execute(
        "DELETE FROM payment_methods WHERE id=$1 AND route_id=$2",
        str(pm_id), str(route_id),
    )
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Payment method not found")
    return {"message": f"Payment method {pm_id} removed"}