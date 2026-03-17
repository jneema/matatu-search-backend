import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, SmallInteger, Boolean, Date, Time, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import Base, UUIDMixin
from datetime import date

if TYPE_CHECKING:
    from app.models.route import Route


class FareType(str, enum.Enum):
    PEAK = "peak"
    OFF_PEAK = "off_peak"
    LATE_NIGHT = "late_night"
    WEEKEND = "weekend"
    PUBLIC_HOLIDAY = "public_holiday"


class PaymentMethodType(str, enum.Enum):
    CASH = "cash"
    MPESA = "mpesa"
    TAP = "tap"


class Fare(Base, UUIDMixin):
    __tablename__ = "fares"

    route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id"), nullable=False
    )
    fare_type: Mapped[FareType] = mapped_column(SAEnum(FareType), nullable=False)
    day_type: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    amount_kes: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    valid_from: Mapped[str] = mapped_column(Time, nullable=False)
    valid_until: Mapped[str] = mapped_column(Time, nullable=False)

    route: Mapped["Route"] = relationship("Route", back_populates="fares")


class PaymentMethod(Base, UUIDMixin):
    __tablename__ = "payment_methods"

    route_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id"), nullable=False
    )
    method: Mapped[PaymentMethodType] = mapped_column(
        SAEnum(PaymentMethodType), nullable=False
    )

    route: Mapped["Route"] = relationship("Route", back_populates="payment_methods")


class PublicHoliday(Base, UUIDMixin):
    __tablename__ = "public_holidays"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    holiday_date: Mapped[date] = mapped_column(Date, nullable=False, unique=True)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=True)
    year: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)