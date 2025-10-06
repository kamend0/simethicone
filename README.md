# Simethicone

A project to determine the most economical car to drive in a given area and time period. 
(Spoiler alert: it's the one with the highest MPG.)

**Stack:** Almost 100% Python-based. Postgres database and FastAPI REST API. A single 
SQL script to create a derived table.

The app's database is unpopulated on app startup, though tables are created according 
to model definitions in `src/database/models.py`. The REST API is spun up right away on
`localhost:8000` with just two endpoints as described in the project document (a health 
check at root, and an `economical` endpoint).

## Running the app

A Makefile is included with commands to build the Docker images, load the database, and 
run the app. You will need a `.env` file in your root directory with the following 
entries:

```
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DATABASE
POSTGRES_USERNAME
POSTGRES_PASSWORD
EIA_API_KEY
```

Clone the repo, add that file, then you're off to the races with `make build`. It will 
spin up the API automatically, but you need to run `make load_db` before it'll be ready 
to handle requests properly.

To stop the app, use `make stop`. To start it up again, use `make start`; to stop *and*
destroy the database volume(s), use `make kill`.

## Limitations (non-exhaustive list)

The ETL is a one-and-done thing; `make load_db` is essentially a magic trick. It expects 
to build everything from the ground up, not update it with new data. Mainly that 
work would happen with the EIA API interaction, but for now the only way to update the 
data is to wipe it and run the ETL again. It takes about a minute.

The ETL has a manual switch to grab local data that you have to change source code for. 
It's mainly a development thing, but that means there's no smarter mechanism for not 
hitting the API if you don't have to.
