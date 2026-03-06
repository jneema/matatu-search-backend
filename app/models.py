from typing import List, Optional
from sqlalchemy import ForeignKey, JSON, Text, Table, Column,  Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy.sql.schema import Table as SATable

road_destination_association: SATable = Table(
    "road_destination",
    Base.metadata,
    Column("road_id", Integer, ForeignKey(
        "roads.id", ondelete="CASCADE"), primary_key=True),
    Column("destination_id", Integer, ForeignKey(
        "destinations.id", ondelete="CASCADE"), primary_key=True),
)


class Town(Base):
    __tablename__ = "towns"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    roads: Mapped[List["Road"]] = relationship(
        "Road", back_populates="town", cascade="all, delete-orphan")


class Road(Base):
    __tablename__ = "roads"
    id: Mapped[int] = mapped_column(primary_key=True)
    town_id: Mapped[int] = mapped_column(ForeignKey("towns.id"))
    name: Mapped[str] = mapped_column(index=True)

    town: Mapped["Town"] = relationship("Town", back_populates="roads")
    destinations: Mapped[List["Destination"]] = relationship(
        "Destination", secondary=road_destination_association, back_populates="roads"
    )


class Destination(Base):
    __tablename__ = "destinations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    departure: Mapped[str]  # General area (e.g. "CBD")
    distance: Mapped[Optional[str]] = mapped_column(nullable=True)

    roads: Mapped[List["Road"]] = relationship(
        "Road", secondary=road_destination_association, back_populates="destinations"
    )
    matatus: Mapped[List["Matatu"]] = relationship(
        "Matatu", back_populates="destination", cascade="all, delete-orphan")


class Matatu(Base):
    __tablename__ = "matatus"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.id"))

    sacco_name: Mapped[str]
    matatu_name: Mapped[Optional[str]]  # The "Nganya" name
    matatu_number: Mapped[Optional[str]]  # Plate or Side No.

    # Specific Stage Logic
    cbd_stage: Mapped[str]      # e.g., "Ambassadeur", "Railways"
    estate_stage: Mapped[str]   # e.g., "Maasai Lodge"

    # Fare & Service Logic
    peak_fare_inbound: Mapped[int]
    peak_fare_outbound: Mapped[int]
    off_peak_fare: Mapped[int]
    is_express: Mapped[bool] = mapped_column(default=False)
    is_electric: Mapped[bool] = mapped_column(default=False)

    payment_methods: Mapped[List[str]] = mapped_column(JSON)
    rating: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    contacts: Mapped[Optional[str]] = mapped_column(nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True)  # Tips/Alerts

    destination: Mapped["Destination"] = relationship(
        "Destination", back_populates="matatus")
