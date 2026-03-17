import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, Numeric, SmallInteger, DateTime, ForeignKey, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.sacco import Sacco
    from app.models.stage import Stage
    from app.models.fare import Fare, PaymentMethod
    from app.models.alert import RouteAlert, CorridorSurge
    from app.models.intelligence import Occupancy, FareCorrection


class RouteStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    SEASONAL = "seasonal"


class Corridor(Base, UUIDMixin):
    __tablename__ = "corridors"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    routes: Mapped[list["Route"]] = relationship("Route", back_populates="corridor")
    surges: Mapped[list["CorridorSurge"]] = relationship(
        "CorridorSurge", back_populates="corridor"
    )


class Route(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "routes"

    sacco_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("saccos.id"), nullable=False
    )
    corridor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("corridors.id"), nullable=True
    )
    origin_stage_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stages.id"), nullable=False
    )
    dest_stage_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stages.id"), nullable=False
    )
    via_description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    via_description_sw: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    distance_km: Mapped[Optional[float]] = mapped_column(Numeric(6, 2), nullable=True)
    is_express: Mapped[bool] = mapped_column(Boolean, default=False)
    route_status: Mapped[RouteStatus] = mapped_column(
        SAEnum(RouteStatus), nullable=False, default=RouteStatus.ACTIVE
    )
    departure_frequency_mins: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    avg_duration_mins: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    peak_duration_mins: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    fare_last_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_confirmed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    sacco: Mapped["Sacco"] = relationship("Sacco", back_populates="routes")
    corridor: Mapped[Optional["Corridor"]] = relationship(
        "Corridor", back_populates="routes"
    )
    origin_stage: Mapped["Stage"] = relationship(
        "Stage", foreign_keys=[origin_stage_id], back_populates="origin_routes"
    )
    dest_stage: Mapped["Stage"] = relationship(
        "Stage", foreign_keys=[dest_stage_id], back_populates="dest_routes"
    )
    path: Mapped[list["RoutePath"]] = relationship(
        "RoutePath", back_populates="route", order_by="RoutePath.stop_order"
    )
    fares: Mapped[list["Fare"]] = relationship("Fare", back_populates="route")
    payment_methods: Mapped[list["PaymentMethod"]] = relationship(
        "PaymentMethod", back_populates="route"
    )
    alerts: Mapped[list["RouteAlert"]] = relationship(
        "RouteAlert", back_populates="route"
    )
    occupancy: Mapped[list["Occupancy"]] = relationship(
        "Occupancy", back_populates="route"
    )
    corrections: Mapped[list["FareCorrection"]] = relationship(
        "FareCorrection", back_populates="route"
    )


class RoutePath(Base, UUIDMixin):
    __tablename__ = "route_paths"

    route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id"), nullable=False
    )
    stage_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stages.id"), nullable=False
    )
    stop_order: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    route: Mapped["Route"] = relationship("Route", back_populates="path")
    stage: Mapped["Stage"] = relationship("Stage")


class Transfer(Base, UUIDMixin):
    __tablename__ = "transfers"

    leg1_route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id"), nullable=False
    )
    leg2_route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id"), nullable=False
    )
    transfer_stage_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stages.id"), nullable=False
    )
    avg_wait_mins: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    total_fare_kes: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    leg1_route: Mapped["Route"] = relationship(
        "Route", foreign_keys=[leg1_route_id]
    )
    leg2_route: Mapped["Route"] = relationship(
        "Route", foreign_keys=[leg2_route_id]
    )
    transfer_stage: Mapped["Stage"] = relationship("Stage")