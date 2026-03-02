from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class MatatuBase(BaseModel):
    saccoName: str
    matatuName: str
    matatuNumber: Optional[str] = None
    stageLocationDestination: str
    stageLocationDeparture: Optional[str] = None
    payment: List[str]
    dropoffs: str
    peakFare: int
    offPeakFare: int
    type: str
    rating: Optional[float] = None
    contacts: Optional[str] = None

class RouteCreate(BaseModel):
    town: str = "Nairobi"
    road: str
    destination: str
    departure: str
    distance: Optional[str] = None
    comments: Optional[str] = None
    matatus: List[MatatuBase]

class TownOut(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class RoadOut(BaseModel):
    name: str 
    model_config = ConfigDict(from_attributes=True)

class DestinationOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
    
class MatatuOut(BaseModel):
    sacco_name: str
    matatu_name: str
    peak_fare: int
    off_peak_fare: int
    payment_methods: List[str]
    model_config = ConfigDict(from_attributes=True)

class RouteDetailOut(BaseModel):
    id: int
    road: str
    destination: str
    departure: str
    distance: Optional[str]
    matatus: List[MatatuOut]
    model_config = ConfigDict(from_attributes=True)