from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Union

from app.database import get_db
import app.towns.service as service
from app.towns.schemas import TownOut

router = APIRouter(prefix="/towns", tags=["towns"])


@router.get("/", response_model=List[TownOut])
async def fetch_towns(db: AsyncSession = Depends(get_db)) -> List[TownOut]:
    return await service.get_towns_action(db)


@router.post("/new", status_code=201)
async def add_town(name: str, db: AsyncSession = Depends(get_db)) -> Dict[str, Union[str, int]]:
    return await service.create_town_action(db, name)
