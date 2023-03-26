"""
    Project settings file
"""
import os
from typing import List, Union, Optional, Dict, Any

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl, validator
from sqlalchemy import engine

class Settings(BaseSettings):
    '''
    Application settings for api
    '''
    load_dotenv()
    FIRST_SUPERUSER: str = os.environ.get("FIRST_SUPERUSER", "victor")
    FIRST_SUPERUSER_PASSWORD: str = os.environ.get("FIRST_SUPERUSER_PASSWORD", "password@123")
    FIRST_SUPERUSER_PHONE: str = os.environ.get("FIRST_SUPERUSER_PHONE", "07039466998")
    FIRST_SUPERUSER_EMAIL: str = os.environ.get("FIRST_SUPERUSER_EMAIL", "adebayovicktor@gmail.com")
    # POSTGRES_SERVER: Optional[str] = os.environ.get("POSTGRES_SERVER", "")
    # POSTGRES_PORT: Optional[str] = os.environ.get("POSTGRES_PORT","")
    # POSTGRES_USER: Optional[str] = os.environ.get("POSTGRES_USER","")
    # POSTGRES_PASSWORD: Optional[str] = os.environ.get("POSTGRES_PASSWORD", "")
    # POSTGRES_DB: Optional[str] = os.environ.get("POSTGRES_DB", "")
    SQLALCHEMY_DATABASE_URI: Union[Optional[engine.url.URL], Optional[str]] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, value: Optional[str], values: Dict[str, Any]) -> Any:  # pylint: disable=no-self-argument
        if isinstance(value, str):
            return value
        return engine.url.URL.create(
            "postgresql+psycopg2",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            database=os.environ.get("POSTGRES_DB"),
        )
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = [
        "http://localhost:3000",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> Union[List[str], str]:  # pylint: disable=no-self-argument
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    class Config:  # pylint: disable=too-few-public-methods
        env_file = ".env"
        case_sensitive = True
