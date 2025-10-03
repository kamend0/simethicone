from datetime import date, datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


class AnnualMiles(Base):
    __tablename__ = "annual_miles"

    duoarea: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(nullable=False)
    miles: Mapped[int] = mapped_column(nullable=False)


class FuelEfficiency(Base):
    __tablename__ = "fuel_efficiency"

    duoarea: Mapped[str] = mapped_column(nullable=False)
    period: Mapped[date] = mapped_column(nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[float] = mapped_column()


class Vehicle(Base):
    __tablename__ = "vehicle"

    make: Mapped[str] = mapped_column(nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    comb08u: Mapped[float] = mapped_column(nullable=False)
    fueltype1: Mapped[str] = mapped_column(nullable=False)
