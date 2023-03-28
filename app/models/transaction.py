import uuid
from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from app.db.base_class import Base


class Transaction(Base):
    transaction_id: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False
    )
    account_id = Column(
        UUID(as_uuid=True), ForeignKey("account.account_id", ondelete="CASCADE"),
        nullable=False
    )
    transaction_type = Column(String, nullable=False)
    transaction_amount = Column(Float, nullable=False, index=True, default=0.00)
    user_ip = Column(String, nullable=False)
    user_location = Column(String, nullable=False)
    transaction_description = Column(String, nullable=False)
    account = relationship(
        "Account", foreign_keys=[account_id]
    )
