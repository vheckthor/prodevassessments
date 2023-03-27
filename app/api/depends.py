from typing import Generator, Tuple

from fastapi import Request
from pydantic import ValidationError
from jose import jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.schemas.token_schema import TokenPayload
from app.core import security
from app.crud.crud_user import user
from app.db.session import session_local
from app.models.user import User


def get_db() -> Generator:
    try:
        db = session_local()
        yield db
    finally:
        db.close()

def get_authorization_scheme_param(authorization_header_value: str) -> Tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


def get_current_user(db: Session, request: Request) -> User:
    authorization: str = request.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise Exception("Not authenticated")

    try:
        payload = jwt.decode(
            token, settings.Settings().SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as error:
        raise ValueError(
            f"Could not validate credentials. Error received: {error}"
        ) from error
    current_user = user.get(db, id=token_data.sub)
    if not current_user:
        raise Exception(f"Could not validate user. Received: {current_user}")
    return current_user


def get_current_active_user(db: Session, request: Request) -> User:
    current_user = get_current_user(db=db, request=request)

    if not user.is_active(current_user):
        raise Exception("user account deactivated")

    return current_user