from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, validator


class TransactionRequest(BaseModel):
    transaction_type: str
    transaction_amount: float
    transaction_description: str

    @validator("transaction_type")
    @classmethod
    def validate_transaction_type(cls, value: str):
        if value.lower() not in ["credit", "debit"]:
            raise ValueError(
                "incorrect transaction type, transaction type must be credit or debit")
        return value

    @validator("transaction_amount")
    @classmethod
    def validate_transaction_amount(cls, value: float) -> float:
        if value <= 0.0:
            raise ValueError("transaction amount must be greater than 0")

        return value


class TransactionResponse(BaseModel):
    class Config():
        orm_mode = True

    transaction_date: str = Field(alias="date_created")
    transaction_type: str
    transaction_amount: float
    transaction_description: str

    @validator("transaction_date", pre=True)
    @classmethod
    def validate_transaction_date(cls, value):
        string_date_time = value.strftime("%Y/%m/%d, %H:%M:%S")
        return string_date_time


class AllAccountTransactionResponse(BaseModel):
    total_count: int
    total_number_of_pages: int
    current_page: int
    next_page: int
    limit: int
    all_transactions: list[TransactionResponse]


class TransactionSchema(BaseModel):
    transaction_id: Optional[UUID]
    account_id: UUID
    transaction_type: str
    transaction_amount: float
    user_ip: str
    user_location: str
    transaction_description: str
