import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import pandas as pd
import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from database.connector import get_engine
from database.models import FuelEfficiency
from etl.shared import get_logger, load_table

BASE_URL = "https://api.eia.gov/v2/petroleum/pri/gnd/data"
RECORD_LIMIT = 5000


@retry(
    wait=wait_exponential(multiplier=1, min=2, max=15),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
)
def get_with_exp_retry(url: str, params: dict):
    response = requests.get(url, params=params, timeout=10)  # add timeout
    response.raise_for_status()  # raise for HTTP errors, which will be retried
    return response


def fetch_fuel_efficiency_response_json(offset: int = 0) -> dict:
    params = {
        "api_key": os.environ.get("EIA_API_KEY"),
        "frequency": "weekly",
        "data[0]": "value",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": offset,
        "length": 5000,
    }

    response = get_with_exp_retry(url=BASE_URL, params=params)

    # We know that our response is valid and non-empty at this point, because we limit
    # our requests to the total number of available records, and capture bad statuses
    return response.json()


def fetch_fuel_efficiency_data(
    offset: int = 0, response_json: dict = None
) -> list[dict]:
    if response_json is None:
        response_json = fetch_fuel_efficiency_response_json(offset=offset)
    return response_json.get("response", {}).get("data", [])


def fetch_all_fuel_efficiency_data(logger=get_logger()):
    """
    Makes exactly the number of API calls needed to the EIA API to retrieve all fuel
    efficiency data by querying for total records first, then multithreading all
    necessary requests thereafter.
    Returns a list of all dict objects representing each record in their database.
    """
    logger.info("Retrieving total number of fuel efficiency records to fetch...")

    # Two birds with one stone: first batch gives data and total records
    first_batch_data = fetch_fuel_efficiency_response_json(offset=0)
    total_num_records = int(first_batch_data["response"]["total"])
    all_offsets = list(range(RECORD_LIMIT, total_num_records, RECORD_LIMIT))

    logger.info(f"Total available records: {total_num_records}")
    logger.info(
        f"Total remaining API calls to make: {len(all_offsets)} in batches of {RECORD_LIMIT} records"
    )

    all_results = fetch_fuel_efficiency_data(response_json=first_batch_data)
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Workers limited to 4 in an effort to reduce our impact on the API, and the
        # risk that we get our API key blocked/banned
        futures = [
            executor.submit(fetch_fuel_efficiency_data, offset)
            for offset in all_offsets
        ]
        for future in as_completed(futures):
            all_results.extend(future.result())
            logger.info(
                f"{len(future.result())} records fetched; total of {len(all_results)} records fetched so far"
            )
    logger.info(f"All API calls completed. Total records retrieved: {len(all_results)}")
    return all_results


def run_fuel_efficiency_etl(logger=get_logger()):
    """
    Extracts fuel efficiency data from the EIA API. Assumes presence of API key in the
    environment. Saves both the raw data returned from the API to a raw table in the
    database, as well as a pared-down and cleaned version to the "production" table.
    """
    TABLE = FuelEfficiency.__table__

    def _parse_fuel_efficiency_record(record: dict) -> dict:
        """
        Takes a record returned from the EIA fuel efficiency API, paring it down and
        cleaning to match the corresponding FuelEfficiency data model
        """
        load_record = {
            "period": record.get("period"),
            "duoarea": record.get("duoarea", "").strip(),
            "product_name": record.get("product-name"),
            "value": record.get("value"),
        }

        load_record["period"] = datetime.strptime(load_record["period"], "YYYY-mm-DD")
        load_record["value"] = float(record["value"])

        return load_record

    all_data = fetch_all_fuel_efficiency_data()

    # First, load these to the database to their own raw table; easiest with Pandas
    logger.info(f"Pushing raw data for {len(all_data)} to raw table...")
    pd.DataFrame(data=all_data).to_sql(name=f"raw_{TABLE.name}", con=get_engine())

    # Now we do some cleaning
    logger.info("Prepping fuel efficiency data for load to production...")
    load_data = [
        _parse_fuel_efficiency_record(record=data_record) for data_record in all_data
    ]

    load_table(table=TABLE, records=load_data)
