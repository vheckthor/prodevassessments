import uuid
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID



from app.db.base_class import Base

class User(Base):
    id: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False
    )
    first_name = Column(String, nullable=False)
    last_name= Column(String, nullable=False)
    email= Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    account= relationship(
        "Account",
        foreign_keys="Account.user_id",
        uselist=True,
        viewonly= True,
        cascade="all, delete-orphan"
    )
