import uuid
from datetime import timedelta
from sqlalchemy.orm import Session
from app.api.api_v1.endpoints.test_mocks.user_api_mock import MockUserSession
from app.models import Account, Transaction
from app.core.security import create_access_token


class MockAccountSession():
    """Mock session for db"""

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
        self.users = MockUserSession(db_session)
        self.data = [
            Account(
                account_id=uuid.uuid4(),
                user_id=uuid.UUID("1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f5"),
                account_number="8912038294",
                account_type="savings",
            ),
            Account(
                account_id=uuid.UUID("91237437-72ad-4f11-9bce-587f129929ee"),
                user_id=uuid.UUID("1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f5"),
                account_number="1123038294",
                account_type="current",
            )
        ]

    def get_logged_in_jwt(self) -> str:
        token = create_access_token(
            uuid.UUID("1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f5"),
            timedelta(seconds=1000)
        )
        return token

    def add_mock_data_to_db(self, account=None) -> None:
        self.users.add_mock_data_to_db()
        if account:
            self.data.append(account)
        self.db_session.add_all(self.data)
        self.db_session.commit()
        self.db_session.refresh(self.data[0])

    def clear_mock_db(self) -> None:
        self.db_session.query(Account).delete()
        self.db_session.commit()
        self.users.clear_mock_db()


class MockTransactionSession():
    """mock transation"""

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
        self.accounts = MockAccountSession(db_session)
        self.data = [
            Transaction(
                account_id="81ba5aa1-5831-4c19-bada-f9bac21fccb4",
                transaction_amount=100000,
                transaction_description="salary for may",
                transaction_id=uuid.UUID(
                    "752cd2cf-7771-401c-ac67-8aefa3cf92f2"),
                user_ip="127.0.0.1",
                user_location="botswana",
                transaction_type="credit"
            ),
            Transaction(
                account_id="81ba5aa1-5831-4c19-bada-f9bac21fccb4",
                transaction_amount=10000,
                transaction_description="POS payments",
                transaction_id=uuid.UUID(
                    "71c1bdb2-5235-4fd5-8311-cd9bf0c8f224"),
                user_ip="127.0.0.1",
                user_location="botswana",
                transaction_type="debit"
            ),
            Transaction(
                account_id="81ba5aa1-5831-4c19-bada-f9bac21fccb4",
                transaction_amount=400000,
                transaction_description="salary for december",
                transaction_id=uuid.UUID(
                    "46db676a-ace6-4d0d-af82-1461107f3d51"),
                user_ip="127.0.0.1",
                user_location="botswana",
                transaction_type="credit"
            ),
            Transaction(
                account_id="81ba5aa1-5831-4c19-bada-f9bac21fccb4",
                transaction_amount=200000,
                transaction_description="salary for june",
                transaction_id=uuid.UUID(
                    "a7ee0029-0210-4114-b073-438b81781326"),
                user_ip="127.0.0.1",
                user_location="burundi",
                transaction_type="credit"
            ),
            Transaction(
                account_id="81ba5aa1-5831-4c19-bada-f9bac21fccb4",
                transaction_amount=10000,
                transaction_description="atm withrawal",
                transaction_id=uuid.UUID(
                    "3aeec719-b85c-4e3c-ac4e-72b31b7a53d5"),
                user_ip="127.0.0.1",
                user_location="botswana",
                transaction_type="debit"
            )
        ]

    def get_logged_in_jwt(self) -> str:
        token = create_access_token(
            uuid.UUID("1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f5"),
            timedelta(seconds=1000)
        )
        return token

    def add_mock_data_to_db(self, transaction=None) -> None:
        self.accounts.add_mock_data_to_db(Account(
            account_id=uuid.UUID("81ba5aa1-5831-4c19-bada-f9bac21fccb4"),
            user_id=uuid.UUID("1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f5"),
            account_balance=10000,
            account_number="1123012492",
            account_type="current",
        ))
        if transaction:
            self.data.append(transaction)
        self.db_session.add_all(self.data)
        self.db_session.commit()
        self.db_session.refresh(self.data[0])

    def get_mock_data_from_db(self, id) -> Account | None:
        self.accounts.add_mock_data_to_db()
        return self.db_session.query(Transaction).filter(
            Transaction.transaction_id == id).first()

    def clear_mock_db(self) -> None:
        self.db_session.query(Transaction).delete()
        self.db_session.commit()
        self.accounts.clear_mock_db()
