from typing import Annotated

from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.api.utils import get_most_economical_memoized
from src.database.connector import get_db

app = FastAPI()


@app.get("/")
async def healthy():
    return JSONResponse(content={"status": "ok"}, status_code=200)


# TODO: create your API
@app.get("/economical/")
async def get_economical(
    duoarea: str,
    month: int,
    year: int,
    db: Annotated[Session, Depends(get_db)],
):
    most_economical = get_most_economical_memoized(
        duoarea=duoarea, month=month, year=year, db=db
    )

    if most_economical.vehicle is None:
        return JSONResponse(
            content={
                "message": "Could not find the most economic vehicle for the given parameters. Please try a different set.",
                "duoarea": duoarea,
                "month": month,
                "year": year,
            },
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    return JSONResponse(
        content={
            "most_economical_vehicle": most_economical.vehicle.common_name(),
            "duoarea": duoarea,
            "month": month,
            "year": year,
        },
        status_code=status.HTTP_200_OK,
    )
