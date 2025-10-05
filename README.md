# Simethicone

A project to determine the most economical car to drive in a given area and time period. 
Spoiler alert: it's the one with the highest MPG.

## Stack

Almost 100% Python-based. Postgres database and FastAPI REST API. A single SQL script 
to create a derived table.

## Building + Running

A Makefile is included with commands to build the Docker images and run the app. You 
will need a `.env` file in your root directory with the proper credentials, including:

- An EIA API key
- All Postgres configs (HOST, PORT, etc.)

Clone the repo, add that file, then you're off to the races with `make build`. Access 
the API via `localhost:8000`.