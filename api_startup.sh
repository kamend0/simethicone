# Load the database upon app startup
python3 -m src.database.scripts.init_db
python3 -m src.etl.run

# Run the API
fastapi run src/api/main.py --host 0.0.0.0 --port 8000 --reload