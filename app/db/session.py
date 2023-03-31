from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from app.config import settings

engine = create_engine(
    settings.Settings().SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

if not database_exists(engine.url):
    create_database(engine.url)

session_local = sessionmaker(
    autocommit=False, autoflush=False, future=True, bind=engine
)
