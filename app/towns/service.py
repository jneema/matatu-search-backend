from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, List, Dict, Union

import app.models as models
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


async def get_towns(db: AsyncSession) -> Sequence[models.Town]:
    result = await db.execute(select(models.Town))
    return result.scalars().all()


async def get_towns_action(db: AsyncSession) -> List[schemas.TownOut]:
    towns = await get_towns(db)
    return [schemas.TownOut(id=t.id, name=t.name) for t in towns]
