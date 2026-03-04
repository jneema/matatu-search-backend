from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Union

from database import get_db
import services.route_service as service
from schemas.route_schemas import (
    RouteCreate,
    RouteDetailOut,
    TownOut,
    RoadOut,
    DestinationOut,
    NewDestination,
    NewRoad,
    BulkDestinationsCreate,
    BulkRoadsCreate,
)

router = APIRouter(prefix="/api", tags=["routes"])


#Routes
@router.post("/routes", status_code=201)
async def create_route(payload: RouteCreate, db: AsyncSession = Depends(get_db)) -> Dict[str, Union[str, int]]:
    dest = await service.create_route_with_matatus(db, payload)
    return {
        "message": "Route and Matatus created",
        "destination_id": dest.id,
    }


#Towns
@router.post("/towns/new", status_code=201)
async def add_town(name: str, db: AsyncSession = Depends(get_db)) -> Dict[str, Union[str, int]]:
    return await service.create_town_action(db, name)


@router.get("/towns", response_model=List[TownOut])
async def fetch_towns(db: AsyncSession = Depends(get_db)) -> List[TownOut]:
    return await service.get_towns_action(db)


#Roads
@router.post("/roads/new", status_code=201)
async def add_road(payload: NewRoad, db: AsyncSession = Depends(get_db)) -> Dict[str, Union[str, int]]:
    road = await service.create_road(db, payload.town, payload.road)
    return {
        "message": "Road created",
        "id": road.id,
    }


@router.get("/roads", response_model=List[RoadOut])
async def fetch_roads(town: str, db: AsyncSession = Depends(get_db)) -> List[RoadOut]:
    return await service.get_roads_action(db, town)


@router.post("/roads/bulk", status_code=201)
async def add_bulk_roads(payload: BulkRoadsCreate, db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    roads = await service.bulk_create_roads(db, payload)
    return {"message": f"Added {len(roads)} roads to {payload.town}"}


#Destinations
@router.post("/destinations/new", status_code=201)
async def add_destination(payload: NewDestination, db: AsyncSession = Depends(get_db)) -> Dict[str, Union[str, int]]:
    dest = await service.create_destination(db, payload.town, payload.road, payload)
    return {"message": "Destination created", "id": dest.id}


@router.get("/destinations", response_model=List[DestinationOut])
async def fetch_destinations(road_name: str, db: AsyncSession = Depends(get_db)) -> List[DestinationOut]:
    return await service.get_destinations_action(db, road_name)


@router.post("/destinations/bulk", status_code=201)
async def add_bulk_destinations(payload: BulkDestinationsCreate, db: AsyncSession = Depends(get_db)) -> Dict[str, Union[str, int]]:
    dests = await service.bulk_create_destinations(db, payload)
    return {"message": "Bulk destinations processed", "count": len(dests)}


#Results
@router.get("/results", response_model=List[RouteDetailOut])
async def get_results(road: str, destination: str, db: AsyncSession = Depends(get_db)) -> List[RouteDetailOut]:
    return await service.get_routes_with_matatus_action(db, road, destination)
