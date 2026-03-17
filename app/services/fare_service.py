from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.fare import Fare, FareType
from app.models.alert import CorridorSurge
from app.models.intelligence import AppSettings
from app.utils.time_utils import get_day_type, is_time_in_window, NAIROBI_TZ


async def get_public_holiday_dates(db: AsyncSession) -> list[date]:
    from app.models.fare import PublicHoliday
    result = await db.execute(select(PublicHoliday))
    return [h.holiday_date for h in result.scalars().all()]


async def get_current_fare(
    route_id,
    db: AsyncSession,
    now: datetime | None = None,
) -> tuple[int, str]:
    """Returns (amount_kes, fare_type_name)"""
    if now is None:
        now = datetime.now(NAIROBI_TZ)

    holidays = await get_public_holiday_dates(db)
    day_type = get_day_type(now, holidays)

    result = await db.execute(
        select(Fare).where(Fare.route_id == route_id)
    )
    fares = result.scalars().all()

    for fare in fares:
        if fare.day_type == day_type:
            from_str = str(fare.valid_from)
            until_str = str(fare.valid_until)
            if is_time_in_window(now, from_str, until_str):
                return fare.amount_kes, fare.fare_type.value

    for fare in fares:
        if fare.day_type == day_type and fare.fare_type == FareType.OFF_PEAK:
            return fare.amount_kes, fare.fare_type.value

    if fares:
        return fares[0].amount_kes, fares[0].fare_type.value

    return 0, "unknown"


async def get_active_surge(
    corridor_id,
    db: AsyncSession,
    now: datetime | None = None,
) -> CorridorSurge | None:
    if corridor_id is None:
        return None
    if now is None:
        now = datetime.now(NAIROBI_TZ)

    result = await db.execute(
        select(CorridorSurge).where(
            CorridorSurge.corridor_id == corridor_id,
            CorridorSurge.is_active == True,
            CorridorSurge.active_from <= now,
            CorridorSurge.active_until >= now,
        )
    )
    return result.scalar_one_or_none()


async def apply_surge(amount_kes: int, surge: CorridorSurge | None) -> tuple[int, bool, str | None]:
    """Returns (final_amount, surge_active, surge_reason)"""
    if surge is None:
        return amount_kes, False, None
    multiplier = float(surge.multiplier)
    return int(amount_kes * multiplier), True, surge.reason