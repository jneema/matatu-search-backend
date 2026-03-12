from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import app.core.models as models
from app.saccos.schemas import SaccoCreate, MatatuCreate
from typing import Optional


async def create_sacco_and_fleet_logic(db: AsyncSession, payload: SaccoCreate):
    # 1. Handle the Sacco (Parent)
    res = await db.execute(select(models.Sacco).where(models.Sacco.name == payload.name))
    sacco = res.scalar_one_or_none()

    if not sacco:
        sacco = models.Sacco(name=payload.name, contacts=payload.contacts)
        db.add(sacco)
        await db.flush()  # Get sacco.id

    # 2. Add Matatus (Children)
    if payload.matatus:
        for m in payload.matatus:
            new_matatu = models.Matatu(
                sacco_id=sacco.id,
                destination_id=m.destinationId,
                matatu_name=m.matatuName,
                matatu_number=m.matatuNumber,
                cbd_stage=m.cbdStage,
                estate_stage=m.estateStage,
                peak_fare_inbound=m.peakFareInbound,
                peak_fare_outbound=m.peakFareOutbound,
                off_peak_fare=m.offPeakFare,
                payment_methods=m.payment,
                is_express=m.isExpress,
                is_electric=m.isElectric,
                rating=m.rating or 0.0,
                contacts=m.contacts,
                notes=m.notes
            )
            db.add(new_matatu)

    await db.commit()
    await db.refresh(sacco)
    return sacco


async def add_matatu_standalone_logic(
    db: AsyncSession,
    payload: MatatuCreate,
    stage_image_url: Optional[str] = None,
    matatu_image_url: Optional[str] = None,
) -> models.Matatu: 
    new_matatu = models.Matatu(
        sacco_id=payload.sacco_id,
        destination_id=payload.destination_id,
        matatu_name=payload.matatuName,
        matatu_number=payload.matatuNumber,
        cbd_stage=payload.cbdStage,
        estate_stage=payload.estateStage,
        peak_fare_inbound=payload.peakFareInbound,
        peak_fare_outbound=payload.peakFareOutbound,
        off_peak_fare=payload.offPeakFare,
        payment_methods=payload.payment,
        is_express=payload.isExpress,
        is_electric=payload.isElectric,
        rating=payload.rating,
        contacts=payload.contacts,
        stage_image_url=stage_image_url,
        matatu_image_url=matatu_image_url,
        notes=payload.notes,
    )
    db.add(new_matatu)
    await db.commit()
    await db.refresh(new_matatu)
    return new_matatu