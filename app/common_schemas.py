from pydantic import BaseModel
from typing import Optional

# Input Schemas
class NewDestination(BaseModel):
    town: str
    road: str
    destination: str
    departure: str
    distance: Optional[str] = None
