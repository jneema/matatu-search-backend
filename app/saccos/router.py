import json
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.saccos.schemas import MatatuOut, MatatuCreate, SaccoCreate, SaccoOut
from app.saccos import service
from app.core.cloudinary import upload_image
import app.core.models as models

router = APIRouter(prefix="/saccos", tags=["saccos"])


@router.post("", response_model=SaccoOut)
async def create_sacco(payload: SaccoCreate, db: AsyncSession = Depends(get_db)):
    # Handles creating Sacco with or without Matatus
    return await service.create_sacco_and_fleet_logic(db, payload)


@router.post("/matatus", response_model=MatatuOut)
async def add_matatu(
    data: str = Form(...),
    stage_image: Optional[UploadFile] = File(None),
    matatu_image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
) -> MatatuOut: 
    payload = MatatuCreate(**json.loads(data))

    stage_url = await upload_image(stage_image, folder="matatus/stages") if stage_image else None
    matatu_url = await upload_image(matatu_image, folder="matatus/vehicles") if matatu_image else None

    matatu: models.Matatu = await service.add_matatu_standalone_logic(
        db, payload,
        stage_image_url=stage_url,
        matatu_image_url=matatu_url,
    )
    return MatatuOut.model_validate(matatu)  