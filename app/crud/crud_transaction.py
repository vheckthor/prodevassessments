import uuid
from uuid import UUID
from typing import Optional, List, Tuple

from sqlalchemy.orm import Session

from app.crud.base import CrudBase
from app.models.transaction import Transaction
from app.config.loggers import log_error


class CrudTransaction(CrudBase[Transaction]):
    def get_by_transaction_accound_id(self,
                                      db: Session,
                                      account_id: UUID,
                                      transaction_description: str,
                                      skip: int = 0,
                                      limit: int = 5,) -> Tuple[int, Optional[List[Transaction]]]:
        
        search_param = f"%{transaction_description}%"
        db_lazy_query = db.query(Transaction).filter(
            Transaction.account_id == account_id, Transaction.transaction_description.like(search_param))
        return (
            db_lazy_query.count(),
            db_lazy_query.offset(skip).limit(limit).all()
        )

    # def get_by_transaction_number(self,db: Session,transaction_number: str, user_id: UUID) -> Optional[Transaction]:
    #     return (
    #         db.query(Transaction).filter(Transaction.transaction_number == transaction_number, Transaction.user_id == user_id).first()
    #     )
    

    def create(self, db: Session, *, obj_in) -> Transaction:
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

    # def update(self, db: Session, *, db_obj: Transaction, obj_in) -> Transaction:
    #     obj_data = jsonable_encoder(db_obj)

    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)

    #     for field in obj_data:
    #         if field in update_data:
    #             setattr(db_obj, field, update_data[field])

    #     try:
    #         db.add(db_obj)
    #         db.commit()
    #         db.refresh(db_obj)
    #     except Exception as e_x:
    #         log_error(e_x)
    #         return None
    #     return db_obj

transaction = CrudTransaction(Transaction)
