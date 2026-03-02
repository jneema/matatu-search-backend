from typing import List
from sqlalchemy import ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Town(Base):
    __tablename__ = "towns"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    roads: Mapped[List["Road"]] = relationship("Road", back_populates="town", cascade="all, delete-orphan")

class Road(Base):
    __tablename__ = "roads"
    id: Mapped[int] = mapped_column(primary_key=True)
    town_id: Mapped[int] = mapped_column(ForeignKey("towns.id"))
    name: Mapped[str] = mapped_column(index=True)
    town: Mapped["Town"] = relationship("Town", back_populates="roads")
    destinations: Mapped[List["Destination"]] = relationship("Destination", back_populates="road", cascade="all, delete-orphan")

class Destination(Base):
    __tablename__ = "destinations"
    id: Mapped[int] = mapped_column(primary_key=True)
    road_id: Mapped[int] = mapped_column(ForeignKey("roads.id"))
    name: Mapped[str] = mapped_column(index=True)
    departure: Mapped[str]
    distance: Mapped[str | None] = mapped_column(nullable=True)
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    road: Mapped["Road"] = relationship("Road", back_populates="destinations")
    matatus: Mapped[List["Matatu"]] = relationship("Matatu", back_populates="destination", cascade="all, delete-orphan")

class Matatu(Base):
    __tablename__ = "matatus"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.id"))
    sacco_name: Mapped[str]
    matatu_name: Mapped[str]
    matatu_number: Mapped[str | None] = mapped_column(nullable=True)
    stage_destination: Mapped[str]
    stage_departure: Mapped[str | None] = mapped_column(nullable=True)
    payment_methods: Mapped[List[str]] = mapped_column(JSON)
    dropoffs: Mapped[str]
    peak_fare: Mapped[int]
    off_peak_fare: Mapped[int]
    matatu_type: Mapped[str]
    rating: Mapped[float | None] = mapped_column(nullable=True)
    contacts: Mapped[str | None] = mapped_column(nullable=True)
    destination: Mapped["Destination"] = relationship("Destination", back_populates="matatus")