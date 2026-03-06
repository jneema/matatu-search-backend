from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from typing import Sequence, List

import app.models as models
from app.roads.schemas import BulkRoadsCreate, RoadOut


async def get_roads(db: AsyncSession, town_name: str) -> Sequence[models.Road]:
    result = await db.execute(
        select(models.Road).join(models.Town).where(
            models.Town.name.ilike(f"%{town_name}%"))
    )
    return result.scalars().all()


async def create_road(db: AsyncSession, town_name: str, road_name: str) -> models.Road:
    res = await db.execute(select(models.Town).where(models.Town.name == town_name))
    town = res.scalar_one_or_none()
    if not town:
        raise HTTPException(404, f"Town '{town_name}' not found")
    road = models.Road(name=road_name, town_id=town.id)
    db.add(road)
    await db.commit()
    await db.refresh(road)
    return road


async def bulk_create_roads(db: AsyncSession, payload: BulkRoadsCreate) -> List[models.Road]:
    res = await db.execute(select(models.Town).where(models.Town.name == payload.town))
    town = res.scalar_one_or_none()
    if not town:
        raise HTTPException(404, f"Town '{payload.town}' not found")
    roads = [models.Road(name=r, town_id=town.id) for r in payload.roads]
    db.add_all(roads)
    await db.commit()
    return roads


async def get_roads_action(db: AsyncSession, town_name: str) -> List[RoadOut]:
    roads = await get_roads(db, town_name)
    return [RoadOut(id=r.id, name=r.name, town_id=r.town_id) for r in roads]
