from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.Settings().SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
session_local = sessionmaker(
    autocommit=False, autoflush=False, future=True, bind=engine
)
