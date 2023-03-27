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
    account_number: str
    account_type: str


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
