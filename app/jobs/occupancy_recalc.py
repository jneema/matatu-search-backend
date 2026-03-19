import structlog
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.intelligence import Occupancy
from datetime import datetime, timezone

log = structlog.get_logger()


async def run_occupancy_recalc():
    log.info("job_start", job="occupancy_recalc")
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Occupancy))
        all_occupancy = result.scalars().all()

        for occ in all_occupancy:
            occ.updated_at = datetime.now(timezone.utc)

        await db.commit()
    log.info("job_done", job="occupancy_recalc", rows=len(all_occupancy))