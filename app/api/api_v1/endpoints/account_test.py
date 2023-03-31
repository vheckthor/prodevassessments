import unittest
from unittest import mock

from fastapi.testclient import TestClient

from app import main
from app.api.depends import get_db
from app.api.api_v1.endpoints.test_mocks.accounts_api_mock import (
    MockAccountSession, MockTransactionSession
)
from app.db.test_mocks.db_test_mock import override_get_db

main.app.dependency_overrides[get_db] = override_get_db

_CREATE_ACCOUNT_TEST_DATA = {
    "account_type": "savings"
}

_CREDIT_TRANSACTION_TEST_DATA = {
    "transaction_type": "credit",
    "transaction_amount": 50000.0,
    "transaction_description": "government funds"
}

_DEBIT_TRANSACTION_TEST_DATA = {
    "transaction_type": "debit",
    "transaction_amount": 3000,
    "transaction_description": "POS withdrawal"
}


class BaseTest(unittest.TestCase):
    client = TestClient(main.app)
    session = None
    headers = {}


class TestAccount(BaseTest):
    """
    TestUser Class
    """

    def setUp(self) -> None:
        self.session = MockAccountSession(list(override_get_db())[0])
        self.session.add_mock_data_to_db()
        self.headers = {
            "Authorization": f"bearer {self.session.get_logged_in_jwt()}"}

    def tearDown(self) -> None:
        self.session.clear_mock_db()

    def test_create_account(self) -> None:
        """/account create"""
        response = self.client.post(
            "/accounts", json=_CREATE_ACCOUNT_TEST_DATA, headers=self.headers)
        actual = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(actual["account_type"], "savings")

    def test_create_account_unauthorized(self) -> None:
        """/accounts create forbidden"""
        response = self.client.post("/accounts", json=_CREATE_ACCOUNT_TEST_DATA,
                                    headers={"Authorization": "some random auth"})
        self.assertEqual(response.status_code, 403)

    def test_get_all_account(self) -> None:
        """/accounts/all get all"""
        response = self.client.get("/accounts/all", headers=self.headers)
        actual = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0]["account_type"], "savings")

    def test_get_one_account(self) -> None:
        """/accounts/id get one"""
        response = self.client.get("/accounts/8912038294",
                                   headers=self.headers)
        actual = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(actual["account_type"], "savings")

    def test_get_one_unavailable_account(self) -> None:
        """/accounts/id get one"""
        response = self.client.get("/accounts/8912428294",
                                   headers=self.headers)
        actual = response.json()
        expected = {"Error": "account not found"}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(actual, expected)

    def test_delete_account(self) -> None:
        """/accounts/id delete account"""
        response = self.client.delete("/accounts/8912038294",
                                      headers=self.headers)
        actual = response.json()
        expected = {"success": "account deleted successfully"}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(actual, expected)

    def test_delete_unavailable_account(self) -> None:
        """/accounts/id delete account"""
        response = self.client.delete("/accounts/8912248294",
                                      headers=self.headers)
        actual = response.json()
        expected = {"Error": "unable to delete account not found"}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(actual, expected)

    def doCleanups(self) -> None:
        self.session.db_session.close()


