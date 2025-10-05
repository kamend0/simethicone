import logging
import marshal
import pickle
import types

from sqlalchemy.orm import Session

from src.database.models import AnnualMiles, Economical, FuelEfficiencyMonthly, Vehicle

with open("src/api/model.pkl", "rb") as fh:
    serialized_data = pickle.load(fh)
    code_obj = marshal.loads(serialized_data["code"])
    predict = types.FunctionType(
        code_obj, globals(), serialized_data["name"], serialized_data["defaults"]
    )


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger


def memoize_most_economical(
    most_economical: Economical,
    db: Session,
) -> Economical:
    """
    Creates an Economical object and loads it to the database; returns the refreshed
    object instance.
    """
    db.add(most_economical)
    db.commit()
    db.refresh(most_economical)

    return most_economical


def calc_most_economical(
    duoarea: str, month: int, year: int, db: Session
) -> Economical:
    """
    Calculate the most economical vehicle to drive given the parameters. Once
    calculated, whether a valid vehicle is found or no calculation can be done, the
    result is memoized (written to the Economical table).
    Returns the Economical record, which might have no Vehicle relation, and thus was
    not calculable.
    """
    most_economical = Economical(duoarea=duoarea, year=year, month=month)

    logging.info(
        f"Calculating most economical vehicle for {duoarea} - {year} - {month}"
    )
    # First, we get the average miles driven per year, which we currently can only
    # determine via the duoarea
    logging.info("Getting average annual miles driven...")
    avg_annual_miles_driven = (
        db.query(AnnualMiles).filter(AnnualMiles.duoarea == duoarea).first()
    )
    if avg_annual_miles_driven is None:
        logging.info(f"No average annual miles data for {duoarea} - {year} - {month}")
        return memoize_most_economical(most_economical=most_economical, db=db)

    # Next we need the average cost of gas for the area and time period
    logging.info("Getting average fuel cost...")
    monthly_fuel_efficiency = (
        db.query(FuelEfficiencyMonthly)
        .filter(
            FuelEfficiencyMonthly.duoarea == duoarea,
            FuelEfficiencyMonthly.year == year,
            FuelEfficiencyMonthly.month == month,
        )
        .first()
    )
    if monthly_fuel_efficiency is None:
        logging.info(f"No average fuel cost data for {duoarea} - {year} - {month}")
        return memoize_most_economical(most_economical=most_economical, db=db)

    # Now, for every car with a model year equal to or less than the queried year (we
    # won't get into the minutiae of whether they were released by this point beyond
    # this check), we calculate what their fuel cost would be
    logging.info("Calculating most economical vehicle...")
    vehicles = (
        db.query(Vehicle)
        .filter(Vehicle.year <= year, Vehicle.average_mpg.isnot(None))
        .all()
    )

    if not vehicles:
        logging.info(f"No vehicle data available for {year} - {month}")
        return memoize_most_economical(most_economical=most_economical, db=db)

    annual_costs = {
        vehicle.id: predict(
            annual_miles=avg_annual_miles_driven.miles,
            combined_mpg=vehicle.average_mpg,
            fuel_price=monthly_fuel_efficiency.avg_cost_per_gallon,
            vehicle_year=vehicle.year,
        )
        for vehicle in vehicles
    }
    annual_costs = {k: v for k, v in annual_costs.items() if v is not None}

    # The most economical vehicle is the one with the minimum annual cost; if there's a
    # tie, we just get the first one in the sequence
    most_economical_vehicle_id = min(annual_costs, key=annual_costs.get)

    logging.info(
        f"Most economical vehicle found: {most_economical_vehicle_id}. Saving to db..."
    )
    most_economical.vehicle_id = most_economical_vehicle_id

    return memoize_most_economical(most_economical=most_economical, db=db)


def get_most_economical_memoized(
    duoarea: str, month: int, year: int, db: Session
) -> Economical:
    """
    Based on the parameters (which should mirror those in the /economical endpoint),
    checks the database for an existing entry; if none, computes it, then writes it
    to that table for memoization and faster future lookup
    Returns the year, make, and model of the vehicle as a string
    """
    most_economical = (
        db.query(Economical)
        .filter(
            Economical.duoarea == duoarea,
            Economical.year == year,
            Economical.month == month,
        )
        .first()
    )

    if most_economical is None:
        logging.info(
            f"No pre-calced economical vehicle found for {duoarea} - {year} - {month}. Calculating..."
        )
        most_economical = calc_most_economical(
            duoarea=duoarea, year=year, month=month, db=db
        )

    return most_economical
