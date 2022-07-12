from unittest import TestCase, mock
from tests.unit import MockDatabase
from tests.data import test_user
from api.services import user_service
from api.models import User


class TestUserService(TestCase):
    def setUp(self):
        self.user_db_mock = mock.patch(
            "api.services.user.user_db", new_callable=MockDatabase
        )
        self.token_db_mock = mock.patch(
            "api.services.token.token_db", new_callable=MockDatabase
        )
        self.user_db = self.user_db_mock.start()
        self.token_db = self.token_db_mock.start()
        self.test_user_obj = User.deserialise_public(**test_user)

    def tearDown(self):
        self.user_db_mock.stop()
        self.token_db_mock.stop()

    def assert_user(self, data):
        self.assertIn("user", data)
        user = data["user"]
        self.assertNotIn("password_hash", user)
        self.assertNotIn("password", user)
        self.assertIn("id", user)
        self.assertEqual(test_user["name"], user["name"])
        self.assertEqual(test_user["email"], user["email"])

    def test_01_register_user(self):
        ret = user_service.register_user(self.test_user_obj)
        self.assert_user(ret)

    def test_02_login_user(self):
        user_service.register_user(self.test_user_obj)
        ret, access_token, refresh_token = user_service.login_user(
            email=self.test_user_obj.email, password=test_user["password"]
        )
        self.assert_user(ret)
        self.assertIsInstance(access_token, str)
        self.assertIsInstance(refresh_token, str)

    def test_03_refresh_credentials(self):
        user_service.register_user(self.test_user_obj)
        _, _, refresh_token = user_service.login_user(
            email=self.test_user_obj.email, password=test_user["password"]
        )
        _, access_token = user_service.refresh_credentials(refresh_token)
        self.assertIsInstance(access_token, str)

    def test_04_logout_user(self):
        user_service.register_user(self.test_user_obj)
        _, _, refresh_token = user_service.login_user(
            email=self.test_user_obj.email, password=test_user["password"]
        )
        ret = user_service.logout_user(refresh_token)
        self.assertIsInstance(ret["message"], str)
