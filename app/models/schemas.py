from __future__ import annotations

from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class RouteStatus(str, Enum):
    active = "active"
    suspended = "suspended"
    seasonal = "seasonal"


class VehicleType(str, Enum):
    s14 = "14-seater"
    s32 = "32-seater"
    s52 = "52-seater"
    electric = "electric"


class OperatingStatus(str, Enum):
    active = "active"
    suspended = "suspended"
    seasonal = "seasonal"


class AliasType(str, Enum):
    abbreviation = "abbreviation"
    colloquial = "colloquial"
    former_name = "former_name"


class StageType(str, Enum):
    formal = "formal"
    informal = "informal"


class Direction(str, Enum):
    inbound = "inbound"
    outbound = "outbound"


class FareType(str, Enum):
    peak = "peak"
    off_peak = "off_peak"
    late_night = "late_night"
    weekend = "weekend"
    public_holiday = "public_holiday"


class PaymentMethod(str, Enum):
    cash = "cash"
    mpesa = "mpesa"
    tap = "tap"


class AlertType(str, Enum):
    short_loop = "short_loop"
    delayed = "delayed"
    suspended_temporary = "suspended_temporary"
    diversion = "diversion"


class CorrectionStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class CorridorCreate(BaseModel):
    name:        str = Field(..., max_length=100)
    description: Optional[str] = None
    is_active:   bool = True


class CorridorOut(CorridorCreate):
    id: UUID


class CorridorSurgeCreate(BaseModel):
    corridor_id:  UUID
    multiplier:   Decimal = Field(..., gt=1, le=5, decimal_places=2)
    reason:       str = Field(..., max_length=200)
    reason_sw:    Optional[str] = Field(None, max_length=200)
    triggered_by: str = Field(..., max_length=100)
    active_from:  datetime
    active_until: datetime

    @model_validator(mode="after")
    def check_dates(self) -> "CorridorSurgeCreate":
        if self.active_until <= self.active_from:
            raise ValueError("active_until must be after active_from")
        return self


class CorridorSurgeOut(CorridorSurgeCreate):
    id:         UUID
    is_active:  bool
    created_at: datetime


class SaccoCreate(BaseModel):
    name:             str = Field(..., max_length=100)
    vehicle_type:     VehicleType
    is_electric:      bool = False
    terminus_area:    Optional[str] = Field(None, max_length=100)
    operating_status: OperatingStatus = OperatingStatus.active
    safety_rating:    Optional[Decimal] = Field(
        None, ge=0, le=5, decimal_places=1)
    comfort_rating:   Optional[Decimal] = Field(
        None, ge=0, le=5, decimal_places=1)
    is_verified:      bool = False


class SaccoOut(SaccoCreate):
    id:               UUID
    last_confirmed_at: Optional[datetime]
    created_at:       datetime


class SaccoAliasCreate(BaseModel):
    sacco_id:   UUID
    alias:      str = Field(..., max_length=100)
    alias_type: AliasType


class SaccoAliasOut(SaccoAliasCreate):
    id: UUID


class StageCreate(BaseModel):
    name:        str = Field(..., max_length=150)
    area:        str = Field(..., max_length=100)
    landmark:    Optional[str] = Field(None, max_length=300)
    landmark_sw: Optional[str] = Field(None, max_length=300)
    stage_type:  StageType
    direction:   Direction
    latitude:    Decimal = Field(..., ge=-90,  le=90)
    longitude:   Decimal = Field(..., ge=-180, le=180)
    is_active:   bool = True


class StageOut(StageCreate):
    id: UUID


class StageHourCreate(BaseModel):
    stage_id:    UUID
    day_of_week: int = Field(..., ge=0, le=6)
    open_from:   time
    open_until:  time


class StageHourOut(StageHourCreate):
    id: UUID


class RouteCreate(BaseModel):
    sacco_id:                UUID
    corridor_id:             Optional[UUID] = None
    origin_stage_id:         UUID
    dest_stage_id:           UUID
    via_description:         Optional[str] = Field(None, max_length=200)
    via_description_sw:      Optional[str] = Field(None, max_length=200)
    distance_km:             Optional[Decimal] = Field(None, ge=0)
    is_express:              bool = False
    route_status:            RouteStatus = RouteStatus.active
    departure_frequency_mins: Optional[int] = Field(None, ge=1, le=120)
    avg_duration_mins:       Optional[int] = Field(None, ge=1)
    peak_duration_mins:      Optional[int] = Field(None, ge=1)


