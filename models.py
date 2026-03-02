from typing import List
from sqlalchemy import ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    road: Mapped[str] = mapped_column(index=True)
    destination: Mapped[str] = mapped_column(index=True)
    town: Mapped[str] = mapped_column(default="Nairobi", index=True)
    departure: Mapped[str]
    distance: Mapped[str | None] = mapped_column(nullable=True)
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)

    matatus: Mapped[list["Matatu"]] = relationship("Matatu", back_populates="route", cascade="all, delete-orphan")

    @property
    def name(self) -> str:
        return self.destination

    @property
    def description(self) -> str:
        return f"Via {self.road}"

class Matatu(Base):
    __tablename__ = "matatus"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))
    
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

    route: Mapped["Route"] = relationship("Route", back_populates="matatus")