from typing import List, Optional
from sqlalchemy import ForeignKey, JSON, Text, Table, Column,  Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
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


class Sacco(Base):
    __tablename__ = "saccos"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    contacts: Mapped[Optional[str]] = mapped_column(nullable=True)

    matatus: Mapped[List["Matatu"]] = relationship(
        "Matatu", back_populates="sacco")


class Matatu(Base):
    __tablename__ = "matatus"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.id"))
    sacco_id: Mapped[int] = mapped_column(ForeignKey("saccos.id"))
    matatu_name: Mapped[Optional[str]]
    matatu_number: Mapped[Optional[str]]
    cbd_stage: Mapped[str]
    estate_stage: Mapped[str]
    peak_fare_inbound: Mapped[int]
    peak_fare_outbound: Mapped[int]
    off_peak_fare: Mapped[int]
    is_express: Mapped[bool] = mapped_column(default=False)
    is_electric: Mapped[bool] = mapped_column(default=False)
    payment_methods: Mapped[List[str]] = mapped_column(JSON)
    rating: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    contacts: Mapped[Optional[str]]
    notes: Mapped[Optional[str]] = mapped_column(Text)
    stage_image_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    matatu_image_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    destination: Mapped["Destination"] = relationship(
        "Destination", back_populates="matatus")
    sacco: Mapped["Sacco"] = relationship("Sacco", back_populates="matatus")
