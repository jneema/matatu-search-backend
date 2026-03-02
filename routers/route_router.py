from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from services import route_service
from schemas.route_schemas import RouteCreate, RouteDetailOut, TownOut, RoadOut, DestinationOut

router = APIRouter(prefix="/api", tags=["routes"])

@router.post("/routes", status_code=201)
async def create_route_feedback(
    payload: RouteCreate,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str | int]:
    route = await route_service.create_route(db, payload)

    return {
        "message": "Feedback submitted successfully",
        "route_id": route.id,
    }

@router.get("/towns", response_model=List[TownOut])
async def get_towns(db: AsyncSession = Depends(get_db)):
    towns = await route_service.get_towns(db)
    return [{"name": t} for t in towns]

@router.get("/roads", response_model=List[RoadOut])
async def get_roads(town: str = "Nairobi", db: AsyncSession = Depends(get_db)):
    roads = await route_service.get_roads(db, town)
    return [{"name": r} for r in roads]

@router.get("/destinations", response_model=List[DestinationOut])
async def get_destinations(road_name: str, db: AsyncSession = Depends(get_db)):
    return await route_service.get_destinations(db, road_name)

@router.get("/results", response_model=List[RouteDetailOut])
async def get_final_routes(road: str, destination: str, db: AsyncSession = Depends(get_db)):
    return await route_service.get_routes_with_matatus(db, road, destination)