from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
from app.db.redis import get_redis
from app.schemas.common import HealthStatus

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthStatus)
async def liveness():
    return HealthStatus(status="ok")


@router.get("/ready", response_model=HealthStatus)
async def readiness(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "unavailable"

    try:
        redis = await get_redis()
        redis.ping()  # ping() on redis.asyncio is sync — no await
        redis_status = "ok"
    except Exception:
        redis_status = "unavailable"

    overall = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"
    return HealthStatus(status=overall, database=db_status, redis=redis_status)
