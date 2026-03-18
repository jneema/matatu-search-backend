import asyncio
from app.db.session import AsyncSessionLocal
from seed.app_settings import seed_app_settings
from seed.public_holidays import seed_public_holidays
from seed.stages import seed_stages
from seed.saccos import seed_saccos
from seed.routes import seed_routes
from seed.fares import seed_fares
from seed.transfers import seed_transfers


async def run():
    print("seeding database...")
    async with AsyncSessionLocal() as db:
        print("app settings...")
        await seed_app_settings(db)

        print("public holidays...")
        await seed_public_holidays(db)

        print("stages...")
        stages = await seed_stages(db)

        print("saccos...")
        saccos = await seed_saccos(db)

        print("routes...")
        await seed_routes(db, saccos, stages)

        print("fares...")
        await seed_fares(db)

        print("transfers...")
        await seed_transfers(db)

    print("done.")


if __name__ == "__main__":
    asyncio.run(run())