from typing import Optional
from uuid import UUID
from pydantic import BaseModel, root_validator, validator


class TransactionRequest(BaseModel):
    transaction_type: str
    transaction_amount: float
    @validator("transaction_type")
    @classmethod
    def validate_transaction_type(cls, value: str):
        if value.lower() not in ["credit", "debit"]:
            raise ValueError("incorrect transaction type, transaction type must be credit or debit")
        return value


class TransactionResponse(BaseModel):
    transaction_number: str
    transaction_type: str
    transaction_amount: float
    transaction_description: str


class AllAccountTransactionResponse(BaseModel):
    all_transactions: list[TransactionResponse]


class TransactionSchema(BaseModel):
    transaction_id: Optional[UUID]
    account_id: UUID
    transaction_type: str
    transaction_amount: float
    user_ip: str
    user_location: str
    transaction_description: str
