import pandas as pd

from src.database.models import Vehicle
from src.etl.utils import get_logger, get_with_exp_retry, load_table


def run_vehicle_data_etl(logger=get_logger(), redownload: bool = False):
    """
    Retrieves vehicle data from the OpenDataSoft URL, saves to disk, then reads into a
    Pandas DataFrame for cleaning/transformations, and loads.
    use_local: boolean flag to use data already downloaded rather than re-downloading it
    """
    TABLE = Vehicle.__table__
    SOURCE_URL = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/exports/parquet"

    if redownload:
        logger.info(f"Downloading vehicle data from {SOURCE_URL}...")
        response = get_with_exp_retry(url=SOURCE_URL)
        with open("data/vehicle_data.parquet", "wb") as file:
            file.write(response.content)

    logger.info("Data downloaded and written to disk. Performing transformations...")
    df = pd.read_parquet(path="data/vehicle_data.parquet")
    ff = df.copy()  # Perform all transformations on a copy to preserve original

    ff = ff[["make", "model", "year", "comb08u", "fueltype1"]]
    ff = ff.rename(columns={"comb08u": "average_mpg", "fueltype1": "fuel_type"})

    ff["year"] = ff["year"].astype(str).str[:4].astype(int)
    ff["average_mpg"] = ff["average_mpg"].astype(float)
    # Some average_mpg values are 0. They aren't really, they're None.
    ff["average_mpg"] = ff["average_mpg"].replace(to_replace=0.0, value=None)

    # Per project requirement, only get cars that take regular gas
    ff = ff[ff["fuel_type"] == "Regular Gasoline"]

    logger.info("Transformations successful, pushing to database...")
    load_table(table=TABLE, records=ff.to_dict(orient="records"))
