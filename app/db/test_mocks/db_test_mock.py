import uuid
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os
from app.db.base import Base

SQLALCHEMY_BASE_DATABASE_URL = "postgresql+psycopg2"

url = engine.url.URL.create(
            SQLALCHEMY_BASE_DATABASE_URL,
            username=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=os.environ.get("POSTGRES_SERVER"),
            port=os.environ.get("POSTGRES_PORT"),
            database="test",
        )
eng = create_engine(url)
if not database_exists(url):
    create_database(url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, future=True, bind=eng)



Base.metadata.create_all(bind=eng)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()