from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.route import Route, RouteStatus, Corridor
from app.models.stage import Stage
from app.models.fare import Fare, PaymentMethod


async def build_corridor_bundle(corridor_id, db: AsyncSession) -> dict:
    result = await db.execute(
        select(Route).where(
            Route.corridor_id == corridor_id,
            Route.route_status == RouteStatus.ACTIVE,
        )
    )
    routes = result.scalars().all()

    bundle_routes = []
    for route in routes:
        fares_result = await db.execute(
            select(Fare).where(Fare.route_id == route.id)
        )
        fares = fares_result.scalars().all()

        payments_result = await db.execute(
            select(PaymentMethod).where(PaymentMethod.route_id == route.id)
        )
        payments = payments_result.scalars().all()

        bundle_routes.append({
            "id": str(route.id),
            "via": route.via_description,
            "is_express": route.is_express,
            "fares": [
                {
                    "type": f.fare_type.value,
                    "day_type": f.day_type,
                    "amount_kes": f.amount_kes,
                    "valid_from": str(f.valid_from),
                    "valid_until": str(f.valid_until),
                }
                for f in fares
            ],
            "payment_methods": [p.method.value for p in payments],
        })

    return {
        "corridor_id": str(corridor_id),
        "routes": bundle_routes,
    }
