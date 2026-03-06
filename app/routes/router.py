from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Union

from app.database import get_db
from app.routes.schemas import RouteDetailOut, RouteCreate
from app.routes.service import get_routes_with_matatus_action, create_route_with_matatus

router = APIRouter(prefix="", tags=["routes"])

# Routes
@router.post("/routes", status_code=201)
async def create_route(payload: RouteCreate, db: AsyncSession = Depends(get_db)) -> Dict[str, Union[str, int]]:
    dest = await create_route_with_matatus(db, payload)
    return {
        "message": "Route and Matatus created",
        "destination_id": dest.id,
    }

# Results
@router.get("/results", response_model=List[RouteDetailOut])
async def get_results(road: str, destination: str, db: AsyncSession = Depends(get_db)) -> List[RouteDetailOut]:
    return await get_routes_with_matatus_action(db, road, destination)
