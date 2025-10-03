from database.connector import get_engine
from database.models import Base


def init_db():
    Base.metadata.create_all(bind=get_engine())


if __name__ == "__main__":
    init_db()
