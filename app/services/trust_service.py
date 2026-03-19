import structlog
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.route import Route
from app.utils.time_utils import NAIROBI_TZ

log = structlog.get_logger()


async def get_data_confidence(route: Route, db: AsyncSession) -> str:
    from app.models.intelligence import FareCorrection, AppSettings

    if route.fare_last_verified_at is None:
        return "low"

    now = datetime.now(NAIROBI_TZ)
    age_days = (now - route.fare_last_verified_at).days

    high_days = 7
    medium_days = 21

    result = await db.execute(
        select(AppSettings).where(
            AppSettings.key == "fare_staleness_high_days")
    )
    setting = result.scalar_one_or_none()
    if setting:
        high_days = int(setting.value)

    result = await db.execute(
        select(AppSettings).where(
            AppSettings.key == "fare_staleness_medium_days")
    )
    setting = result.scalar_one_or_none()
    if setting:
        medium_days = int(setting.value)

    if age_days > medium_days:
        return "low"

    result = await db.execute(
        select(FareCorrection).where(
            FareCorrection.route_id == route.id,
            FareCorrection.status == "pending",
            FareCorrection.reported_at >= now - timedelta(days=7),
        )
    )
    pending_corrections = len(result.scalars().all())

    if pending_corrections >= 3:
        return "low"
    if age_days > high_days or pending_corrections >= 1:
        return "medium"
    return "high"
