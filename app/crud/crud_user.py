from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import update as update_user
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CrudBase
from app.models.user import User
from app.config.loggers import log_error


class CrudUser(CrudBase[User]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in) -> User:
        db_obj = User(
            id=obj_in.id,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            phone_number=obj_in.phone_number,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name
        )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as e_x:
            log_error(e_x)
            return None
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in) -> User:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password


        try:
            query = update_user(User).where(User.email == obj_in.email).values(update_data)
            db.execute(query)
            db.commit()
        except Exception as e_x:
            log_error(e_x)
            return None
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user_by_email = self.get_by_email(db, email=email)
        if not user_by_email:
            return None
        if not verify_password(password, user_by_email.hashed_password):
            return None
        return user_by_email

    def is_superuser(self, user_to_check: User) -> bool:
        return user_to_check.is_superuser

    def is_active(self, user_to_check: User) -> bool:
        return user_to_check.is_active


user = CrudUser(User)
