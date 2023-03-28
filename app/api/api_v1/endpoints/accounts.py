import logging
from typing import Optional
from uuid import UUID
from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from pydantic import ValidationError
from starlette.responses import JSONResponse

from sqlalchemy.orm import Session
from app.crud.crud_account import account

from app.config import settings
from app.core.security import create_access_token
from app.config.loggers import log_error
from app.api.depends import get_db
from app.schemas.account_schema import AccountRequest, AccountResponse, AccountSchema, AllUserAccountResponse
from app.core.security_decorators import auth_required

account_router = APIRouter(prefix="/accounts",dependencies=[Depends(get_db)])


@account_router.post("",tags=["createaccount"], response_model=AccountResponse, status_code=201)
@auth_required
async def create_account(payload: AccountRequest,
                         request_obj: Request,
                         user_id: Optional[UUID] = None,
                         session: Session = Depends(get_db)):
    """create a account api endpoint"""
    logging.info("Creating account")
    print(payload.dict())
    data = {**payload.dict(), "user_id": user_id}
    request_data = AccountSchema(**data)
    response = account.create(db=session, obj_in=request_data)
    if response is None:
        error_message = {
            "error_message": "An error occurred unable to create account"}
        logging.error("Error creating an account.")
        return JSONResponse(error_message, status_code=400)
    response_dict = response.__dict__
    resp = {**response_dict}
    json_response = AccountResponse(**resp).dict()
    return JSONResponse(json_response, status_code=201)


@account_router.get("/all",
                    tags=["get all user account"],
                    response_model=AllUserAccountResponse, status_code=200)
@auth_required
async def get_all_account(
    request_obj: Request,
    user_id: Optional[UUID] = None,
    session: Session = Depends(get_db)
):
    """get all account"""
    logging.info("get account")
    response = account.get_by_account_owner_id(db=session, user_id=user_id)
    if response is None:
        return JSONResponse({"Error": "accounts not found"}, status_code=404)
    resp = [AccountResponse(account_number=acc.account_number,
                            account_type=acc.account_type).dict() for acc in response]
    json_response = resp
    return JSONResponse(json_response, status_code=200)


@account_router.get("/{account_number}",
                    tags=["get with account number"],
                    response_model=AccountResponse, status_code=200)
@auth_required
async def get_account(account_number: str,
                      request_obj: Request,
                      user_id: Optional[UUID] = None,
                      session: Session = Depends(get_db)):
    """ get account api endpoint"""
    logging.info("get account")
    response = account.get_by_account_number(
        db=session, account_number=account_number, user_id=user_id)
    if response is None:
        return JSONResponse({"Error": "account not found"}, status_code=404)
    response_dict = response.__dict__
    resp = {**response_dict}
    json_response = AccountResponse(**resp).dict()
    return JSONResponse(json_response, status_code=200)


@account_router.delete("/{account_number}", tags=["delete"], status_code=200)
@auth_required
async def delete_account(account_number: str,
                         request_obj: Request,
                         user_id: Optional[UUID] = None,
                         session: Session = Depends(get_db)):
    """ delete account api endpoint"""
    logging.info("delete account")
    account_to_delete = account.get_by_account_number(
        db=session, account_number=account_number, user_id=user_id)
    if account_to_delete is None:
        return JSONResponse({"Error": "unable to delete account not found"}, status_code=404)
    deleted = account.delete(db=session, db_obj=account_to_delete) is not None
    if not deleted:
        return JSONResponse({"Error": "unable to delete, an error occured"}, status_code=400)
    return JSONResponse({"success": "account deleted successfully"}, status_code=200)
