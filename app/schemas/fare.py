from uuid import UUID
from pydantic import BaseModel
from app.models.fare import FareType, PaymentMethodType


class FareRead(BaseModel):
    id: UUID
    route_id: UUID
    fare_type: FareType
    day_type: int
    amount_kes: int
    valid_from: str
    valid_until: str

    model_config = {"from_attributes": True}


class FareCorrectionCreate(BaseModel):
    reported_amount_kes: int
    fare_type: FareType


class PaymentMethodRead(BaseModel):
    method: PaymentMethodType

    model_config = {"from_attributes": True}
