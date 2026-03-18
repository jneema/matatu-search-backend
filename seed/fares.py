from datetime import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.route import Route
from app.models.fare import Fare, FareType, PaymentMethod, PaymentMethodType


async def seed_fares(db: AsyncSession):
    result = await db.execute(
        select(Route).options(selectinload(Route.sacco))
    )
    routes = result.scalars().all()

    fare_configs = {
        "Super Metro": {"peak": 100, "off_peak": 80,  "late_night": 120, "weekend": 80},
        "Kenya Mpya":  {"peak": 70,  "off_peak": 60,  "late_night": 90,  "weekend": 60},
        "Metro Trans": {"peak": 100, "off_peak": 80,  "late_night": 120, "weekend": 80},
        "Joy Kenya":   {"peak": 60,  "off_peak": 50,  "late_night": 80,  "weekend": 50},
        "Paradiso":    {"peak": 150, "off_peak": 120, "late_night": 180, "weekend": 120},
    }

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
        config = fare_configs.get(sacco_name, {"peak": 100, "off_peak": 80, "late_night": 120, "weekend": 80})

        fares = [
            Fare(route_id=route.id, fare_type=FareType.PEAK,           day_type=0, amount_kes=config["peak"],        valid_from=time(6, 0),      valid_until=time(9, 0)),
            Fare(route_id=route.id, fare_type=FareType.PEAK,           day_type=0, amount_kes=config["peak"],        valid_from=time(16, 0),     valid_until=time(20, 0)),
            Fare(route_id=route.id, fare_type=FareType.OFF_PEAK,       day_type=0, amount_kes=config["off_peak"],    valid_from=time(9, 0),      valid_until=time(16, 0)),
            Fare(route_id=route.id, fare_type=FareType.LATE_NIGHT,     day_type=0, amount_kes=config["late_night"],  valid_from=time(21, 0),     valid_until=time(23, 59, 59)),
            Fare(route_id=route.id, fare_type=FareType.WEEKEND,        day_type=1, amount_kes=config["weekend"],     valid_from=time(0, 0),      valid_until=time(23, 59, 59)),
            Fare(route_id=route.id, fare_type=FareType.PUBLIC_HOLIDAY,  day_type=2, amount_kes=config["late_night"],  valid_from=time(0, 0),      valid_until=time(23, 59, 59)),
        ]
        for f in fares:
            db.add(f)
        total_fares += len(fares)

        for method in payment_configs.get(sacco_name, [PaymentMethodType.CASH]):
            db.add(PaymentMethod(route_id=route.id, method=method))

    await db.commit()
    print(f"  seeded {total_fares} fare rows and payment methods")