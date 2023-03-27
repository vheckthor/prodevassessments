import uuid
from uuid import UUID
from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CrudBase
from app.models.account import Account
from app.config.loggers import log_error



class CrudAccount(CrudBase[Account]):
    def get_by_account_owner_id(self,db: Session,user_id: UUID, skip: int = 0, limit: int = 5,) -> Optional[List[Account]]:
        return (
            db.query(Account).filter(Account.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_account_number(self,db: Session,account_number: str) -> Optional[Account]:
        return (
            db.query(Account).filter(Account.account_number == account_number).first()
        )
    

    def create(self, db: Session, *, obj_in) -> Account:
        db_obj = Account(
            account_id=uuid.uuid4(),
            user_id = obj_in.user_id,
            account_number=obj_in.account_number,
            account_type=obj_in.account_type
        )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as e_x:
            log_error(e_x)
            return None
        return db_obj

    def update(self, db: Session, *, db_obj: Account, obj_in) -> Account:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as e_x:
            log_error(e_x)
            return None
        return db_obj

account = CrudAccount(Account)
