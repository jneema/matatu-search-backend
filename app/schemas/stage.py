from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.models.stage import StageType, Direction


class StageBase(BaseModel):
    name: str
    area: str
    landmark: Optional[str] = None
    landmark_sw: Optional[str] = None
    stage_type: StageType
    direction: Direction
    latitude: float
    longitude: float


class StageRead(StageBase):
    id: UUID
    is_active: bool

    model_config = {"from_attributes": True}


class StageNearby(BaseModel):
    lat: float
    lng: float
    radius_m: float = 500.0


class StageResolveResult(BaseModel):
    stage: StageRead
    match_confidence: str
    score: float