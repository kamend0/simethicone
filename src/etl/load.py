"""
Top-level script to run the various ETLs populating the Simethicone database
"""

from src.etl.annual_miles import run_annual_miles_etl
from src.etl.fuel_efficiency import run_fuel_efficiency_etl
from src.etl.vehicle_data import run_vehicle_data_etl

if __name__ == "__main__":
    run_annual_miles_etl()
    run_fuel_efficiency_etl(use_local=False)
    run_vehicle_data_etl()
