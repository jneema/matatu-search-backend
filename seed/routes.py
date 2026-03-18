from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.route import Route, RouteStatus, Corridor
from app.models.stage import Stage, Direction


async def seed_routes(db: AsyncSession, saccos: dict, stages: dict) -> dict:
    thika_corridor = Corridor(name="Thika Road Corridor", description="All routes along Thika Road superhighway")
    db.add(thika_corridor)
    await db.commit()

    juja_inbound = stages.get("Juja_inbound")
    gpo = stages.get("CBD_both")
    otc = stages.get("CBD_both")

    result = await db.execute(select(Stage).where(Stage.area == "CBD", Stage.direction == Direction.BOTH))
    cbd_stages = result.scalars().all()
    gpo_stage = next((s for s in cbd_stages if "GPO" in s.name), cbd_stages[0] if cbd_stages else None)
    otc_stage = next((s for s in cbd_stages if "OTC" in s.name), cbd_stages[0] if cbd_stages else None)

    result = await db.execute(select(Stage).where(Stage.area == "Juja", Stage.direction == Direction.INBOUND))
    juja_stage = (await result.scalars().first()) if False else None
    juja_result = await db.execute(select(Stage).where(Stage.area == "Juja", Stage.direction == Direction.INBOUND))
    juja_stage = juja_result.scalars().first()

    now = datetime.now(timezone.utc)

    routes_data = [
        Route(sacco_id=saccos["Super Metro"].id, corridor_id=thika_corridor.id, origin_stage_id=juja_stage.id, dest_stage_id=otc_stage.id, via_description="via Expressway", via_description_sw="kupitia Barabara ya Kasi", is_express=True, route_status=RouteStatus.ACTIVE, departure_frequency_mins=5, avg_duration_mins=40, peak_duration_mins=55, fare_last_verified_at=now, last_confirmed_at=now),
        Route(sacco_id=saccos["Kenya Mpya"].id, corridor_id=thika_corridor.id, origin_stage_id=juja_stage.id, dest_stage_id=gpo_stage.id, via_description="via Service Lane", via_description_sw="kupitia Barabara ya Huduma", is_express=False, route_status=RouteStatus.ACTIVE, departure_frequency_mins=8, avg_duration_mins=50, peak_duration_mins=70, fare_last_verified_at=now, last_confirmed_at=now),
        Route(sacco_id=saccos["Metro Trans"].id, corridor_id=thika_corridor.id, origin_stage_id=juja_stage.id, dest_stage_id=gpo_stage.id, via_description="via Expressway", is_express=True, route_status=RouteStatus.ACTIVE, departure_frequency_mins=10, avg_duration_mins=42, peak_duration_mins=57, fare_last_verified_at=now, last_confirmed_at=now),
        Route(sacco_id=saccos["Joy Kenya"].id, corridor_id=thika_corridor.id, origin_stage_id=juja_stage.id, dest_stage_id=gpo_stage.id, via_description="via Old Thika Road", is_express=False, route_status=RouteStatus.ACTIVE, departure_frequency_mins=12, avg_duration_mins=60, peak_duration_mins=80, fare_last_verified_at=now, last_confirmed_at=now),
        Route(sacco_id=saccos["Paradiso"].id, corridor_id=thika_corridor.id, origin_stage_id=juja_stage.id, dest_stage_id=otc_stage.id, via_description="via Expressway", is_express=True, route_status=RouteStatus.ACTIVE, departure_frequency_mins=15, avg_duration_mins=38, peak_duration_mins=52, fare_last_verified_at=now, last_confirmed_at=now),
    ]
    for r in routes_data:
        db.add(r)
    await db.commit()

    print(f"  seeded {len(routes_data)} routes and 1 corridor")
    return {r.sacco_id: r for r in routes_data}