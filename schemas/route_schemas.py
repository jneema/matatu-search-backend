from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

#Input Schemas
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

class NewDestination(BaseModel):
    town: str
    road: str
    destination: str
    departure: str
    distance: Optional[str] = None

class RouteCreate(NewDestination):
    matatus: List[MatatuBase]

class NewRoad(BaseModel):
    town: str
    road: str

#Output Schemas
class TownOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class RoadOut(BaseModel):
    id: int
    name: str
    town_id: int
    model_config = ConfigDict(from_attributes=True)

class DestinationOut(BaseModel):
    id: int
    name: str
    departure: str
    distance: Optional[str]
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

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

class RouteDetailOut(BaseModel):
    destination_id: int = Field(validation_alias="id")
    destination_name: str = Field(validation_alias="name")
    road_name: str
    matatus: List[MatatuOut]
    model_config = ConfigDict(from_attributes=True)

#Bulk Schemas
class BulkRoadsCreate(BaseModel):
    town: str
    roads: List[str]

class BulkDestinationsCreate(BaseModel):
    town: str
    road: str
    destinations: List[RouteCreate]