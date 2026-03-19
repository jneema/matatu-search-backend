from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.db.session import get_db
from app.models.alert import RouteAlert, CorridorSurge
from app.models.intelligence import FareCorrection
from app.schemas.alert import RouteAlertCreate, SurgeRead, SurgeCreate
from app.services.notification_service import notify_corridor_surge, notify_route_alert
from app.cache.decorators import cache_delete_pattern
from app.cache.keys import active_surges_key

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.post("/alerts")
async def create_alert(
    alert: RouteAlertCreate,
    db: AsyncSession = Depends(get_db),
):
    new_alert = RouteAlert(
        route_id=alert.route_id,
        alert_type=alert.alert_type,
        message=alert.message,
        message_sw=alert.message_sw,
        triggered_by="admin",
        active_from=alert.active_from,
        active_until=alert.active_until,
    )
    db.add(new_alert)
    await db.commit()
    await cache_delete_pattern("trip_search:*")
    await notify_route_alert(alert.route_id, alert.alert_type.value, alert.message, db)
    return {"status": "created"}


@router.post("/surges")
async def create_surge(
    surge: SurgeCreate,
    db: AsyncSession = Depends(get_db),
):
    new_surge = CorridorSurge(
        corridor_id=surge.corridor_id,
        multiplier=surge.multiplier,
        reason=surge.reason,
        reason_sw=surge.reason_sw,
        triggered_by="admin",
        active_from=surge.active_from,
        active_until=surge.active_until,
    )
    db.add(new_surge)
    await db.commit()
    await cache_delete_pattern("trip_search:*")
    await cache_delete_pattern(f"active_surges:{surge.corridor_id}*")
    await notify_corridor_surge(surge.corridor_id, surge.reason, db)
    return {"status": "created"}


@router.get("/corrections/pending")
async def pending_corrections(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FareCorrection).where(FareCorrection.status == "pending")
    )
    return result.scalars().all()