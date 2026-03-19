from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.stage import Stage
from app.schemas.stage import StageRead
from app.utils.geo import distance_meters

router = APIRouter(prefix="/api/v1/stages", tags=["stages"])


@router.get("", response_model=list[StageRead])
async def list_stages(
    area: str | None = Query(None),
    direction: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Stage).where(Stage.is_active == True)
    if area:
        query = query.where(Stage.area.ilike(f"%{area}%"))
    if direction:
        query = query.where(Stage.direction == direction)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/nearby", response_model=list[StageRead])
async def nearby_stages(
    lat: float = Query(...),
    lng: float = Query(...),
    radius_m: float = Query(500.0),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Stage).where(Stage.is_active == True))
    all_stages = result.scalars().all()
    return [
        s for s in all_stages
        if distance_meters(lat, lng, float(s.latitude), float(s.longitude)) <= radius_m
    ]


@router.get("/{stage_id}", response_model=StageRead)
async def get_stage(stage_id: str, db: AsyncSession = Depends(get_db)):
    from fastapi import HTTPException
    result = await db.get(Stage, stage_id)
    if not result:
        raise HTTPException(status_code=404, detail="Stage not found")
    return result
