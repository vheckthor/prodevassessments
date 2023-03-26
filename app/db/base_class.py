import uuid
from datetime import datetime
from re import sub

from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base


@as_declarative()
class Base:
    # __allow_unmapped__ = True
    date_created = Column(DateTime, default = datetime.now(), nullable = False)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return "_".join(
            sub(
                "([A-Z][a-z]+)",
                r" \1",
                sub("([A-Z]+)", r" \1", cls.__name__.replace("-", " ")),
            ).split()
        ).lower()

# Base = declarative_base(cls=Base)
