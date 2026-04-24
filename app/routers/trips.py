from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload, aliased
from datetime import datetime, timezone

from app.db.session import get_db
from app.models.route import Route, RoutePath, RouteStatus
from app.schemas.trip import TripResponse, TripOption, TransferDetail
from app.services.stage_resolver import resolve_stage

router = APIRouter(prefix="/api/v1/trips", tags=["trips"])


TRANSFER_HUBS = [
    "OTC Terminal",
    "GPO Drop-off",
    "GPO Pick-up",
    "Roysambu (TRM)",
    "Githurai 45",
]


def extract_fare(route):
    if not route.fares:
        return 0
    return min(f.amount_kes for f in route.fares)


def estimate_wait_time(route_a, route_b):
    freq_a = getattr(route_a, "departure_frequency_mins", 10)
    freq_b = getattr(route_b, "departure_frequency_mins", 10)
    return int(((freq_a + freq_b) / 2) * 0.6)


def build_trip_option(route) -> TripOption:
    return TripOption(
        route_id=route.id,
        sacco=route.sacco.name,
        vehicle_type=route.sacco.vehicle_type,
        via=None,
        terminus_area=getattr(route.sacco, "terminus_area", None),
        fare=extract_fare(route),
        fare_type_now="STANDARD",
        off_peak_fare=None,
        peak_fare=None,
        is_off_peak_now=True,
        duration_mins=getattr(route, "avg_duration_mins", None),
        wait_mins_est=None,
        payment_methods=[],
        safety_rating=getattr(route.sacco, "safety_rating", None),
        comfort_rating=getattr(route.sacco, "comfort_rating", None),
        likely_full=False,
        tags=[],
        data_confidence="0.85",
        surge_active=False,
        surge_reason=None,
        active_alerts=[],
        is_transfer=False,
        transfer_detail=None,
        origin_stage=None,
        dest_stage=None,
    )


def pick_best_transfer(routes_a, routes_b):
    for hub in TRANSFER_HUBS:
        for ra in routes_a:
            ra_stages = [p.stage.name for p in ra.path]
            if hub not in ra_stages:
                continue

            for rb in routes_b:
                rb_stages = [p.stage.name for p in rb.path]
                if hub in rb_stages:
                    return hub, ra, rb

    return None, None, None


@router.get("/search", response_model=TripResponse)
async def search_trips(
    origin: str = Query(...),
    destination: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    now = datetime.now(timezone.utc)

    origin_result = await resolve_stage(origin, db)
    dest_result = await resolve_stage(destination, db)

    if not origin_result or not dest_result:
        raise HTTPException(status_code=404, detail="Stage not found")

    origin_st = origin_result.stage
    dest_st = dest_result.stage

    p1 = aliased(RoutePath)
    p2 = aliased(RoutePath)

    direct_query = (
        select(Route)
        .join(p1, Route.id == p1.route_id)
        .join(p2, Route.id == p2.route_id)
        .where(
            and_(
                Route.route_status == RouteStatus.ACTIVE,
                p1.stage_id == origin_st.id,
                p2.stage_id == dest_st.id,
                p1.stop_order < p2.stop_order,
            )
        )
        .options(
            selectinload(Route.sacco),
            selectinload(Route.fares),
            selectinload(Route.path).selectinload(RoutePath.stage),
        )
        .distinct()
    )
    direct_routes = (await db.execute(direct_query)).scalars().all()

    origin_query = (
        select(Route)
        .join(RoutePath)
        .where(
            Route.route_status == RouteStatus.ACTIVE,
            RoutePath.stage_id == origin_st.id,
        )
        .options(
            selectinload(Route.path).selectinload(RoutePath.stage),
            selectinload(Route.fares),
            selectinload(Route.sacco),
        )
    )
    origin_routes = (await db.execute(origin_query)).scalars().all()

    dest_query = (
        select(Route)
        .join(RoutePath)
        .where(
            Route.route_status == RouteStatus.ACTIVE,
            RoutePath.stage_id == dest_st.id,
        )
        .options(
            selectinload(Route.path).selectinload(RoutePath.stage),
            selectinload(Route.fares),
            selectinload(Route.sacco),
        )
    )
    dest_routes = (await db.execute(dest_query)).scalars().all()

    scenarios: dict = {}
    all_options: list[TripOption] = []

    if direct_routes:
        direct_options = []
        for route in direct_routes:
            opt = build_trip_option(route)
            if route.is_express:
                opt.tags = ["EXPRESS"]
            direct_options.append(opt)

        direct_options.sort(key=lambda o: (o.duration_mins or 999))
        scenarios["DIRECT"] = direct_options
        all_options.extend(direct_options)

    hub, route_a, route_b = pick_best_transfer(origin_routes, dest_routes)

    if hub and route_a and route_b:
        transfer_opt = TripOption(
            route_id=route_a.id,
            sacco=route_a.sacco.name,
            vehicle_type=route_a.sacco.vehicle_type,
            via=hub,
            terminus_area=None,
            fare=extract_fare(route_a) + extract_fare(route_b),
            fare_type_now="TRANSFER",
            off_peak_fare=None,
            peak_fare=None,
            is_off_peak_now=True,
            duration_mins=(
                getattr(route_a, "avg_duration_mins", 0)
                + getattr(route_b, "avg_duration_mins", 0)
                + estimate_wait_time(route_a, route_b)
            ),
            wait_mins_est=estimate_wait_time(route_a, route_b),
            payment_methods=[],
            safety_rating=None,
            comfort_rating=None,
            likely_full=False,
            tags=["TRANSFER"],
            data_confidence="0.75",
            surge_active=False,
            surge_reason=None,
            active_alerts=[],
            is_transfer=True,
            transfer_detail=TransferDetail(
                transfer_stage=hub,
                avg_wait_mins=estimate_wait_time(route_a, route_b),
                leg1_sacco=route_a.sacco.name,
                leg2_sacco=route_b.sacco.name,
            ),
            origin_stage=None,
            dest_stage=None,
        )
        scenarios["TRANSFER"] = [transfer_opt]
        all_options.append(transfer_opt)

    if not all_options:
        raise HTTPException(status_code=404, detail="No routes found")

    all_options.sort(key=lambda o: (
        1 if o.is_transfer else 0,
        o.duration_mins or 999,
    ))

    return TripResponse(
        trip=f"{origin_st.name} → {dest_st.name}",
        queried_at=now.isoformat(),
        origin_stages=[origin_st.name],
        dest_stages=[dest_st.name],
        scenarios=scenarios,
        all_options=all_options,
    )
