from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from typing import Sequence, List, Dict, Union

import models
import schemas.route_schemas as schemas

# Queries


async def get_towns(db: AsyncSession) -> Sequence[models.Town]:
    result = await db.execute(select(models.Town))
    return result.scalars().all()


async def get_roads(db: AsyncSession, town_name: str) -> Sequence[models.Road]:
    result = await db.execute(
        select(models.Road).join(models.Town).where(
            models.Town.name.ilike(f"%{town_name}%"))
    )
    return result.scalars().all()


async def get_destinations(db: AsyncSession, road_name: str) -> Sequence[models.Destination]:
    result = await db.execute(
        select(models.Destination).join(models.Destination.roads).where(
            models.Road.name.ilike(f"%{road_name}%"))
    )
    return result.scalars().all()


async def get_routes_with_matatus(db: AsyncSession, road_name: str, dest_name: str) -> Sequence[models.Destination]:
    query = (
        select(models.Destination)
        .options(selectinload(models.Destination.matatus))
        .join(models.Destination.roads)
        .where(
            models.Road.name.ilike(f"%{road_name}%"),
            models.Destination.name.ilike(f"%{dest_name}%")
        )
    )
    result = await db.execute(query)
    return result.scalars().all()

# Create


async def create_town(db: AsyncSession, name: str) -> models.Town:
    town = models.Town(name=name)
    db.add(town)
    await db.commit()
    await db.refresh(town)
    return town


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


async def create_destination(db: AsyncSession, town_name: str, road_name: str, payload: schemas.NewDestination) -> models.Destination:
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


async def create_route_with_matatus(db: AsyncSession, payload: schemas.RouteCreate) -> models.Destination:
    # Town
    res = await db.execute(select(models.Town).where(models.Town.name == payload.town))
    town = res.scalar_one_or_none()
    if not town:
        town = models.Town(name=payload.town)
        db.add(town)
        await db.flush()

    # Road
    res = await db.execute(select(models.Road).where(models.Road.name == payload.road, models.Road.town_id == town.id))
    road = res.scalar_one_or_none()
    if not road:
        road = models.Road(name=payload.road, town_id=town.id)
        db.add(road)
        await db.flush()

    # Destination
    res = await db.execute(select(models.Destination).where(models.Destination.name == payload.destination))
    dest = res.scalar_one_or_none()
    if not dest:
        dest = models.Destination(
            name=payload.destination,
            departure=payload.departure,
            distance=payload.distance
        )
        db.add(dest)
        await db.flush()

    if road not in dest.roads:
        dest.roads.append(road)

    # Matatus
    for m in payload.matatus:
        db.add(models.Matatu(
            destination_id=dest.id,
            sacco_name=m.saccoName,
            matatu_name=m.matatuName,
            cbd_stage=m.cbdStage,
            estate_stage=m.estateStage,
            peak_fare_inbound=m.peakFareInbound,
            peak_fare_outbound=m.peakFareOutbound,
            off_peak_fare=m.offPeakFare,
            is_express=m.isExpress,
            is_electric=m.isElectric,
            payment_methods=m.payment,
            rating=m.rating if m.rating is not None else 0.0,
            contacts=m.contacts,
            notes=m.notes
        ))

    await db.commit()
    await db.refresh(dest)
    return dest

# Bulk


async def bulk_create_roads(db: AsyncSession, payload: schemas.BulkRoadsCreate) -> List[models.Road]:
    res = await db.execute(select(models.Town).where(models.Town.name == payload.town))
    town = res.scalar_one_or_none()
    if not town:
        raise HTTPException(404, f"Town '{payload.town}' not found")
    roads = [models.Road(name=r, town_id=town.id) for r in payload.roads]
    db.add_all(roads)
    await db.commit()
    return roads


async def bulk_create_destinations(db: AsyncSession, payload: schemas.BulkDestinationsCreate) -> List[models.Destination]:
    results: List[models.Destination] = []
    for route_data in payload.destinations:
        dest = await create_route_with_matatus(db, route_data)
        results.append(dest)
    return results

# Actions


async def create_town_action(db: AsyncSession, name: str) -> Dict[str, Union[str, int]]:
    town = await create_town(db, name)
    return {"message": "Town created", "id": town.id}


async def get_towns_action(db: AsyncSession) -> List[schemas.TownOut]:
    towns = await get_towns(db)
    return [schemas.TownOut(id=t.id, name=t.name) for t in towns]


async def get_roads_action(db: AsyncSession, town_name: str) -> List[schemas.RoadOut]:
    roads = await get_roads(db, town_name)
    return [schemas.RoadOut(id=r.id, name=r.name, town_id=r.town_id) for r in roads]


async def get_destinations_action(
    db: AsyncSession, road_name: str
) -> List[schemas.DestinationOut]:
    dests = await get_destinations(db, road_name)
    return [
        schemas.DestinationOut(
            id=d.id,
            name=d.name,
            departure=d.departure,
            distance=d.distance,
            description=f"Via {road_name}"
        )
        for d in dests
    ]

async def get_routes_with_matatus_action(db: AsyncSession, road_name: str, dest_name: str) -> List[schemas.RouteDetailOut]:
    destinations = await get_routes_with_matatus(db, road_name, dest_name)
    return [schemas.RouteDetailOut.model_validate(d) for d in destinations]
