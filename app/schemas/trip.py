from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.models.sacco import VehicleType
from app.schemas.alert import RouteAlertRead


class StageEmbed(BaseModel):
    id: UUID
    name: str
    area: str
    landmark: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    direction: str

    class Config:
        from_attributes = True


class TransferDetail(BaseModel):
    transfer_stage: str
    avg_wait_mins: Optional[int] = None
    leg1_sacco: str
    leg2_sacco: str


class TripOption(BaseModel):
    route_id: UUID
    sacco: str
    vehicle_type: VehicleType
    via: Optional[str] = None
    terminus_area: Optional[str] = None
    fare: int
    fare_type_now: str
    off_peak_fare: Optional[int] = None
    peak_fare: Optional[int] = None
    is_off_peak_now: bool
    duration_mins: Optional[int] = None
    wait_mins_est: Optional[int] = None
    payment_methods: list[str]
    safety_rating: Optional[float] = None
    comfort_rating: Optional[float] = None
    likely_full: bool = False
    tags: list[str]
    data_confidence: str
    surge_active: bool = False
    surge_reason: Optional[str] = None
    active_alerts: list[RouteAlertRead] = []
    is_transfer: bool = False
    transfer_detail: Optional[TransferDetail] = None
    origin_stage: Optional[StageEmbed] = None
    dest_stage: Optional[StageEmbed] = None


class TripSearchRequest(BaseModel):
    origin: str
    destination: str
    depart_after: Optional[str] = None
    budget_kes: Optional[int] = None
    payment_preference: Optional[str] = None
    user_lat: Optional[float] = None
    user_lng: Optional[float] = None
    include_transfers: bool = True


class TripResponse(BaseModel):
    trip: str
    queried_at: str
    origin_stages: list[str]
    dest_stages: list[str]
    scenarios: dict[str, list[TripOption]]
    all_options: list[TripOption]