from uuid import UUID
from typing import Optional
from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: Optional[UUID] = None
