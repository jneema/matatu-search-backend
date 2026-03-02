from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from typing import Sequence, List
import models
import schemas.route_schemas as schemas

# --- QUERIES ---
async def get_towns(db: AsyncSession) -> Sequence[models.Town]:
    result = await db.execute(select(models.Town))
    return result.scalars().all()

async def get_roads(db: AsyncSession, town_name: str) -> Sequence[models.Road]:
    result = await db.execute(
        select(models.Road).join(models.Town).where(models.Town.name == town_name)
    )
    return result.scalars().all()

async def get_destinations(db: AsyncSession, road_name: str) -> Sequence[models.Destination]:
    result = await db.execute(
        select(models.Destination).join(models.Road).where(models.Road.name == road_name)
    )
    return result.scalars().all()

async def get_routes_with_matatus(db: AsyncSession, road_name: str, dest_name: str) -> List[models.Destination]:
    query = (
        select(models.Destination)
        .options(selectinload(models.Destination.matatus))
        .join(models.Road)
        .where(models.Road.name == road_name, models.Destination.name == dest_name)
    )
    result = await db.execute(query)
    dest = result.scalars().first()
    return [dest] if dest else []

# --- CREATION LOGIC ---
async def create_road(db: AsyncSession, town_name: str, road_name: str) -> models.Road:
    town = (await db.execute(select(models.Town).where(models.Town.name == town_name))).scalar_one_or_none()
    if not town:
        raise HTTPException(404, f"Town '{town_name}' not found")
    
    new_road = models.Road(name=road_name, town_id=town.id)
    db.add(new_road)
    await db.commit()
    await db.refresh(new_road)
    return new_road

async def create_destination(db: AsyncSession, town_name: str, road_name: str, payload: schemas.NewDestination) -> models.Destination:
    # Ensure Road exists in that Town
    road = (await db.execute(
        select(models.Road).join(models.Town)
        .where(models.Town.name == town_name, models.Road.name == road_name)
    )).scalar_one_or_none()

    if not road:
        raise HTTPException(404, "Road not found in specified town")

    new_dest = models.Destination(
        road_id=road.id,
        name=payload.destination,
        departure=payload.departure,
        distance=payload.distance,
        comments=payload.comments
    )
    db.add(new_dest)
    await db.commit()
    await db.refresh(new_dest)
    return new_dest

async def create_route_with_matatus(db: AsyncSession, payload: schemas.RouteCreate) -> models.Destination:
    # 1. Get or Create Town
    town = (await db.execute(
        select(models.Town).where(models.Town.name == payload.town)
    )).scalar_one_or_none()
    
    if not town:
        town = models.Town(name=payload.town)
        db.add(town)
        await db.flush() # Get town.id

    # 2. Get or Create Road
    road = (await db.execute(
        select(models.Road).where(
            models.Road.name == payload.road, 
            models.Road.town_id == town.id
        )
    )).scalar_one_or_none()

    if not road:
        road = models.Road(name=payload.road, town_id=town.id)
        db.add(road)
        await db.flush() # Get road.id

    # 3. Create the Destination
    new_dest = models.Destination(
        road_id=road.id,
        name=payload.destination,
        departure=payload.departure,
        distance=payload.distance,
        comments=payload.comments
    )
    db.add(new_dest)
    await db.flush()

    # 4. Add the Matatus
    for m in payload.matatus:
        new_matatu = models.Matatu(
            destination_id=new_dest.id,
            sacco_name=m.saccoName,
            matatu_name=m.matatuName,
            matatu_number=m.matatuNumber,
            stage_destination=m.stageLocationDestination,
            stage_departure=m.stageLocationDeparture,
            payment_methods=m.payment,
            dropoffs=m.dropoffs,
            peak_fare=m.peakFare,
            off_peak_fare=m.offPeakFare,
            matatu_type=m.type,
            rating=m.rating,
            contacts=m.contacts
        )
        db.add(new_matatu)
    
    await db.commit()
    await db.refresh(new_dest)
    return new_dest