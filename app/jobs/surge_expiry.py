import structlog
from datetime import datetime, timezone
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.alert import CorridorSurge

log = structlog.get_logger()


async def run_surge_expiry():
    log.info("job_start", job="surge_expiry")
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(CorridorSurge).where(
                CorridorSurge.is_active == True,
                CorridorSurge.active_until < now,
            )
        )
        expired = result.scalars().all()
        for surge in expired:
            surge.is_active = False
        await db.commit()
    log.info("job_done", job="surge_expiry", expired_count=len(expired))