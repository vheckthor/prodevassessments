import uuid
from sqlalchemy.orm import Session
from app import models
from app.core.security import get_password_hash


class MockUserSession():
    """Mock session for db"""

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
        self.data = [models.User(
            id=uuid.UUID('1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f5'),
            last_name="Drey",
            first_name="Kad",
            email="kad@gmail.com",
            hashed_password=get_password_hash("helloworld"),
            phone_number="07029345"
        ),
            models.User(
            id=uuid.uuid4(),
            last_name="Durojaye",
            first_name="Blend",
            email="durojaye@gmail.com",
            hashed_password=get_password_hash("test_password"),
            phone_number="13482345"
        )]

    def add_mock_data_to_db(self, user=None):
        if user:
            self.data.append(user)
        self.db_session.add_all(self.data)
        self.db_session.commit()
        self.db_session.refresh(self.data[0])

    def get_mock_data_from_db(self, id):
        return self.db_session.query(models.User).filter(models.User.id == id).first()

    def clear_mock_db(self) -> None:
        self.db_session.query(models.User).delete()
        self.db_session.commit()
