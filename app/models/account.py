import uuid
from sqlalchemy import Column, String, ForeignKey, Float
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
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    account_type = Column(String, nullable=False, default="savings")
    account_number = Column(String, nullable=False, index=True, unique=True)
    account_balance = Column(Float, nullable=True, default=0.00)
    user = relationship(
        "User", foreign_keys=[user_id]
    )
    transaction = relationship(
        "Transaction",
        foreign_keys="Transaction.account_id",
        uselist=True,
        viewonly=True,
        cascade="all, delete-orphan"
    )
