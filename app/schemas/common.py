from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int


class ErrorResponse(BaseModel):
    error: str
    message: str
    suggestions: Optional[list[str]] = None


class HealthStatus(BaseModel):
    status: str
    database: Optional[str] = None
    redis: Optional[str] = None