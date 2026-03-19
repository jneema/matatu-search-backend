from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.route import Route
from app.models.sacco import VehicleType
from app.schemas.trip import TripOption, TripResponse
from app.services.fare_service import get_current_fare, get_active_surge, apply_surge
from app.services.trust_service import get_data_confidence
from app.utils.time_utils import NAIROBI_TZ
from app.utils.geo import is_within_radius


async def build_trip_option(
    route: Route,
    db: AsyncSession,
    now: datetime,
    user_lat: float | None = None,
    user_lng: float | None = None,
    lang: str = "en",
) -> TripOption:
    fare_amount, fare_type_now = await get_current_fare(route.id, db, now)
    surge = await get_active_surge(route.corridor_id, db, now)
    final_fare, surge_active, surge_reason = await apply_surge(fare_amount, surge)
    confidence = await get_data_confidence(route, db)

    tags = []
    if route.is_express:
        tags.append("express")
    if route.sacco.is_electric:
        tags.append("electric")
    if route.sacco.vehicle_type == VehicleType.SEATER_14:
        tags.append("comfort")
    if "off_peak" in fare_type_now:
        tags.append("off_peak")
    if confidence == "low":
        tags.append("data_unverified")

    payment_methods = [p.method.value for p in route.payment_methods]
    if "mpesa" in payment_methods:
        tags.append("mpesa")

    nearby = False
    if user_lat and user_lng:
        for stop in route.path:
            stage = stop.stage
            if is_within_radius(user_lat, user_lng, float(stage.latitude), float(stage.longitude)):
                nearby = True
                tags.append("nearby_stage")
                break

    likely_full = False
    current_hour = now.hour
    current_dow = now.weekday()
    for occ in route.occupancy:
        if occ.day_of_week == current_dow and occ.hour_slot == current_hour:
            likely_full = occ.avg_load_factor >= 0.85
            break

    via = route.via_description
    if lang == "sw" and route.via_description_sw:
        via = route.via_description_sw

    from app.schemas.alert import RouteAlertRead
    active_alerts = [
        RouteAlertRead.model_validate(a)
        for a in route.alerts
        if a.is_active and a.active_from <= now <= a.active_until
    ]

    if any(a.alert_type.value == "short_loop" for a in active_alerts):
        tags.append("short_loop_warning")

    return TripOption(
        route_id=route.id,
        sacco=route.sacco.name,
        vehicle_type=route.sacco.vehicle_type,
        via=via,
        terminus_area=route.sacco.terminus_area,
        fare=final_fare,
        fare_type_now=fare_type_now,
        is_off_peak_now="off_peak" in fare_type_now,
        duration_mins=route.peak_duration_mins if "peak" in fare_type_now else route.avg_duration_mins,
        wait_mins_est=route.departure_frequency_mins,
        payment_methods=payment_methods,
        safety_rating=float(
            route.sacco.safety_rating) if route.sacco.safety_rating else None,
        comfort_rating=float(
            route.sacco.comfort_rating) if route.sacco.comfort_rating else None,
        likely_full=likely_full,
        tags=tags,
        data_confidence=confidence,
        surge_active=surge_active,
        surge_reason=surge_reason,
        active_alerts=active_alerts,
        is_transfer=False,
    )


async def build_trip_response(
    routes: list[Route],
    origin_stage_names: list[str],
    dest_stage_names: list[str],
    trip_label: str,
    db: AsyncSession,
    now: datetime | None = None,
    user_lat: float | None = None,
    user_lng: float | None = None,
    budget_kes: int | None = None,
    payment_preference: str | None = None,
    lang: str = "en",
) -> TripResponse:
    if now is None:
        now = datetime.now(NAIROBI_TZ)

    options = []
    for route in routes:
        option = await build_trip_option(route, db, now, user_lat, user_lng, lang)

        if budget_kes and option.fare > budget_kes:
            continue
        if payment_preference and payment_preference not in option.payment_methods:
            continue

        options.append(option)

    options.sort(key=lambda o: o.fare)

    if options:
        options[0].tags.append("cheapest")

    fastest = min(options, key=lambda o: o.duration_mins or 9999, default=None)
    if fastest:
        fastest.tags.append("fastest")

    scenarios = {
        "express":  [o for o in options if "express" in o.tags],
        "cheapest": [o for o in options if "cheapest" in o.tags],
        "comfort":  [o for o in options if "comfort" in o.tags],
        "electric": [o for o in options if "electric" in o.tags],
        "off_peak": [o for o in options if "off_peak" in o.tags],
    }

    return TripResponse(
        trip=trip_label,
        queried_at=now.isoformat(),
        origin_stages=origin_stage_names,
        dest_stages=dest_stage_names,
        scenarios=scenarios,
        all_options=options,
    )
