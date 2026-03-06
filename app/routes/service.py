from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Sequence, List

import app.models as models
from app.routes.schemas import RouteDetailOut, RouteCreate


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


async def get_routes_with_matatus_action(db: AsyncSession, road_name: str, dest_name: str) -> List[RouteDetailOut]:
    destinations = await get_routes_with_matatus(db, road_name, dest_name)
    return [RouteDetailOut.model_validate(d) for d in destinations]


async def create_route_with_matatus(db: AsyncSession, payload: RouteCreate) -> models.Destination:
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
