import structlog
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import AsyncSessionLocal
from app.models.route import Transfer, Route, RouteStatus
from app.models.fare import Fare, FareType

log = structlog.get_logger()


async def run_transfer_fare_sync():
    log.info("job_start", job="transfer_fare_sync")
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Transfer).where(Transfer.is_active == True)
        )
        transfers = result.scalars().all()

        updated = 0
        deactivated = 0

        for transfer in transfers:
            leg1 = await db.get(Route, transfer.leg1_route_id)
            leg2 = await db.get(Route, transfer.leg2_route_id)

            if not leg1 or not leg2:
                transfer.is_active = False
                deactivated += 1
                continue

            if (
                leg1.route_status != RouteStatus.ACTIVE
                or leg2.route_status != RouteStatus.ACTIVE
            ):
                transfer.is_active = False
                deactivated += 1
                continue

            leg1_fare_result = await db.execute(
                select(Fare).where(
                    Fare.route_id == leg1.id,
                    Fare.fare_type == FareType.PEAK,
                    Fare.day_type == 0,
                )
            )
            leg1_fare = leg1_fare_result.scalars().first()

            leg2_fare_result = await db.execute(
                select(Fare).where(
                    Fare.route_id == leg2.id,
                    Fare.fare_type == FareType.PEAK,
                    Fare.day_type == 0,
                )
            )
            leg2_fare = leg2_fare_result.scalars().first()

            if leg1_fare and leg2_fare:
                transfer.total_fare_kes = leg1_fare.amount_kes + leg2_fare.amount_kes
                updated += 1

        await db.commit()
    log.info("job_done", job="transfer_fare_sync",
             updated=updated, deactivated=deactivated)
