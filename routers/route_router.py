from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from database import get_db
from services.route_service import (create_route_with_matatus, create_road,create_destination, get_towns, get_roads, get_destinations, get_routes_with_matatus)
from schemas.route_schemas import (
    RouteCreate, RouteDetailOut, TownOut, RoadOut, 
    DestinationOut, NewDestination, NewRoad, MatatuOut
)

router = APIRouter(prefix="/api", tags=["routes"])

@router.post("/routes", status_code=201)
async def create_feedback(payload: RouteCreate, db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    dest = await create_route_with_matatus(db, payload)
    return {"message": "Feedback submitted", "destination_id": dest.id}

@router.post("/roads/new")
async def add_road(payload: NewRoad, db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    road = await create_road(db, payload.town, payload.road)
    return {"message": "Road created", "id": road.id}

@router.post("/destinations/new")
async def add_destination(payload: NewDestination, db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    dest = await create_destination(db, payload.town, payload.road, payload)
    return {"message": "Destination created", "id": dest.id}

@router.get("/towns", response_model=List[TownOut])
async def fetch_towns(db: AsyncSession = Depends(get_db)) -> List[TownOut]:
    towns = await get_towns(db)
    return [TownOut(id=t.id, name=t.name) for t in towns]

@router.get("/roads", response_model=List[RoadOut])
async def fetch_roads(town: str, db: AsyncSession = Depends(get_db)) -> List[RoadOut]:
    roads = await get_roads(db, town)
    return [RoadOut(id=r.id, name=r.name) for r in roads]

@router.get("/destinations", response_model=List[DestinationOut])
async def fetch_destinations(
    road_name: str,
    db: AsyncSession = Depends(get_db)
) -> List[DestinationOut]:
    dests = await get_destinations(db, road_name)
    return [
        DestinationOut(id=d.id, name=d.name, description=f"Via {road_name}")
        for d in dests
    ]

@router.get("/results", response_model=List[RouteDetailOut])
async def get_results(
    road: str,
    destination: str,
    db: AsyncSession = Depends(get_db),
) -> List[RouteDetailOut]:                      
    results = await get_routes_with_matatus(db, road, destination)
    return [
        RouteDetailOut(
            id=d.id,
            destination=d.name,
            departure=d.departure,
            distance=d.distance,
            matatus=[MatatuOut.model_validate(m) for m in d.matatus],
        )
        for d in results
    ]