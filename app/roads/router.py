from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Union

from app.core.database import get_db
from app.roads.schemas import NewRoad, RoadOut, BulkRoadsCreate
from app.roads.service import get_roads_action, create_road, bulk_create_roads

router = APIRouter(prefix="/roads", tags=["roads"])


@router.get("/", response_model=List[RoadOut])
async def fetch_roads(town: str, db: AsyncSession = Depends(get_db)) -> List[RoadOut]:
    return await get_roads_action(db, town)


@router.post("/new", status_code=201)
async def add_road(payload: NewRoad, db: AsyncSession = Depends(get_db)) -> Dict[str, Union[str, int]]:
    road = await create_road(db, payload.town, payload.road)
    return {
        "message": "Road created",
        "id": road.id,
    }


@router.post("/bulk", status_code=201)
async def add_bulk_roads(payload: BulkRoadsCreate, db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    roads = await bulk_create_roads(db, payload)
    return {"message": f"Added {len(roads)} roads to {payload.town}"}
