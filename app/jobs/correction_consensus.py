import structlog
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func
from app.db.session import AsyncSessionLocal
from app.models.intelligence import FareCorrection, CorrectionStatus, AppSettings
from app.models.route import Route

log = structlog.get_logger()


async def run_correction_consensus():
    log.info("job_start", job="correction_consensus")
    async with AsyncSessionLocal() as db:
        consensus_count = 3
        window_days = 7

        result = await db.execute(
            select(AppSettings).where(AppSettings.key == "correction_consensus_count")
        )
        setting = result.scalar_one_or_none()
        if setting:
            consensus_count = int(setting.value)

        result = await db.execute(
            select(AppSettings).where(AppSettings.key == "correction_window_days")
        )
        setting = result.scalar_one_or_none()
        if setting:
            window_days = int(setting.value)

        cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)

        result = await db.execute(
            select(
                FareCorrection.route_id,
                FareCorrection.fare_type,
                FareCorrection.reported_amount_kes,
                func.count(FareCorrection.id).label("report_count"),
            )
            .where(
                FareCorrection.status == CorrectionStatus.PENDING,
                FareCorrection.reported_at >= cutoff,
            )
            .group_by(
                FareCorrection.route_id,
                FareCorrection.fare_type,
                FareCorrection.reported_amount_kes,
            )
            .having(func.count(FareCorrection.id) >= consensus_count)
        )
        consensus_hits = result.all()

        flagged = 0
        for hit in consensus_hits:
            route = await db.get(Route, hit.route_id)
            if route:
                route.fare_last_verified_at = None
                flagged += 1

            corrections_result = await db.execute(
                select(FareCorrection).where(
                    FareCorrection.route_id == hit.route_id,
                    FareCorrection.fare_type == hit.fare_type,
                    FareCorrection.reported_amount_kes == hit.reported_amount_kes,
                    FareCorrection.status == CorrectionStatus.PENDING,
                )
            )
            for correction in corrections_result.scalars().all():
                correction.status = CorrectionStatus.ACCEPTED

        await db.commit()
    log.info("job_done", job="correction_consensus", flagged_routes=flagged)