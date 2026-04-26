from __future__ import annotations

import uuid
from typing import Optional

import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.db import get_conn
from app.models.schemas import (
    StageCreate, StageOut, StageVerify,
    StageHourCreate, StageHourOut,
    MessageOut,
)

router = APIRouter(prefix="/stages", tags=["Stages"])


@router.get("", response_model=list[StageOut], summary="List stages")
async def list_stages(
    stage_type: Optional[str] = Query(None),
    direction:  Optional[str] = Query(None),
    from_id:    Optional[uuid.UUID] = Query(
        None, description="Filter for stages reachable from this origin"),
    area:       Optional[str] = Query(None),
    is_active:  bool = Query(True),
    limit:      int = Query(50),
    offset:     int = Query(0),
    conn: asyncpg.Connection = Depends(get_conn),
):
    params: list = [is_active]
    filters = ["s.is_active = $1"]

    select_clause = "SELECT DISTINCT s.id, s.name, s.area, s.landmark, s.landmark_sw, s.stage_type, s.direction, s.latitude, s.longitude, s.image_url, s.is_active"
    from_clause = "FROM stages s"

    if from_id:
        from_clause += """ 
            JOIN route_paths rp_dest ON s.id = rp_dest.stage_id
            JOIN route_paths rp_origin ON rp_dest.route_id = rp_origin.route_id
        """
        params.append(str(from_id))
        filters.append(f"rp_origin.stage_id = ${len(params)}")
        filters.append(f"rp_dest.stop_order > rp_origin.stop_order")

        if direction:
            from_clause += " JOIN routes r ON rp_dest.route_id = r.id"
            params.append(direction)
            filters.append(f"r.direction = ${len(params)}::direction")
            direction = None

    if stage_type:
        params.append(stage_type)
        filters.append(f"s.stage_type = ${len(params)}::stagetype")

    if direction:
        params.append(direction)
        filters.append(f"s.direction = ${len(params)}::direction")

    if area:
        params.append(f"%{area}%")
        filters.append(f"s.area ILIKE ${len(params)}")

    where = " AND ".join(filters)

    params.append(limit)
    limit_idx = len(params)
    params.append(offset)
    offset_idx = len(params)

    query = f"""
        {select_clause}
        {from_clause}
        WHERE {where}
        ORDER BY s.area, s.name
        LIMIT ${limit_idx} OFFSET ${offset_idx}
    """

    rows = await conn.fetch(query, *params)
    return [dict(r) for r in rows]


@router.get("/{stage_id}", response_model=StageOut, summary="Get a stage")
async def get_stage(
    stage_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    row = await conn.fetchrow(
        """
        SELECT id, name, area, landmark, landmark_sw, image_url,
               stage_type, direction, latitude, longitude, is_active
        FROM   stages WHERE id = $1
        """,
        str(stage_id),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Stage not found")
    return dict(row)


@router.post("", response_model=StageOut, status_code=status.HTTP_201_CREATED,
             summary="Create a stage")
async def create_stage(
    body: StageCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    new_id = str(uuid.uuid4())
    await conn.execute(
        """
        INSERT INTO stages
            (id, name, area, landmark, landmark_sw,
             stage_type, direction, latitude, longitude, image_url, is_active)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10, $11)
        """,
        new_id, body.name, body.area, body.landmark, body.landmark_sw,
        body.stage_type.value, body.direction.value,
        body.latitude, body.longitude, body.image_url, body.is_active,
    )
    return {**body.model_dump(), "id": new_id}


@router.patch("/{stage_id}", response_model=StageOut, summary="Update a stage")
async def update_stage(
    stage_id: uuid.UUID,
    body: StageCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    result = await conn.execute(
        """
        UPDATE stages
        SET name=$1, area=$2, landmark=$3, landmark_sw=$4,
            stage_type=$5, direction=$6, latitude=$7,
            longitude=$8, image_url=$9, is_active=$10
        WHERE id=$10
        """,
        body.name, body.area, body.landmark, body.landmark_sw,
        body.stage_type.value, body.direction.value,
        body.latitude, body.longitude, body.image_url, body.is_active,
        str(stage_id),
    )
    if result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="Stage not found")
    return {**body.model_dump(), "id": stage_id}


@router.delete("/{stage_id}", response_model=MessageOut, summary="Deactivate a stage")
async def deactivate_stage(
    stage_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    result = await conn.execute(
        "UPDATE stages SET is_active = false WHERE id = $1",
        str(stage_id),
    )
    if result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="Stage not found")
    return {"message": f"Stage {stage_id} deactivated"}


@router.get("/{stage_id}/hours", response_model=list[StageHourOut],
            summary="Get operating hours for a stage")
async def list_stage_hours(
    stage_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    rows = await conn.fetch(
        """
        SELECT id, stage_id, day_of_week, open_from, open_until
        FROM   stage_hours WHERE stage_id = $1
        ORDER  BY day_of_week
        """,
        str(stage_id),
    )
    return [dict(r) for r in rows]


@router.post("/{stage_id}/hours", response_model=StageHourOut,
             status_code=status.HTTP_201_CREATED,
             summary="Add operating hours to a stage")
async def add_stage_hour(
    stage_id: uuid.UUID,
    body: StageHourCreate,
    conn: asyncpg.Connection = Depends(get_conn),
):
    new_id = str(uuid.uuid4())
    await conn.execute(
        """
        INSERT INTO stage_hours (id, stage_id, day_of_week, open_from, open_until)
        VALUES ($1, $2, $3, $4, $5)
        """,
        new_id, str(stage_id), body.day_of_week,
        body.open_from, body.open_until,
    )
    return {**body.model_dump(), "id": new_id, "stage_id": stage_id}

@router.post("/{stage_id}/verify", response_model=StageOut)
async def verify_stage(
    stage_id: uuid.UUID,
    conn: asyncpg.Connection = Depends(get_conn),
):
    row = await conn.fetchrow(
        "UPDATE stages SET is_active = true WHERE id = $1 RETURNING *",
        str(stage_id),
    )
    if not row:
        raise HTTPException(status_code=404, detail="SACCO not found")
    return dict(row)
