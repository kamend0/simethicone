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
the API via `localhost:8000`. It will automatically start the app as well, but if you 
need to re-start it, use `make start`. This will not run the database loads again.

## Stopping + Destroying

To stop the app, use `make stop`. To stop and destroy the database volume(s), use 
`make kill`.

## Limitations (non-exhaustive list)

The ETL is a one-and-done thing; `make build` is essentially a magic trick. It expects 
to build everything from the ground up, not update it with new data. Mainly that 
work would happen with the EIA API interaction, but for now the only way to update the 
data is to wipe it and run the ETL again. It takes a few minutes if you're hitting the 
API.

The ETL has a manual switch to grab local data that you have to change source code for. 
It's mainly a development thing, but that means there's no smarter mechanism for not 
hitting the API if you don't have to.
