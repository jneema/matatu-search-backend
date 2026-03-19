from unittest import result

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from datetime import datetime, timezone
from app.db.session import get_db
from app.models.route import Route, RouteStatus
from app.models.stage import Direction
from app.schemas.trip import TripResponse
from app.services.stage_resolver import resolve_stage
from app.services.scenario_engine import build_trip_response
from app.cache.keys import trip_search_key
from app.cache.decorators import cache_get, cache_set
import structlog

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1/trips", tags=["trips"])


@router.get("/search", response_model=TripResponse)
async def search_trips(
    origin: str = Query(...),
    destination: str = Query(...),
    budget_kes: int | None = Query(None),
    payment_preference: str | None = Query(None),
    user_lat: float | None = Query(None),
    user_lng: float | None = Query(None),
    include_transfers: bool = Query(True),
    lang: str = Query("en"),
    db: AsyncSession = Depends(get_db),
):
    from fastapi import HTTPException

    origin_result = await resolve_stage(origin, db, direction_filter=Direction.INBOUND)
    if not origin_result:
        raise HTTPException(
            status_code=404,
            detail={"error": "STAGE_NOT_FOUND",
                    "message": f"Could not resolve origin stage from '{origin}'"}
        )

    dest_result = await resolve_stage(destination, db)
    if not dest_result:
        raise HTTPException(
            status_code=404,
            detail={"error": "STAGE_NOT_FOUND",
                    "message": f"Could not resolve destination stage from '{destination}'"}
        )

    origin_stage = origin_result.stage
    dest_stage = dest_result.stage

    now = datetime.now(timezone.utc)

    # Only cache when no user-specific params are passed
    use_cache = not any([budget_kes, payment_preference, user_lat, user_lng])
    cache_key = trip_search_key(
        str(origin_stage.id), str(dest_stage.id), now.hour)

    if use_cache:
        cached = await cache_get(cache_key)
        if cached:
            log.info("cache_hit", key=cache_key)
            return cached

    result = await db.execute(
        select(Route).where(
            Route.origin_stage_id == origin_stage.id,
            Route.dest_stage_id == dest_stage.id,
            Route.route_status == RouteStatus.ACTIVE,
        ).options(
            selectinload(Route.sacco),
            selectinload(Route.fares),
            selectinload(Route.payment_methods),
            selectinload(Route.alerts),
            selectinload(Route.occupancy),
            selectinload(Route.path),
        )
    )
    routes = list(result.scalars().all())

    response = await build_trip_response(
        routes=routes,
        origin_stage_names=[origin_stage.name],
        dest_stage_names=[dest_stage.name],
        trip_label=f"{origin_stage.name} → {dest_stage.name}",
        db=db,
        now=now,
        user_lat=user_lat,
        user_lng=user_lng,
        budget_kes=budget_kes,
        payment_preference=payment_preference,
        lang=lang,
    )

    if use_cache:
        await cache_set(cache_key, response.model_dump(mode="json"), ttl_seconds=120)
        log.info("cache_set", key=cache_key)

    return response
