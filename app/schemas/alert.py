from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.models.alert import AlertType


class RouteAlertRead(BaseModel):
    id: UUID
    route_id: UUID
    alert_type: AlertType
    message: str
    message_sw: Optional[str] = None
    triggered_by: str
    active_from: datetime
    active_until: datetime
    is_active: bool

    model_config = {"from_attributes": True}


class RouteAlertCreate(BaseModel):
    route_id: UUID
    alert_type: AlertType
    message: str
    message_sw: Optional[str] = None
    active_from: datetime
    active_until: datetime


class SurgeRead(BaseModel):
    id: UUID
    corridor_id: UUID
    multiplier: float
    reason: str
    reason_sw: Optional[str] = None
    triggered_by: str
    active_from: datetime
    active_until: datetime
    is_active: bool

    model_config = {"from_attributes": True}


class SurgeCreate(BaseModel):
    corridor_id: UUID
    multiplier: float
    reason: str
    reason_sw: Optional[str] = None
    active_from: datetime
    active_until: datetime