from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.sacco import Sacco
from app.models.route import Route, RouteStatus
from app.schemas.sacco import SaccoRead, SaccoRating

router = APIRouter(prefix="/api/v1/saccos", tags=["saccos"])


@router.get("", response_model=list[SaccoRead])
async def list_saccos(
    is_electric: bool | None = Query(None),
    vehicle_type: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Sacco).where(Sacco.operating_status == "active")
    if is_electric is not None:
        query = query.where(Sacco.is_electric == is_electric)
    if vehicle_type:
        query = query.where(Sacco.vehicle_type == vehicle_type)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{sacco_id}/routes")
async def get_sacco_routes(sacco_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Route).where(
            Route.sacco_id == sacco_id,
            Route.route_status == RouteStatus.ACTIVE,
        )
    )
    return result.scalars().all()


@router.post("/{sacco_id}/rating")
async def rate_sacco(
    sacco_id: str,
    rating: SaccoRating,
    db: AsyncSession = Depends(get_db),
):
    sacco = await db.get(Sacco, sacco_id)
    if not sacco:
        raise HTTPException(status_code=404, detail="Sacco not found")

    if rating.type == "safety":
        current = float(sacco.safety_rating or 0)
        sacco.safety_rating = round((current + rating.score) / 2, 1)
    elif rating.type == "comfort":
        current = float(sacco.comfort_rating or 0)
        sacco.comfort_rating = round((current + rating.score) / 2, 1)
    else:
        raise HTTPException(status_code=422, detail="type must be 'safety' or 'comfort'")

    await db.commit()
    return {"status": "ok"}