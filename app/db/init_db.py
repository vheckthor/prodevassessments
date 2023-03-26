from sqlalchemy.orm import Session

from app import crud, schemas
from app.config import settings
from app.db import base  # pylint: disable=unused-import

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    config_setting = settings.Settings()
    user = crud.user.get_by_email(db, email=config_setting.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            username=config_setting.FIRST_SUPERUSER,
            password=config_setting.FIRST_SUPERUSER_PASSWORD,
            phone=config_setting.FIRST_SUPERUSER_PHONE,
            email=config_setting.FIRST_SUPERUSER_EMAIL,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
