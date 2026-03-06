from pydantic import BaseModel, ConfigDict
from typing import List


class NewRoad(BaseModel):
    town: str
    road: str


class RoadOut(BaseModel):
    id: int
    name: str
    town_id: int
    model_config = ConfigDict(from_attributes=True)


class BulkRoadsCreate(BaseModel):
    town: str
    roads: List[str]
