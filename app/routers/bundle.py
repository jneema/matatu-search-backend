from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.bundle_service import build_corridor_bundle

router = APIRouter(prefix="/api/v1/bundle", tags=["bundle"])


@router.get("/{corridor_id}")
async def get_bundle(corridor_id: str, db: AsyncSession = Depends(get_db)):
    return await build_corridor_bundle(corridor_id, db)