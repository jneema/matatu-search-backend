from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

# Input Schemas
class MatatuBase(BaseModel):
    saccoName: str
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


# Output Schemas
class MatatuOut(BaseModel):
    id: int
    sacco_name: str
    matatu_name: Optional[str]
    cbd_stage: str
    estate_stage: str
    peak_fare_inbound: int
    peak_fare_outbound: int
    off_peak_fare: int
    is_express: bool
    is_electric: bool
    payment: List[str] = Field(validation_alias="payment_methods")
    rating: Optional[float] = 0.0  # allow None
    contacts: Optional[str]
    notes: Optional[str]
    model_config = ConfigDict(from_attributes=True)
