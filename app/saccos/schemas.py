from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class SaccoBase(BaseModel):
    name: str
    contacts: Optional[str] = None


class MatatuBase(BaseModel):
    saccoName: str
    destinationId: int
    matatuName: Optional[str] = None
    matatuNumber: Optional[str] = None
    cbdStage: str
    estateStage: str
    peakFareInbound: int
    peakFareOutbound: int
    offPeakFare: int
    payment: List[str]
    isExpress: bool = False
    isElectric: bool = False
    rating: Optional[float] = 0.0
    contacts: Optional[str] = None
    notes: Optional[str] = None


class SaccoCreate(SaccoBase):
    matatus: Optional[List[MatatuBase]] = None


class MatatuCreate(MatatuBase):
    sacco_id: int
    destination_id: int

    stage_image_url: Optional[str] = None
    matatu_image_url: Optional[str] = None


class SaccoOut(SaccoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MatatuOut(BaseModel):
    id: int
    sacco: "SaccoOut"
    matatu_name: Optional[str]
    cbd_stage: str
    estate_stage: str
    destination_id: int = Field(serialization_alias="destinationId")
    peak_fare_inbound: int
    peak_fare_outbound: int
    off_peak_fare: int
    is_express: bool
    is_electric: bool
    payment: List[str] = Field(validation_alias="payment_methods")
    rating: Optional[float] = 0.0
    contacts: Optional[str]
    notes: Optional[str]
    stage_image_url: Optional[str] = None   
    matatu_image_url: Optional[str] = None  
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
