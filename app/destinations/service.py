from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from typing import Sequence, List

import app.models as models
from app.routes.service import create_route_with_matatus
from app.destinations.schemas import BulkDestinationsCreate, DestinationOut
from app.common_schemas import NewDestination

# Queries
async def get_destinations(db: AsyncSession, road_name: str) -> Sequence[models.Destination]:
    result = await db.execute(
        select(models.Destination).join(models.Destination.roads).where(
            models.Road.name.ilike(f"%{road_name}%"))
    )
    return result.scalars().all()


# Create
async def create_destination(db: AsyncSession, town_name: str, road_name: str, payload: NewDestination) -> models.Destination:
    res = await db.execute(select(models.Road).join(models.Town)
                           .where(models.Town.name == town_name, models.Road.name == road_name))
    road = res.scalar_one_or_none()
    if not road:
        raise HTTPException(404, "Road not found in specified town")
    dest = models.Destination(
        name=payload.destination,
        departure=payload.departure,
        distance=payload.distance
    )
    dest.roads.append(road)
    db.add(dest)
    await db.commit()
    await db.refresh(dest)
    return dest


# Bulk
async def bulk_create_destinations(db: AsyncSession, payload: BulkDestinationsCreate) -> List[models.Destination]:
    results: List[models.Destination] = []
    for route_data in payload.destinations:
        dest = await create_route_with_matatus(db, route_data)
        results.append(dest)
    return results


# Actions
async def get_destinations_action(
    db: AsyncSession, road_name: str
) -> List[DestinationOut]:
    dests = await get_destinations(db, road_name)
    return [
        DestinationOut(
            id=d.id,
            name=d.name,
            departure=d.departure,
            distance=d.distance,
            description=f"Via {road_name}"
        )
        for d in dests
    ]
