import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


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


def create_sessionmaker(
    connection_string: str = get_connection_string(), engine: Engine = None
):
    if not engine:
        engine = create_engine(connection_string)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db(
    session_maker: Session = create_sessionmaker(),
):
    return session_maker()
