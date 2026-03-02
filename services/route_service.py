from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import schemas.route_schemas as route_schemas
import models

# ROUTES
async def create_route(db: AsyncSession, payload: route_schemas.RouteCreate):
    new_route = models.Route(
        town=payload.town,
        road=payload.road,
        destination=payload.destination,
        departure=payload.departure,
        distance=payload.distance,
        comments=payload.comments,
    )

    db.add(new_route)
    await db.flush()

    for m in payload.matatus:
        db.add(
            models.Matatu(
                route_id=new_route.id,
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
                contacts=m.contacts,
            )
        )

    await db.commit()
    return new_route

# QUERIES
async def get_towns(db: AsyncSession):
    result = await db.execute(
        select(models.Route.town).distinct()
    )
    return result.scalars().all()


async def get_roads(db: AsyncSession, town: str):
    result = await db.execute(
        select(models.Route.road)
        .where(models.Route.town == town)
        .distinct()
    )
    return result.scalars().all()


async def get_destinations(db: AsyncSession, road_name: str):
    result = await db.execute(
        select(models.Route).where(models.Route.road == road_name)
    )
    return result.scalars().all()


async def get_routes_with_matatus(
    db: AsyncSession,
    road: str,
    destination: str,
):
    query = (
        select(models.Route)
        .options(selectinload(models.Route.matatus))
        .where(
            models.Route.road == road,
            models.Route.destination == destination,
        )
    )

    result = await db.execute(query)
    return result.scalars().unique().all()