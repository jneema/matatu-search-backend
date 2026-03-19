from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.db.session import get_db
from app.models.intelligence import FareCorrection
from app.schemas.fare import FareCorrectionCreate
from app.models.route import Route
from uuid import UUID
from fastapi import HTTPException

router = APIRouter(prefix="/api/v1/routes", tags=["corrections"])


@router.post("/{route_id}/fare-correction")
async def submit_correction(
    route_id: UUID,
    correction: FareCorrectionCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    # Verify the route exists before inserting — prevents a FK violation 500
    # and returns a clean 404 to the caller instead.
    route = await db.get(Route, route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")

    fingerprint = request.headers.get("X-Device-Fingerprint")
    new_correction = FareCorrection(
        route_id=route_id,
        reported_amount_kes=correction.reported_amount_kes,
        fare_type=correction.fare_type.value,
        reported_at=datetime.now(timezone.utc),
        device_fingerprint=fingerprint,
    )
    db.add(new_correction)
    await db.commit()
    return {"status": "submitted"}
