from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.route import Route, RouteStatus, Corridor, RoutePath


async def seed_routes(db: AsyncSession, saccos: dict, stages: dict):

    corridor = Corridor(
        name="Nairobi Core Network",
        description="Full coverage matatu routing graph"
    )

    db.add(corridor)
    await db.commit()

    now = datetime.now(timezone.utc)

    async def create_route(sacco, origin, dest, via, path, freq, duration, is_express):

        if sacco not in saccos:
            return

        missing = [p for p in [origin, dest] + path if p not in stages]
        if missing:
            print("Missing stages:", missing)
            return

        route = Route(
            sacco_id=saccos[sacco].id,
            corridor_id=corridor.id,
            origin_stage_id=stages[origin].id,
            dest_stage_id=stages[dest].id,
            via_description=via,
            is_express=is_express,
            route_status=RouteStatus.ACTIVE,
            departure_frequency_mins=freq,
            avg_duration_mins=duration,
            fare_last_verified_at=now,
            last_confirmed_at=now
        )

        db.add(route)
        await db.flush()

        for i, s in enumerate(path):
            db.add(RoutePath(
                route_id=route.id,
                stage_id=stages[s].id,
                stop_order=i
            ))

    inbound_stages = [
        "Juja Main Stage_inbound",
        "Kenyatta University_inbound",
        "Githurai 45_inbound",
        "Roysambu (TRM)_inbound",
        "Garden City_inbound",
        "Muthaiga_inbound",
        "Pangani_inbound",
    ]

    cbd_inbound = [
        "OTC Terminal_inbound",
        "GPO Drop-off_inbound",
        "River Road_inbound"
    ]

    for origin in inbound_stages:
        for dest in cbd_inbound:

            await create_route(
                "Super Metro",
                origin,
                dest,
                "via Thika Road",
                [origin, dest],
                5,
                25,
                True
            )

            await create_route(
                "Kenya Mpya",
                origin,
                dest,
                "via Service Lane",
                [origin, "Githurai 45_inbound",
                    "Roysambu (TRM)_inbound", dest],
                10,
                55,
                False
            )

    # ==========================================================
    # 2. CBD → ALL OUTBOUND (FULL COVERAGE)
    # ==========================================================

    outbound_stages = [
        "OTC Stage_outbound",
        "GPO Pick-up_outbound",
        "River Road_outbound"
    ]

    north_stages = [
        "Juja Main Stage_outbound",
        "Kenyatta University_outbound",
        "Githurai 45_outbound",
        "Roysambu (TRM)_outbound",
        "Garden City_outbound",
        "Muthaiga_outbound",
        "Pangani_outbound",
    ]

    for origin in outbound_stages:
        for dest in north_stages:

            await create_route(
                "Metro Trans",
                origin,
                dest,
                "via Thika Road",
                [origin, "Pangani_outbound", dest],
                10,
                30,
                True
            )

            await create_route(
                "Joy Kenya",
                origin,
                dest,
                "via CBD corridor",
                [origin, "River Road_outbound", "Pangani_outbound", dest],
                15,
                45,
                False
            )

    cross_links = [
        ("Roysambu (TRM)_inbound", "GPO Drop-off_inbound"),
        ("Githurai 45_inbound", "River Road_inbound"),
        ("Pangani_outbound", "Roysambu (TRM)_outbound"),
        ("Muthaiga_outbound", "GPO Pick-up_outbound"),
    ]

    for o, d in cross_links:
        await create_route(
            "Paradiso",
            o,
            d,
            "express shuttle",
            [o, d],
            20,
            20,
            True
        )

    await db.commit()
    print(" FULL ROUTE COVERAGE SEED COMPLETE")
