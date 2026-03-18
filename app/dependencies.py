from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.redis import get_redis


async def get_db_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db`