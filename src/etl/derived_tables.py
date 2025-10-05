from sqlalchemy import text

from src.database.connector import get_engine
from src.etl.utils import get_logger

logger = get_logger()


def create_derived_tables():
    engine = get_engine()

    derived_table_queries = {
        "fuel_efficiency_monthly": "load_fuel_efficiency_monthly.sql"
    }

    for table_name, table_query_filepth in derived_table_queries.items():
        query_filepath = f"src/database/sql/{table_query_filepth}"
        logger.info(
            f"Populating table {table_name} from query definition at {query_filepath}"
        )
        with open(query_filepath, "r") as f:
            query = f.read()

        with engine.begin() as conn:
            conn.execute(text(query))

        logger.info(f"Table {table_name} populated successfully!")
