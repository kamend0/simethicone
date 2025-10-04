from src.database.connector import get_engine
from src.database.models import Base


def init_db():
    Base.metadata.create_all(bind=get_engine())


if __name__ == "__main__":
    init_db()