class TestAccountTransactions(BaseTest):
    def setUp(self) -> None:
        self.session = MockTransactionSession(list(override_get_db())[0])
        self.session.add_mock_data_to_db()
        self.headers = {
            "Authorization": f"bearer {self.session.get_logged_in_jwt()}"}

    def tearDown(self) -> None:
        self.session.clear_mock_db()

    def test_perform_credit_transaction(self) -> None:
        """/accounts/{id}/transaction credit account"""
        with mock.patch("app.api.api_v1.endpoints.accounts.get_user_ip") as mock_ip:
            mock_ip.return_value = "127.0.121.1"
            with mock.patch("app.api.api_v1.endpoints.accounts.get_user_location_from_ip") as mock_location:
                mock_location.return_value = "Kalakuta"
                response = self.client.post("/accounts/1123012492/transactions",
                                            json=_CREDIT_TRANSACTION_TEST_DATA, headers=self.headers)
                actual = response.json()
                balance = 60000
                str_response = "50000.0 has been credited"
                expected = {"success": str_response, "balance": balance}
                self.assertEqual(response.status_code, 201)
                self.assertEqual(actual, expected)

    def test_perform_debit_transaction(self) -> None:
        """/accounts/{id}/transaction debit account"""
        with mock.patch("app.api.api_v1.endpoints.accounts.get_user_ip") as mock_ip:
            mock_ip.return_value = "127.0.121.1"
            with mock.patch("app.api.api_v1.endpoints.accounts.get_user_location_from_ip") as mock_location:
                mock_location.return_value = "maitama"
                response = self.client.post("/accounts/1123012492/transactions",
                                            json=_DEBIT_TRANSACTION_TEST_DATA, headers=self.headers)
                actual = response.json()
                balance = 7000
                str_response = "3000.0 has been debited"
                expected = {"success": str_response, "balance": balance}
                self.assertEqual(response.status_code, 201)
                self.assertEqual(actual, expected)

    def test_perform_debit_more_than_balance_transaction(self) -> None:
        """/accounts/{id}/transaction debit account"""
        with mock.patch("app.api.api_v1.endpoints.accounts.get_user_ip") as mock_ip:
            mock_ip.return_value = "127.0.121.1"
            with mock.patch("app.api.api_v1.endpoints.accounts.get_user_location_from_ip") as mock_location:
                mock_location.return_value = "maitama"
                response = self.client.post("/accounts/1123012492/transactions",
                                            json={**_DEBIT_TRANSACTION_TEST_DATA,
                                                  "transaction_amount": 12000},
                                            headers=self.headers)
                self.assertEqual(response.status_code, 400)

    def test_perform_debit_with_wrong_account_number_transaction(self) -> None:
        """/accounts/{id}/transaction debit account"""
        with mock.patch("app.api.api_v1.endpoints.accounts.get_user_ip") as mock_ip:
            mock_ip.return_value = "127.0.121.1"
            with mock.patch("app.api.api_v1.endpoints.accounts.get_user_location_from_ip") as mock_location:
                mock_location.return_value = "maitama"
                response = self.client.post("/accounts/1121212492/transactions",
                                            json={**_DEBIT_TRANSACTION_TEST_DATA,
                                                  "transaction_amount": 12000},
                                            headers=self.headers)
                self.assertEqual(response.status_code, 404)

    def test_perform_credit_with_wrong_account_number_transaction(self) -> None:
        """/accounts/{id}/transaction debit account"""
        with mock.patch("app.api.api_v1.endpoints.accounts.get_user_ip") as mock_ip:
            mock_ip.return_value = "127.0.121.1"
            with mock.patch("app.api.api_v1.endpoints.accounts.get_user_location_from_ip") as mock_location:
                mock_location.return_value = "maitama"
                response = self.client.post("/accounts/1121221492/transactions",
                                            json={
                                                **_CREDIT_TRANSACTION_TEST_DATA, "transaction_amount": 12000},
                                            headers=self.headers)
                self.assertEqual(response.status_code, 404)

    def test_get_all_transaction_with_description_as_search_param_and_paging(self) -> None:
        """/accounts/{id}/transaction debit account"""

        response = self.client.get("/accounts/1123012492/transactions?search=salary&page_mumber=1&limit=2",
                                   headers=self.headers)
        actual = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(actual['all_transactions']), 2)
        self.assertEqual(actual["next_page"], 2)
        self.assertEqual(actual["total_count"], 3)

    def test_get_all_transaction_with_description_as_search_param_and_paging_more(self) -> None:
        """/accounts/{id}/transaction debit account"""

        response = self.client.get("/accounts/1123012492/transactions?search=salary&page_mumber=1&limit=4",
                                   headers=self.headers)
        actual = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(actual["all_transactions"]), 3)
        self.assertEqual(actual["next_page"], 1)
        self.assertEqual(actual["total_count"], 3)

    def doCleanups(self) -> None:
        self.session.db_session.close()


if __name__ == '__main__':
    unittest.main()