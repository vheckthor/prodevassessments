from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str


class UserAuthRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str

class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    isactive: Optional[bool]

class UserSchema(BaseModel):
    class Config:
        extra = "allow"
        orm_mode = True
        arbitrary_types_allowed = True

    id: UUID
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    isactive: Optional[bool]
