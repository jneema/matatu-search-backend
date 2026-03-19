import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, Numeric, SmallInteger, Time, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.route import Route


class StageType(str, enum.Enum):
    FORMAL = "formal"
    INFORMAL = "informal"


class Direction(str, enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BOTH = "both"


class Stage(Base, UUIDMixin):
    __tablename__ = "stages"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    area: Mapped[str] = mapped_column(String(100), nullable=False)
    landmark: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    landmark_sw: Mapped[Optional[str]] = mapped_column(
        String(300), nullable=True)
    stage_type: Mapped[StageType] = mapped_column(
        SAEnum(StageType), nullable=False)
    direction: Mapped[Direction] = mapped_column(
        SAEnum(Direction), nullable=False)
    latitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)
    longitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    hours: Mapped[list["StageHours"]] = relationship(
        "StageHours", back_populates="stage"
    )
    origin_routes: Mapped[list["Route"]] = relationship(
        "Route", foreign_keys="Route.origin_stage_id", back_populates="origin_stage"
    )
    dest_routes: Mapped[list["Route"]] = relationship(
        "Route", foreign_keys="Route.dest_stage_id", back_populates="dest_stage"
    )


class StageHours(Base, UUIDMixin):
    __tablename__ = "stage_hours"

    stage_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stages.id"), nullable=False
    )
    day_of_week: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    open_from: Mapped[str] = mapped_column(Time, nullable=False)
    open_until: Mapped[str] = mapped_column(Time, nullable=False)

    stage: Mapped["Stage"] = relationship("Stage", back_populates="hours")
