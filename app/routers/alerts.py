from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.db.session import get_db
from app.models.alert import RouteAlert, CorridorSurge
from app.schemas.alert import RouteAlertRead, SurgeRead

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])


@router.get("", response_model=list[RouteAlertRead])
async def list_alerts(
    db: AsyncSession = Depends(get_db),
):
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(RouteAlert).where(
            RouteAlert.is_active == True,
            RouteAlert.active_from <= now,
            RouteAlert.active_until >= now,
        )
    )
    return result.scalars().all()


@router.get("/surges", response_model=list[SurgeRead])
async def list_surges(db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(CorridorSurge).where(
            CorridorSurge.is_active == True,
            CorridorSurge.active_from <= now,
            CorridorSurge.active_until >= now,
        )
    )
    return result.scalars().all()


@router.get("/routes/{route_id}", response_model=list[RouteAlertRead])
async def get_route_alerts(route_id: str, db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(RouteAlert).where(
            RouteAlert.route_id == route_id,
            RouteAlert.is_active == True,
            RouteAlert.active_from <= now,
            RouteAlert.active_until >= now,
        )
    )
    return result.scalars().all()