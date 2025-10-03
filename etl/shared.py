"""
Various functions to retrieve, read, parse, clean, and load data integral to the
Simethicone database
"""

import logging

from sqlalchemy import insert
from sqlalchemy.sql.schema import Table

from database.connector import get_engine


def get_logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger()


def load_table(
    table: Table, records: list[dict], logger: logging.Logger = get_logger()
):
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
