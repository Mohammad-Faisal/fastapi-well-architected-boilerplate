from sqlmodel import create_engine, Session

from src.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
