import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, Numeric, DateTime, Text, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.route import Route, Corridor


class AlertType(str, enum.Enum):
    SHORT_LOOP = "short_loop"
    DELAYED = "delayed"
    SUSPENDED_TEMPORARY = "suspended_temporary"
    DIVERSION = "diversion"


class RouteAlert(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "route_alerts"

    route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id"), nullable=False
    )
    alert_type: Mapped[AlertType] = mapped_column(SAEnum(AlertType), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    message_sw: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    triggered_by: Mapped[str] = mapped_column(String(100), nullable=False)
    active_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    active_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    route: Mapped["Route"] = relationship("Route", back_populates="alerts")


class CorridorSurge(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "corridor_surges"

    corridor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("corridors.id"), nullable=False
    )
    multiplier: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)
    reason: Mapped[str] = mapped_column(String(200), nullable=False)
    reason_sw: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    triggered_by: Mapped[str] = mapped_column(String(100), nullable=False)
    active_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    active_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    corridor: Mapped["Corridor"] = relationship("Corridor", back_populates="surges")