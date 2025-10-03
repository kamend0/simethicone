"""
Various functions to retrieve, read, parse, clean, and load data integral to the
Simethicone database
"""

import logging

from sqlalchemy import insert
from sqlalchemy.sql.schema import Table

from database.connector import get_engine
from database.models import AnnualMiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def load_table(table: Table, records: list[dict]):
    """
    Attempts to load the provided records to the specified table; does not create the
    table or modify schema, and assumes data is prepped to adhere to table schema.
    No return value, relies on sqlalchemy's execute() to raise applicable errors
    """
    engine = get_engine()
    with engine.begin() as conn:
        logger.info(f"Beginning load of {len(records)} records to table {table.name}")
        conn.execute(insert(table), records)
        logger.info(f"Successfully loaded {len(records)} records to table {table.name}")


def run_annual_miles_etl():
    """
    Loads, transforms, and loads annual miles data, which is read in from a static
    CSV file provided in project documentation
    """
    TABLE = AnnualMiles.__table__
    SOURCE_FILENAME = "data/annual_miles.csv"

    def _clean_annual_mile_line(headers: list[str], raw_line: str) -> tuple[str]:
        """
        Given a raw line from the annual_miles.csv file, return the three values we
        expect cleaned and extracted from the line: state, duoarea, and miles.
        """
        # Leading and trailing characters: remove both whitespace AND commas, the latter
        # in particular throws off any interpretation of the CSV data
        line = raw_line.strip().strip(",").strip('"')

        # Some happen to be tab-separated; replace with commas
        line = line.replace("\t", ",")

        line_elements = [el.strip() for el in line.split(",") if el]  # non-empty only

        # The last two elements are always duoarea and miles, but states can have
        # multi-word names
        state = " ".join(line_elements[:-2])
        duoarea = line_elements[-2]
        miles = int(line_elements[-1])

        return dict(zip(headers, [state, duoarea, miles]))

    with open(file=SOURCE_FILENAME, mode="r") as file:
        lines = [line for line in file]

    file_headers = [header.strip() for header in lines[0].split(",")]
    rows = [
        _clean_annual_mile_line(headers=file_headers, raw_line=line)
        for line in lines[1:]
    ]

    load_table(table=TABLE, records=rows)


if __name__ == "__main__":
    run_annual_miles_etl()
