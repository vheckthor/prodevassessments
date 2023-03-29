from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, root_validator, validator
from app.core.account_number_generator import generate_random_account


class AccountRequest(BaseModel):
    account_type: str
    @validator("account_type")
    @classmethod
    def validate_account_type(cls, value: str):
        if value.lower() not in ["current", "savings"]:
            raise ValueError("incorrect account type, account type must be savings or current")
        return value


class AccountResponse(BaseModel):
    class Config():
        orm_mode = True

    account_number: str
    account_type: str
    account_date_created: str = Field(alias="date_created")
    account_balance: float

    @validator("account_date_created", pre=True)
    @classmethod
    def validate_transaction_date(cls, value):
        string_date_time = value.strftime("%Y/%m/%d, %H:%M:%S")
        return string_date_time



class AllUserAccountResponse(BaseModel):
    all_accounts: list[AccountResponse]


class AccountSchema(BaseModel):
    class Config:
        extra = "allow"
        orm_mode = True
        arbitrary_types_allowed = True

    account_id: Optional[UUID]
    account_type: Optional[str]
    account_number: Optional[str]
    account_balance: Optional[float]
    user_id: UUID

    @root_validator()
    @classmethod
    def validate_account_number(cls, values):
        """
        account_number
        """
        account_typ = values.get("account_type")
        values["account_number"] = generate_random_account(account_typ)
        return values
