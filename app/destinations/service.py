from typing import Sequence, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

import app.core.models as models
from app.core.common_schemas import NewDestination
from app.destinations.schemas import BulkDestinationsCreate
from app.routes.service import create_route_with_matatus

# Queries
async def get_destinations(
    db: AsyncSession,
    road_name: str,
    search: Optional[str] = None
) -> Sequence[models.Destination]:

    road_name = road_name.strip()

    query = (
        select(models.Destination)
        .join(models.Destination.roads)
        .where(models.Road.name.ilike(f"%{road_name}%"))
    )

    if search:
        search = search.strip()
        query = query.where(models.Destination.name.ilike(f"%{search}%"))

    result = await db.execute(query)
    return result.scalars().all()


# Create single destination
async def create_destination(
    db: AsyncSession,
    town_name: str,
    road_name: str,
    payload: NewDestination
) -> models.Destination:
    # Check if destination already exists
    existing = await db.execute(
        select(models.Destination)
        .join(models.Destination.roads)
        .where(
            models.Destination.name.ilike(payload.destination),
            models.Road.name.ilike(road_name)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail="Destination already exists")

    # Get road inside the town
    res = await db.execute(
        select(models.Road)
        .join(models.Town)
        .where(
            models.Town.name.ilike(town_name),
            models.Road.name.ilike(road_name)
        )
    )
    road = res.scalar_one_or_none()
    if not road:
        raise HTTPException(
            status_code=404, detail="Road not found in specified town")

    # Create destination
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


# Bulk create destinations
async def bulk_create_destinations(
    db: AsyncSession,
    payload: BulkDestinationsCreate
) -> List[models.Destination]:
    results: List[models.Destination] = []
    for route_data in payload.destinations:
        dest = await create_route_with_matatus(db, route_data)
        results.append(dest)
    return results
