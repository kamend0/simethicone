import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_connection_string():
    """
    Formats and returns postgres connection string using data from environment variables
    Why not stored in its own variable? .env vars are shared with Docker config which
    need them broken out
    """
    return (
        "postgresql://"
        f"{os.environ.get('POSTGRES_USERNAME')}:"
        f"{os.environ.get('POSTGRES_PASSWORD')}"
        f"@{os.environ.get('POSTGRES_HOST', default='localhost')}:{os.environ.get('POSTGRES_PORT', default=5432)}/"
        f"{os.environ.get('POSTGRES_DATABASE', default='postgres')}"
    )


def get_engine(connection_string: str = get_connection_string()):
    return create_engine(connection_string)


# For FastAPI connection, need an async function

Session = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)


async def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
