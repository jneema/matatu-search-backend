from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.models.sacco import VehicleType, OperatingStatus


class SaccoBase(BaseModel):
    name: str
    vehicle_type: VehicleType
    is_electric: bool = False
    terminus_area: Optional[str] = None
    operating_status: OperatingStatus = OperatingStatus.ACTIVE
    safety_rating: Optional[float] = None
    comfort_rating: Optional[float] = None


class SaccoRead(SaccoBase):
    id: UUID
    is_verified: bool

    model_config = {"from_attributes": True}


class SaccoRating(BaseModel):
    type: str
    score: float