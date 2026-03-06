from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Union

from app.database import get_db
from app.destinations.service import create_destination, bulk_create_destinations, get_destinations_action
from app.destinations.schemas import DestinationOut, BulkDestinationsCreate
from app.common_schemas import NewDestination


router = APIRouter(prefix="/destinations", tags=["destinations"])


@router.post("/new", status_code=201)
async def add_destination(payload: NewDestination, db: AsyncSession = Depends(get_db)) -> Dict[str, Union[str, int]]:
    dest = await create_destination(db, payload.town, payload.road, payload)
    return {"message": "Destination created", "id": dest.id}


@router.post("/bulk", status_code=201)
async def add_bulk_destinations(payload: BulkDestinationsCreate, db: AsyncSession = Depends(get_db)) -> Dict[str, Union[str, int]]:
    dests = await bulk_create_destinations(db, payload)
    return {"message": "Bulk destinations processed", "count": len(dests)}


@router.get("/", response_model=List[DestinationOut])
async def fetch_destinations(road_name: str, db: AsyncSession = Depends(get_db)) -> List[DestinationOut]:
    return await get_destinations_action(db, road_name)
