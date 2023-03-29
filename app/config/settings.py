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
    PROJECT_NAME: Optional[str] = os.environ.get("PROJECT_NAME", "test")
    API_V1_STR: Optional[str] = os.environ.get("API_V1_STR", "/prodev")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "100"))
    FIRST_SUPERUSER: str = os.environ.get("FIRST_SUPERUSER", "victor")
    FIRST_SUPERUSER_PASSWORD: str = os.environ.get("FIRST_SUPERUSER_PASSWORD", "password@123")
    FIRST_SUPERUSER_PHONE: str = os.environ.get("FIRST_SUPERUSER_PHONE", "07039466998")
    FIRST_SUPERUSER_EMAIL: str = os.environ.get("FIRST_SUPERUSER_EMAIL", "adebayovicktor@gmail.com")
    IPIFY_API_KEY: str = os.environ.get("IPIFY_API_KEY", "")
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
