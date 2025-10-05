from datetime import date, datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
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
    gasoline_type: Mapped[str] = mapped_column(nullable=False)
    cost_per_gallon: Mapped[float] = mapped_column(nullable=True)


class Vehicle(Base):
    __tablename__ = "vehicle"

    make: Mapped[str] = mapped_column(nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    average_mpg: Mapped[float] = mapped_column(nullable=True)
    fuel_type: Mapped[str] = mapped_column(nullable=False)

    def common_name(self):
        """
        Returns the name of the vehicle in natural language (e.g., "2002 Toyota
        Corolla") as a string
        """
        return f"{self.year} {self.make} {self.model}"


class FuelEfficiencyMonthly(Base):
    __tablename__ = "fuel_efficiency_monthly"

    duoarea: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    avg_cost_per_gallon: Mapped[float] = mapped_column(nullable=False)


class Economical(Base):
    __tablename__ = "economical"

    duoarea: Mapped[str] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)

    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=True)
    vehicle: Mapped["Vehicle"] = relationship()
