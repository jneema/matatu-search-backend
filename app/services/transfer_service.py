from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.route import Transfer, Route
from app.models.stage import Stage


async def get_transfers(
    origin_stage_ids: list,
    dest_stage_ids: list,
    db: AsyncSession,
) -> list[Transfer]:
    result = await db.execute(
        select(Transfer).where(
            Transfer.is_active == True,
        )
    )
    all_transfers = result.scalars().all()

    matches = []
    for transfer in all_transfers:
        leg1 = await db.get(Route, transfer.leg1_route_id)
        leg2 = await db.get(Route, transfer.leg2_route_id)
        if leg1 is None or leg2 is None:
            continue
        if (
            leg1.origin_stage_id in origin_stage_ids
            and leg2.dest_stage_id in dest_stage_ids
        ):
            matches.append(transfer)

    return matches
