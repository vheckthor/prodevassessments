import uuid
from uuid import UUID
from typing import Optional, List, Tuple, Any

from sqlalchemy.orm import Session

from app.crud.base import CrudBase
from app.models.transaction import Transaction
from app.config.loggers import log_error
from app.schemas.transaction_schema import AllAccountTransactionResponse, TransactionResponse


class CrudTransaction(CrudBase[Transaction]):

    def get_transaction_count(self, db: Session, account_id: UUID) -> int:
        """get transaction count for a given account id"""
        return db.query(Transaction).filter(Transaction.account_id == account_id).count()

    def get_by_transaction_account_id_and_search_param(self,
                                                       db: Session,
                                                       account_id: UUID,
                                                       transaction_description: str,
                                                       page_number: int = 0,
                                                       limit: int = 50,) -> AllAccountTransactionResponse:
        """get transaction information by search params and account id"""
        if limit > 50 or limit < 1:
            raise ValueError(
                {"error_message": "The limit value is invalid", "error_code": 400})
        search_param = f"%{transaction_description}%"
        db_lazy_query = db.query(Transaction).filter(
            Transaction.account_id == account_id, Transaction.transaction_description.like(search_param))
        total_count = db_lazy_query.count()
        skip: int = (page_number * limit) - limit
        float_value = total_count / limit
        total_pages = int(
            float_value) if float_value.is_integer() else int(float_value)+1
        next_page = page_number+1 if page_number < total_pages else page_number
        data = db_lazy_query.offset(skip).limit(limit).all()
        list_of_transformed_response = [
            TransactionResponse.from_orm(val) for val in data]
        return AllAccountTransactionResponse(
            total_count=total_count,
            total_number_of_pages=total_pages,
            current_page=page_number,
            limit=limit,
            next_page=next_page,
            all_transactions=list_of_transformed_response)

    def create(self, db: Session, *, obj_in) -> Transaction | None:
        """create a transaction"""
        db_obj = Transaction(
            transaction_id=uuid.uuid4(),
            account_id=obj_in.account_id,
            transaction_type=obj_in.transaction_type,
            transaction_amount=obj_in.transaction_amount,
            user_ip=obj_in.user_ip,
            user_location=obj_in.user_location,
            transaction_description=obj_in.transaction_description
        )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as e_x:
            log_error(e_x)
            return None
        return db_obj


transaction = CrudTransaction(Transaction)
