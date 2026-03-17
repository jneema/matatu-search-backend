from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.db.session import get_db
from app.models.intelligence import FareCorrection
from app.schemas.fare import FareCorrectionCreate

router = APIRouter(prefix="/api/v1/routes", tags=["corrections"])


@router.post("/{route_id}/fare-correction")
async def submit_correction(
    route_id: str,
    correction: FareCorrectionCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
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