class RouteOut(RouteCreate):
    id:                   UUID
    fare_last_verified_at: Optional[datetime]
    last_confirmed_at:    Optional[datetime]
    created_at:           datetime


class RoutePathCreate(BaseModel):
    route_id:   UUID
    stage_id:   UUID
    stop_order: int = Field(..., ge=1)


class RoutePathOut(RoutePathCreate):
    id: UUID


class FareCreate(BaseModel):
    route_id:    UUID
    fare_type:   FareType
    day_type:    int = Field(..., ge=0, le=6)
    amount_kes:  int = Field(..., gt=0, le=5000)
    valid_from:  time
    valid_until: time


class FareOut(FareCreate):
    id: UUID


class PaymentMethodCreate(BaseModel):
    route_id: UUID
    method:   PaymentMethod


class PaymentMethodOut(PaymentMethodCreate):
    id: UUID


class StageMatch(BaseModel):
    id:         UUID
    name:       str
    area:       str
    stage_type: StageType
    landmark:   Optional[str]


class RouteResult(BaseModel):
    route_id:                UUID
    sacco_name:              str
    origin:                  str
    destination:             str
    via:                     Optional[str]
    is_express:              bool
    is_panya:                bool
    departure_frequency_mins: Optional[int]
    avg_duration_mins:       Optional[int]
    peak_fare_kes:           Optional[int]
    off_peak_fare_kes:       Optional[int]
    payment_methods:         list[str]
    route_status:            RouteStatus


class TransferResult(BaseModel):
    leg1: RouteResult
    leg2: RouteResult
    transfer_stage: str
    avg_wait_mins:  Optional[int]
    total_fare_kes: Optional[int]


class SearchResponse(BaseModel):
    direct_routes: list[RouteResult]
    transfers:     list[TransferResult]
    origin_resolved:      Optional[StageMatch]
    destination_resolved: Optional[StageMatch]


class RouteAlertCreate(BaseModel):
    route_id:     UUID
    alert_type:   AlertType
    message:      str
    message_sw:   Optional[str] = None
    triggered_by: str = Field(..., max_length=100)
    active_from:  datetime
    active_until: datetime

    @model_validator(mode="after")
    def check_dates(self) -> "RouteAlertCreate":
        if self.active_until <= self.active_from:
            raise ValueError("active_until must be after active_from")
        return self


class RouteAlertOut(RouteAlertCreate):
    id:         UUID
    is_active:  bool
    created_at: datetime


class FareCorrectionCreate(BaseModel):
    route_id:            UUID
    reported_amount_kes: int = Field(..., gt=0, le=5000)
    fare_type:           str = Field(..., max_length=50)
    device_fingerprint:  Optional[str] = Field(None, max_length=64)


class FareCorrectionOut(FareCorrectionCreate):
    id:          UUID
    reported_at: datetime
    status:      CorrectionStatus


class FareCorrectionReview(BaseModel):
    status: CorrectionStatus = Field(...,
                                     description="Must be 'accepted' or 'rejected'")

    @model_validator(mode="after")
    def not_pending(self) -> "FareCorrectionReview":
        if self.status == CorrectionStatus.pending:
            raise ValueError("Review status cannot be 'pending'")
        return self


class PublicHolidayCreate(BaseModel):
    name:         str = Field(..., max_length=100)
    holiday_date: date
    is_recurring: bool = True
    year:         Optional[int] = Field(None, ge=2000, le=2100)


class PublicHolidayOut(PublicHolidayCreate):
    id: UUID


class AppSettingUpsert(BaseModel):
    value:       str
    description: Optional[str] = None
    updated_by:  Optional[str] = Field(None, max_length=100)


class AppSettingOut(AppSettingUpsert):
    key:        str
    updated_at: Optional[datetime]


class MessageOut(BaseModel):
    message: str


class PaginatedMeta(BaseModel):
    total:  int
    limit:  int
    offset: int
