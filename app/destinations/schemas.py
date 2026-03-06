from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.routes.schemas import RouteCreate


# Output Schemas
class DestinationOut(BaseModel):
    id: int
    name: str
    departure: str
    distance: Optional[str]
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# Bulk Schemas
class BulkDestinationsCreate(BaseModel):
    town: str
    road: str
    destinations: List[RouteCreate]
