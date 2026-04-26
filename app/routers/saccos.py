from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.db import get_conn
from app.models.schemas import (
    SaccoCreate, SaccoOut,
    SaccoAliasCreate, SaccoAliasOut,
    MessageOut,
)

router = APIRouter(prefix="/saccos", tags=["SACCOs"])


@router.get("", response_model=list[SaccoOut], summary="List SACCOs")
async def list_saccos(
    operating_status: Optional[str] = Query(None),
    vehicle_type:     Optional[str] = Query(None),
    is_verified:      Optional[bool] = Query(None),
    limit:  int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    conn: asyncpg.Connection = Depends(get_conn),
):
    filters = ["1=1"]
    params: list = []

    if operating_status:
        params.append(operating_status)
        filters.append(f"operating_status = ${len(params)}::operatingstatus")
    if vehicle_type:
        params.append(vehicle_type)
        filters.append(f"vehicle_type = ${len(params)}::vehicletype")
    if is_verified is not None:
        params.append(is_verified)
        filters.append(f"is_verified = ${len(params)}")

    where = " AND ".join(filters)
    params += [limit, offset]

    rows = await conn.fetch(
        *params,
    )
    return [dict(r) for r in rows]


@router.get("/{sacco_id}", response_model=SaccoOut, summary="Get a SACCO")
async def get_sacco(
    sacco_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    row = await conn.fetchrow(
        str(sacco_id),
    )
    if not row:
        raise HTTPException(status_code=404, detail="SACCO not found")
    return dict(row)


@router.post("", response_model=SaccoOut, status_code=status.HTTP_201_CREATED,
             summary="Register a new SACCO")
async def create_sacco(
    body: SaccoCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    new_id = str(uuid.uuid4())
    now = datetime.now(tz=timezone.utc)
    await conn.execute(
        new_id, body.name, body.vehicle_type.value, body.is_electric,
        body.terminus_area, body.operating_status.value,
        body.safety_rating, body.comfort_rating, body.is_verified, now,
    )
    return {
        **body.model_dump(),
        "id": new_id, "created_at": now, "last_confirmed_at": None,
    }


@router.patch("/{sacco_id}", response_model=SaccoOut, summary="Update a SACCO")
async def update_sacco(
    sacco_id: uuid.UUID,
    body: SaccoCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    result = await conn.execute(
        body.name, body.vehicle_type.value, body.is_electric,
        body.terminus_area, body.operating_status.value,
        body.safety_rating, body.comfort_rating, body.is_verified,
        str(sacco_id),
    )
    if result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="SACCO not found")

    row = await conn.fetchrow("SELECT * FROM saccos WHERE id=$1", str(sacco_id))

    if not row:
        raise HTTPException(
            status_code=404, detail="Record disappeared after update")

    return dict(row.items())


@router.delete("/{sacco_id}", response_model=MessageOut, summary="Suspend a SACCO")
async def suspend_sacco(
    sacco_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    result = await conn.execute(
        "UPDATE saccos SET operating_status='suspended' WHERE id=$1",
        str(sacco_id),
    )
    if result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="SACCO not found")
    return {"message": f"SACCO {sacco_id} suspended"}


@router.get("/{sacco_id}/aliases", response_model=list[SaccoAliasOut],
            summary="List aliases for a SACCO")
async def list_aliases(
    sacco_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    rows = await conn.fetch(
        "SELECT id, sacco_id, alias, alias_type FROM sacco_aliases WHERE sacco_id=$1",
        str(sacco_id),
    )
    return [dict(r) for r in rows]


@router.post("/{sacco_id}/aliases", response_model=SaccoAliasOut,
             status_code=status.HTTP_201_CREATED,
             summary="Add an alias to a SACCO")
async def add_alias(
    sacco_id: uuid.UUID,
    body: SaccoAliasCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    new_id = str(uuid.uuid4())
    await conn.execute(
        new_id, str(sacco_id), body.alias, body.alias_type.value,
    )
    return {**body.model_dump(), "id": new_id, "sacco_id": sacco_id}


@router.delete("/{sacco_id}/aliases/{alias_id}", response_model=MessageOut,
               summary="Remove a SACCO alias")
async def delete_alias(
    sacco_id: uuid.UUID,
    alias_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    result = await conn.execute(
        "DELETE FROM sacco_aliases WHERE id=$1 AND sacco_id=$2",
        str(alias_id), str(sacco_id),
    )
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Alias not found")
    return {"message": f"Alias {alias_id} removed"}
