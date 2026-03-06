from pydantic import BaseModel, ConfigDict, Field
from typing import List
from app.matatus.schemas import MatatuBase, MatatuOut
from app.common_schemas import NewDestination


class RouteCreate(NewDestination):
    matatus: List[MatatuBase]


class RouteDetailOut(BaseModel):
    destination_id: int = Field(validation_alias="id")
    destination_name: str = Field(validation_alias="name")
    road_name: str
    matatus: List[MatatuOut]
    model_config = ConfigDict(from_attributes=True)
