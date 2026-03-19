import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.route import Route


class VehicleType(str, enum.Enum):
    SEATER_14 = "14-seater"
    SEATER_32 = "32-seater"
    SEATER_52 = "52-seater"
    ELECTRIC = "electric"


class OperatingStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    SEASONAL = "seasonal"


class AliasType(str, enum.Enum):
    ABBREVIATION = "abbreviation"
    COLLOQUIAL = "colloquial"
    FORMER_NAME = "former_name"


class Sacco(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "saccos"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    vehicle_type: Mapped[VehicleType] = mapped_column(
        SAEnum(VehicleType), nullable=False)
    is_electric: Mapped[bool] = mapped_column(Boolean, default=False)
    terminus_area: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True)
    operating_status: Mapped[OperatingStatus] = mapped_column(
        SAEnum(OperatingStatus), nullable=False, default=OperatingStatus.ACTIVE
    )
    safety_rating: Mapped[Optional[float]] = mapped_column(
        Numeric(2, 1), nullable=True)
    comfort_rating: Mapped[Optional[float]] = mapped_column(
        Numeric(2, 1), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_confirmed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    routes: Mapped[list["Route"]] = relationship(
        "Route", back_populates="sacco")
    aliases: Mapped[list["SaccoAlias"]] = relationship(
        "SaccoAlias", back_populates="sacco"
    )


class SaccoAlias(Base, UUIDMixin):
    __tablename__ = "sacco_aliases"

    sacco_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("saccos.id"), nullable=False
    )
    alias: Mapped[str] = mapped_column(String(100), nullable=False)
    alias_type: Mapped[AliasType] = mapped_column(
        SAEnum(AliasType), nullable=False)

    sacco: Mapped["Sacco"] = relationship("Sacco", back_populates="aliases")
