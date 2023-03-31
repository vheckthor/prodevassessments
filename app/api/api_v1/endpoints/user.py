"""user router module"""
import logging
import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from pydantic import ValidationError
from starlette.responses import JSONResponse

from sqlalchemy.orm import Session
from app.crud.crud_user import user

from app.config import settings
from app.core.security import create_access_token
from app.config.loggers import log_error
from app.api.depends import get_db, get_current_active_user
from app.schemas.user_schema import (
    UserRequest, UserAuthRequest, UserResponse, UserSchema, UserUpdateSchema)


user_router = APIRouter(
    prefix="/users", dependencies=[Depends(get_db)], tags=["Users"])


@user_router.post("", response_model=UserResponse, status_code=201)
async def create_user(request: UserRequest, session: Session = Depends(get_db)):
    """create a user api endpoint"""
    logging.info("Creating user")
    data = {**request.dict(), "id": uuid.uuid4()}
    request_data = UserSchema(**data)
    response = user.create(db=session, obj_in=request_data)
    if response is None:
        error_message = {
            "error_message": "An error occurred unable to create user"}
        logging.error("Error creating an user.")
        return JSONResponse(error_message, status_code=400)
    response_dict = response.__dict__
    resp = {**response_dict, "id": str(response_dict["id"])}
    json_response = UserResponse(**resp).dict()
    return JSONResponse(json_response, status_code=201)


@user_router.put("", response_model=UserResponse, status_code=202)
async def update_user(request: UserRequest, request_obj: Request, session: Session = Depends(get_db)):
    """ update user api endpoint"""
    logging.info("Updating user")
    data = {**request.dict()}
    request_data = UserUpdateSchema(**data)
    try:
        current_user = get_current_active_user(session, request_obj)
    except (ValueError, ValidationError, Exception) as e_x:
        log_error(e_x)
        return JSONResponse({"Error": "Unable to authenticate user"}, status_code=400)
    response = user.update(
        db=session,  db_obj=current_user, obj_in=request_data)
    if response is None:
        error_message = {
            "error_message": "An error occurred unable to update user"}
        logging.error("Error updating an user.")
        return JSONResponse(error_message, status_code=400)
    response_dict = response.__dict__
    resp = {**response_dict, "id": str(response_dict["id"])}
    json_response = UserResponse(**resp).dict()
    return JSONResponse(json_response, status_code=202)


@user_router.post("/authenticate", status_code=200)
async def authenticate_user(request: UserAuthRequest, session: Session = Depends(get_db)):
    """ authenticate user api endpoint"""
    logging.info("authenticate user")
    response = user.authenticate(
        db=session, email=request.email, password=request.password)
    if response is None:
        error_message = {"error_message": "Unable to authenticate user"}
        logging.error("Error authenticating an user.")
        return JSONResponse(error_message, status_code=401)
    if not response.is_active:
        return JSONResponse({"error": "user has been deactivated"}, status_code=403)
    access_token_expires = timedelta(
        minutes=settings.Settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    token_auth = {
        "access_token": create_access_token(
            response.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
    return JSONResponse(token_auth, status_code=200)


@user_router.get("/{userid}", response_model=UserResponse, status_code=200)
async def get_user(userid: uuid.UUID, session: Session = Depends(get_db)):
    """ get user api endpoint"""
    logging.info("get user")
    response = user.get(db=session, id=userid)
    if response is None:
        return JSONResponse({"Error": "user not found"}, status_code=404)
    response_dict = response.__dict__
    resp = {**response_dict, "id": str(response_dict["id"])}
    json_response = UserResponse(**resp).dict()
    return JSONResponse(json_response, status_code=200)


@user_router.delete("/{userid}", response_model=UserResponse, status_code=200)
async def delete_user(userid: uuid.UUID, session: Session = Depends(get_db)):
    """ delete user api endpoint"""
    logging.info("delete user")
    user_to_delete = user.get(db=session, id=userid)
    if user_to_delete is None:
        return JSONResponse({"Error": "unable to delete user not found"}, status_code=404)
    deleted = user.delete(db=session, db_obj=user_to_delete) is not None
    if not deleted:
        return JSONResponse({"Error": "unable to delete, an error occured"}, status_code=400)
    return JSONResponse({"success": "user deleted successfully"}, status_code=200)
