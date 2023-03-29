import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

from sqlalchemy.orm import Session

from app.crud.crud_account import account
from app.crud.crud_transaction import transaction
from app.crud.crud_user import user
from app.core.transaction_operations import (
    get_user_ip, get_user_location_from_ip, perform_credit_or_debit_operations
)
from app.api.depends import get_db
from app.schemas.account_schema import AccountRequest, AccountResponse, AccountSchema, AllUserAccountResponse
from app.schemas.transaction_schema import (
    TransactionRequest, TransactionSchema, AllAccountTransactionResponse)
from app.core.security_decorators import auth_required

account_router = APIRouter(
    prefix="/accounts", tags=["Accounts"], dependencies=[Depends(get_db)])


@account_router.post("", response_model=AccountResponse, status_code=201)
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


@account_router.get("/{id}",
                    response_model=AccountResponse, status_code=200)
async def get_account(id: str,
                      request_obj: Request,
                      user_id: Optional[UUID] = None,
                      session: Session = Depends(get_db)):
    """ get account api endpoint"""
    logging.info("get account")
    response = account.get_by_account_number(
        db=session, account_number=id, user_id=user_id)
    if response is None:
        return JSONResponse({"Error": "account not found"}, status_code=404)
    user_obj = user.get(db=session, id=response.user_id)
    user_full_name = f"{user_obj.first_name} {user_obj.last_name}"
    total_transaction_count = transaction.get_transaction_count(db=session,
                                                                account_id=response.account_id)
    json_response = {"account_name": user_full_name,
                     **AccountResponse.from_orm(response).dict(),
                     "total_transactions": total_transaction_count,
                     }
    return JSONResponse(json_response, status_code=200)


@account_router.delete("/{account_number}", status_code=200)
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


@account_router.post("/{id}/transactions", status_code=201)
@auth_required
async def perform_transactions(payload: TransactionRequest,
                               request_obj: Request,
                               id: str,
                               user_id: Optional[UUID] = None,
                               session: Session = Depends(get_db)) -> JSONResponse:
    """Transaction operation, input amount must be a float"""
    logging.info("transaction operation")
    user_ip = get_user_ip(request_obj)
    user_location = get_user_location_from_ip(user_ip)
    account_to_details = account.get_by_account_number(
        db=session, account_number=id, user_id=user_id)
    if account_to_details is None:
        return JSONResponse({"error": "account  details not found"}, status_code=404)
    try:
        balance = perform_credit_or_debit_operations(
            account_to_details.account_balance, payload.transaction_amount, payload.transaction_type
        )
    except ValueError as e_x:
        return JSONResponse({"error": f"{e_x}"}, status_code=400)
    account.update(db=session, db_obj=account_to_details,
                   obj_in={"account_balance": balance})
    transact_data = {**payload.dict(), "account_id": account_to_details.account_id,
                     "user_ip": user_ip, "user_location": user_location}
    done = transaction.create(
        db=session, obj_in=TransactionSchema(**transact_data))
    if done is None:
        return JSONResponse({"error": "transaction unsuccessful"}, status_code=400)
    str_response = f"""{payload.transaction_amount} has been {payload.transaction_type}ed"""
    return JSONResponse(
        {"success": str_response, "balance": balance}, status_code=201)


@account_router.get("/{id}/transactions", response_model=AllAccountTransactionResponse, status_code=200)
@auth_required
async def get_list_transactions(
                                request_obj: Request,
                                id: str,
                                user_id: Optional[UUID] = None,
                                search: Optional[str]="",
                                page_mumber: Optional[int]=1,
                                limit: Optional[int]=50,
                                session: Session = Depends(get_db)) -> JSONResponse:
    """Get list of all transactions for an account number (id) 
    and search by transaction description"""
    trans_account = account.get_by_account_number(db=session, account_number=id, user_id=user_id)
    if trans_account is None:
        return JSONResponse({"error": "Account is not found"}, status_code=404)
    try:
        resp = transaction.get_by_transaction_account_id_and_search_param(db=session,
                                                     account_id=trans_account.account_id,
                                                     transaction_description=search,
                                                     limit=limit, page_number=page_mumber)
    except ValueError as ex:
        return JSONResponse(f"{ex}", 400)

    return JSONResponse(resp.dict(), 200)
