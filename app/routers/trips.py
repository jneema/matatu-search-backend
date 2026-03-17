from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.db.session import get_db
from app.models.route import Route, RouteStatus
from app.models.stage import Stage
from app.schemas.trip import TripResponse
from app.services.stage_resolver import resolve_stage
from app.services.scenario_engine import build_trip_response
from app.schemas.common import ErrorResponse

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
    from app.models.stage import Direction

    origin_result = await resolve_stage(origin, db, direction_filter=Direction.INBOUND)
    if not origin_result:
        raise HTTPException(
            status_code=404,
            detail={"error": "STAGE_NOT_FOUND", "message": f"Could not resolve origin stage from '{origin}'"}
        )

    dest_result = await resolve_stage(destination, db)
    if not dest_result:
        raise HTTPException(
            status_code=404,
            detail={"error": "STAGE_NOT_FOUND", "message": f"Could not resolve destination stage from '{destination}'"}
        )

    origin_stage = origin_result.stage
    dest_stage = dest_result.stage

    result = await db.execute(
        select(Route).where(
            Route.origin_stage_id == origin_stage.id,
            Route.dest_stage_id == dest_stage.id,
            Route.route_status == RouteStatus.ACTIVE,
        ).options(
            __import__("sqlalchemy.orm", fromlist=["selectinload"]).selectinload(Route.sacco),
            __import__("sqlalchemy.orm", fromlist=["selectinload"]).selectinload(Route.fares),
            __import__("sqlalchemy.orm", fromlist=["selectinload"]).selectinload(Route.payment_methods),
            __import__("sqlalchemy.orm", fromlist=["selectinload"]).selectinload(Route.alerts),
            __import__("sqlalchemy.orm", fromlist=["selectinload"]).selectinload(Route.occupancy),
            __import__("sqlalchemy.orm", fromlist=["selectinload"]).selectinload(Route.path),
        )
    )
    routes = result.scalars().all()

    now = datetime.now(timezone.utc)

    return await build_trip_response(
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