from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import structlog

log = structlog.get_logger()

scheduler = AsyncIOScheduler()


def setup_scheduler():
    from app.jobs.correction_consensus import run_correction_consensus
    from app.jobs.transfer_fare_sync import run_transfer_fare_sync
    from app.jobs.occupancy_recalc import run_occupancy_recalc
    from app.jobs.surge_expiry import run_surge_expiry

    scheduler.add_job(
        run_surge_expiry,
        IntervalTrigger(minutes=15),
        id="surge_expiry",
        replace_existing=True,
    )

    scheduler.add_job(
        run_correction_consensus,
        IntervalTrigger(hours=6),
        id="correction_consensus",
        replace_existing=True,
    )

    scheduler.add_job(
        run_transfer_fare_sync,
        CronTrigger(hour=2, minute=0),
        id="transfer_fare_sync",
        replace_existing=True,
    )

    scheduler.add_job(
        run_occupancy_recalc,
        CronTrigger(day_of_week="sun", hour=3, minute=0),
        id="occupancy_recalc",
        replace_existing=True,
    )

    log.info("scheduler_jobs_registered", job_count=len(scheduler.get_jobs()))