"""Test for user"""
import unittest
from unittest import mock

from fastapi.testclient import TestClient

from app import main
from app.api.depends import get_db
from app.api.api_v1.endpoints.test_mocks.user_api_mock import MockUserSession
from app.db.test_mocks.db_test_mock import override_get_db

main.app.dependency_overrides[get_db] = override_get_db

_CREATE_USER_TEST_DATA = {
    "first_name": "string",
    "last_name": "strom",
    "email": "string@gmail.com",
    "phone_number": "21034024",
    "password": "string@password"
}

_UPDATE_USER_TEST_DATA = {
    "first_name": "Sodiq",
    "last_name": "Kad",
    "email": "kad@gmail.com",
    "phone_number": "07029345",
    "password": "helloworld"
}


class BaseTest(unittest.TestCase):
    client = TestClient(main.app)
    session = None


class TestUser(BaseTest):
    """
    TestUser Class
    """

    def setUp(self) -> None:
        self.session = MockUserSession(list(override_get_db())[0])
        self.session.add_mock_data_to_db()

    def tearDown(self) -> None:
        self.session.clear_mock_db()

    def test_create_user(self) -> None:
        """/users create"""
        response = self.client.post("/users", json=_CREATE_USER_TEST_DATA)
        expected = {**_CREATE_USER_TEST_DATA}
        expected.__delitem__("password")
        actual = response.json()
        actual.__delitem__("id")
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(actual, expected)

    def test_get_user(self) -> None:
        """/users get"""
        response = self.client.get(
            "/users/1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f5")
        expected = {
            "id": '1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f5',
            "last_name": "Drey",
            "first_name": "Kad",
            "email": "kad@gmail.com",
            "phone_number": "07029345"
        }
        actual = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(actual, expected)

    def test_get_unavailable_user(self) -> None:
        """/users get"""
        response = self.client.get(
            "/users/1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f9")
        expected = {"Error": "user not found"}
        actual = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(actual, expected)

    def test_update_user(self) -> None:
        with mock.patch("app.api.api_v1.endpoints.user.get_current_active_user") as mock_current_user:
            mock_current_user.return_value = self.session.get_mock_data_from_db(
                self.session.data[0].id
            )
            response = self.client.put(
                "/users", json=_UPDATE_USER_TEST_DATA)
            expected = {
                "id": '1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f5',
                "last_name": "Drey",
                "first_name": "Kad",
                "email": "kad@gmail.com",
                "phone_number": "07029345"
            }
            actual = response.json()
            self.assertEqual(response.status_code, 202)
            self.assertDictEqual(actual, expected)

    def test_update_unavailable_user(self) -> None:
        with mock.patch("app.api.api_v1.endpoints.user.get_current_active_user") as mock_current_user:
            mock_current_user.return_value = None
            response = self.client.put(
                "/users", json={**_UPDATE_USER_TEST_DATA, "email": "tar@gmail.com"})
            expected = {
                "error_message": "An error occurred unable to update user"}
            actual = response.json()
            self.assertEqual(response.status_code, 400)
            self.assertDictEqual(actual, expected)

    def test_delete_user(self) -> None:
        """/users delete"""
        response = self.client.delete(
            "/users/1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f5")
        actual = response.json()
        expected = {"success": "user deleted successfully"}
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(actual, expected)

    def test_delete_unavailable_user(self) -> None:
        """/user delete unavailable"""
        response = self.client.delete(
            "/users/1a8d8791-946c-4fc4-8f5d-1b0c4f5ee2f8")
        actual = response.json()
        expected = {"Error": "unable to delete user not found"}
        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(actual, expected)

    def test_authenticate_user(self) -> None:
        """/users authentication"""
        response = self.client.post("/users/authenticate", json={
            "email": "kad@gmail.com",
            "password": "helloworld"
        })
        self.assertEqual(response.status_code, 200)

    def test_authenticate_user_fail(self) -> None:
        """/users authentication"""
        response = self.client.post("/users/authenticate", json={
            "email": "kad@gmail.com",
            "password": "helloworld@error"
        })
        self.assertEqual(response.status_code, 401)

    def doCleanups(self) -> None:
        self.session.db_session.close()


if __name__ == '__main__':
    unittest.main()