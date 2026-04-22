from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.route import Route, Transfer
from app.models.stage import Stage


async def seed_transfers(db: AsyncSession):
    print("seeding multi-leg transfers...")

    # 1. Fetch Routes and Stages for lookup
    # We need to find routes by Sacco name and destination to get the right IDs
    route_result = await db.execute(select(Route))
    all_routes = route_result.scalars().all()

    stage_result = await db.execute(select(Stage))
    stages = {s.name: s.id for s in stage_result.scalars().all()}

    # Helper to find a specific route ID by sacco name and destination
    def get_route_id(sacco_name: str, dest_name: str):
        for r in all_routes:
            # Assumes your Route model has a .sacco relationship with .name
            if r.sacco.name == sacco_name and r.dest_stage.name == dest_name:
                return r.id
        return None

    # 2. Define the Transfer Data
    # Example: Taking a matatu from Juja, dropping at Roysambu,
    # then taking a Metro Trans to GPO.
    transfers_to_seed = [
        {
            "leg1_route_id": get_route_id("Kenya Mpya", "OTC Terminal"),
            "leg2_route_id": get_route_id("Metro Trans", "GPO Drop-off"),
            "transfer_stage_id": stages.get("Roysambu (TRM)"),
            "avg_wait_mins": 12,
            "total_fare_kes": 150,
            "is_active": True
        },
        {
            "leg1_route_id": get_route_id("Super Metro", "OTC Terminal"),
            # Changing at CBD
            "leg2_route_id": get_route_id("Joy Kenya", "River Road"),
            "transfer_stage_id": stages.get("OTC Terminal"),
            "avg_wait_mins": 5,
            "total_fare_kes": 100,
            "is_active": True
        },
        {
            "leg1_route_id": get_route_id("Kenya Mpya", "Pangani"),
            "leg2_route_id": get_route_id("Metro Trans", "GPO Drop-off"),
            "transfer_stage_id": stages.get("Pangani"),
            "avg_wait_mins": 8,
            "total_fare_kes": 120,
            "is_active": True
        },
        {
            "leg1_route_id": get_route_id("Metro Trans", "Muthaiga"),
            "leg2_route_id": get_route_id("Super Metro", "OTC Terminal"),
            "transfer_stage_id": stages.get("Muthaiga"),
            "avg_wait_mins": 6,
            "total_fare_kes": 110,
            "is_active": True
        },
        {
            "leg1_route_id": get_route_id("Joy Kenya", "River Road"),
            "leg2_route_id": get_route_id("Metro Trans", "Roysambu (TRM)"),
            "transfer_stage_id": stages.get("Pangani"),
            "avg_wait_mins": 10,
            "total_fare_kes": 130,
            "is_active": True
        }
    ]

    for data in transfers_to_seed:
        if all([data["leg1_route_id"], data["leg2_route_id"], data["transfer_stage_id"]]):
            transfer = Transfer(**data)
            db.add(transfer)
        else:
            print(f"⚠️ Skipping transfer: Missing one of the required IDs.")

    await db.commit()
    print("  Successfully seeded transfers.")
