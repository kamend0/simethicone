# Create database tables according to models on startup
python3 -m src.database.scripts.init_db

# Run the API
fastapi run src/api/main.py --host 0.0.0.0 --port 8000 --reload