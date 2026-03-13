from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Union

from app.core.database import get_db
from app.destinations.service import get_destinations, create_destination, bulk_create_destinations
from app.destinations.schemas import DestinationOut, BulkDestinationsCreate
from app.core.common_schemas import NewDestination

router = APIRouter(prefix="/destinations", tags=["destinations"])


@router.get("/", response_model=List[DestinationOut])
async def fetch_destinations(
    road_name: str,
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> List[DestinationOut]:
    dest_models = await get_destinations(db, road_name, search)

    # Map SQLAlchemy models to Pydantic schema
    return [
        DestinationOut(
            id=d.id,
            name=d.name,
            departure=d.departure,
            distance=d.distance,
            description=f"Via {road_name}",
        )
        for d in dest_models
    ]


@router.post("/new", status_code=201)
async def add_destination(
    payload: NewDestination,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Union[str, int]]:
    dest = await create_destination(db, payload.town, payload.road, payload)
    return {"message": "Destination created", "id": dest.id}


@router.post("/bulk", status_code=201)
async def add_bulk_destinations(
    payload: BulkDestinationsCreate,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Union[str, int]]:
    dests = await bulk_create_destinations(db, payload)
    return {"message": "Bulk destinations processed", "count": len(dests)}
