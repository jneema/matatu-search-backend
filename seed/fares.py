from datetime import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.route import Route
from app.models.fare import Fare, FareType, PaymentMethod, PaymentMethodType


async def seed_fares(db: AsyncSession):
    # Fetch routes with their Sacco and Path info to determine trip length
    result = await db.execute(
        select(Route).options(
            selectinload(Route.sacco),
            selectinload(Route.path)
        )
    )
    routes = result.scalars().all()

    # Configuration for Terminus-to-Terminus (Long) trips
    fare_configs = {
        "Super Metro": {"peak": 100, "off_peak": 80,  "late_night": 120, "weekend": 80},
        "Kenya Mpya":  {"peak": 80,  "off_peak": 60,  "late_night": 100, "weekend": 70},
        "Metro Trans": {"peak": 80,  "off_peak": 50,  "late_night": 100, "weekend": 60},
        "Joy Kenya":   {"peak": 70,  "off_peak": 50,  "late_night": 90,  "weekend": 50},
        "Paradiso":    {"peak": 120, "off_peak": 100, "late_night": 150, "weekend": 100},
    }

    # Payment support per Sacco
    payment_configs = {
        "Super Metro": [PaymentMethodType.CASH, PaymentMethodType.MPESA],
        "Kenya Mpya":  [PaymentMethodType.CASH],
        "Metro Trans": [PaymentMethodType.CASH, PaymentMethodType.MPESA, PaymentMethodType.TAP],
        "Joy Kenya":   [PaymentMethodType.CASH],
        "Paradiso":    [PaymentMethodType.CASH, PaymentMethodType.MPESA],
    }

    total_fares = 0
    for route in routes:
        sacco_name = route.sacco.name
        config = fare_configs.get(
            sacco_name, {"peak": 100, "off_peak": 80, "late_night": 120, "weekend": 80})

        # --- SECTIONAL FARE LOGIC ---
        # If the route has many stops (like Kenya Mpya), we simulate
        # that short distance 'Between' trips are cheaper than the full route.
        is_short_route = len(route.path) < 4
        fare_modifier = 0.7 if is_short_route else 1.0

        def adj(price): return int(price * fare_modifier)

        fares = [
            # Weekday Peak Morning
            Fare(route_id=route.id, fare_type=FareType.PEAK, day_type=0,
                 amount_kes=adj(config["peak"]), valid_from=time(6, 0), valid_until=time(9, 0)),

            # Weekday Peak Evening
            Fare(route_id=route.id, fare_type=FareType.PEAK, day_type=0,
                 amount_kes=adj(config["peak"]), valid_from=time(16, 0), valid_until=time(20, 0)),

            # Weekday Off-Peak
            Fare(route_id=route.id, fare_type=FareType.OFF_PEAK, day_type=0,
                 amount_kes=adj(config["off_peak"]), valid_from=time(9, 0), valid_until=time(16, 0)),

            # Late Night
            Fare(route_id=route.id, fare_type=FareType.LATE_NIGHT, day_type=0,
                 amount_kes=adj(config["late_night"]), valid_from=time(21, 0), valid_until=time(23, 59)),

            # Weekend
            Fare(route_id=route.id, fare_type=FareType.WEEKEND, day_type=1,
                 amount_kes=adj(config["weekend"]), valid_from=time(0, 0), valid_until=time(23, 59)),
        ]

        for f in fares:
            db.add(f)

        total_fares += len(fares)

        # Add Payment Methods
        methods = payment_configs.get(sacco_name, [PaymentMethodType.CASH])
        for method in methods:
            db.add(PaymentMethod(route_id=route.id, method=method))

    await db.commit()
    print(
        f"  Seeded {total_fares} directional fare rows with sectional pricing modifiers.")
