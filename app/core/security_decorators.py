from functools import wraps
from fastapi import HTTPException
from pydantic import ValidationError
from app.api.depends import get_current_active_user
from app.config.loggers import log_error


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            session = kwargs["session"]
            request_obj = kwargs["request_obj"]
            current_user = get_current_active_user(session, request_obj)
            kwargs["user_id"] = current_user.id
        except (ValueError, ValidationError, Exception) as e_x:
            log_error(e_x)
            raise HTTPException(status_code=403, detail="authentication error")
        if current_user is None:
            raise HTTPException(status_code=403, detail="authentication error")
        return await func(*args, **kwargs)

    return wrapper
