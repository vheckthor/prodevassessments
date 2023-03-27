import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from app.db.base_class import Base


class Account(Base):
    account_id: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    account_type = Column(String, nullable=False, default="savings")
    account_number = Column(String, nullable=False, index=True, unique=True)
    user = relationship(
        "User", foreign_keys=[user_id]
    )
