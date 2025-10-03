from database.models import AnnualMiles
from etl.shared import get_logger, load_table


def run_annual_miles_etl(logger=get_logger()):
    """
    Reads in annual miles data from the provided CSV, cleans as needed, and loads to
    database according to the AnnualMiles model
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

    logger.info(f"Read in {len(lines)} lines from {SOURCE_FILENAME}")

    file_headers = [header.strip() for header in lines[0].split(",")]
    rows = [
        _clean_annual_mile_line(headers=file_headers, raw_line=line)
        for line in lines[1:]
    ]

    logger.info(f"Successfully cleaned all data from {SOURCE_FILENAME}. Loading...")

    load_table(table=TABLE, records=rows, logger=logger)
