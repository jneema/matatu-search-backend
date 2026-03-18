from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.route import Route, Transfer
from app.models.stage import Stage, Direction


async def seed_transfers(db: AsyncSession):
    result = await db.execute(select(Stage).where(Stage.area == "Roysambu", Stage.direction == Direction.INBOUND))
    roysambu = result.scalars().first()

    if not roysambu:
        print("  skipping transfers — Roysambu stage not found")
        return

    result = await db.execute(select(Route))
    routes = result.scalars().all()

    print(f"  skipping transfers — add manually once transfer stages are seeded")