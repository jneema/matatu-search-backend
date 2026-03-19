import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, SmallInteger, Integer, Numeric, DateTime, Text, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.route import Route


class CorrectionStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Occupancy(Base, UUIDMixin):
    __tablename__ = "occupancy"

    route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id"), nullable=False
    )
    day_of_week: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    hour_slot: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    avg_load_factor: Mapped[float] = mapped_column(
        Numeric(3, 2), nullable=False)
    sample_count: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    route: Mapped["Route"] = relationship("Route", back_populates="occupancy")


class FareCorrection(Base, UUIDMixin):
    __tablename__ = "fare_corrections"

    route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id"), nullable=False
    )
    reported_amount_kes: Mapped[int] = mapped_column(
        SmallInteger, nullable=False)
    fare_type: Mapped[str] = mapped_column(String(50), nullable=False)
    reported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[CorrectionStatus] = mapped_column(
        SAEnum(CorrectionStatus), nullable=False, default=CorrectionStatus.PENDING
    )
    device_fingerprint: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )

    route: Mapped["Route"] = relationship(
        "Route", back_populates="corrections")


class SearchLog(Base, UUIDMixin):
    __tablename__ = "search_logs"

    origin_text: Mapped[str] = mapped_column(String(200), nullable=False)
    destination_text: Mapped[str] = mapped_column(String(200), nullable=False)
    resolved_origin_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    resolved_dest_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    result_count: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    had_transfer: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True)
    session_id: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True)
    queried_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )


class AppSettings(Base):
    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_by: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True)
