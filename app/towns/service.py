from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, List, Dict, Union

import app.core.models as models
import app.towns.schemas as schemas


async def create_town(db: AsyncSession, name: str) -> models.Town:
    town = models.Town(name=name)
    db.add(town)
    await db.commit()
    await db.refresh(town)
    return town


async def create_town_action(db: AsyncSession, name: str) -> Dict[str, Union[str, int]]:
    town = await create_town(db, name)
    return {"message": "Town created", "id": town.id}


async def get_towns(db: AsyncSession, search: str = "") -> Sequence[models.Town]:
    query = select(models.Town)
    if search:
        query = query.where(models.Town.name.ilike(f"%{search}%"))
    result = await db.execute(query)
    return result.scalars().all()

async def get_towns_action(db: AsyncSession, search: str = "") -> List[schemas.TownOut]:
    towns = await get_towns(db, search)
    return [schemas.TownOut(id=t.id, name=t.name) for t in towns]
