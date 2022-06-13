# Test cases
# Can create new user
# Can login as new user
# Can logout
# Can refresh session
from unittest import TestCase, mock
from tests import MockModel
from tests.data import users
from api.services import user_service


class TestUserService(TestCase):
    def setUp(self):

        self.user_model_mock = mock.patch(
            "api.services.user.user_model", new_callable=MockModel
        )
        self.token_model_mock = mock.patch(
            "api.services.token.token_model", new_callable=MockModel
        )
        self.user_model_mock.start()
        self.token_model_mock.start()

    def tearDown(self):
        self.user_model_mock.stop()
        self.token_model_mock.stop()

    def assert_user(self, data: dict):
        self.assertIsInstance(data, dict)
        self.assertIn("user", data)
        user = data["user"]
        self.assertNotIn("password_hash", user)
        self.assertNotIn("password", user)
        self.assertIn("id", user)
        self.assertEqual(users[0]["name"], user["name"])
        self.assertEqual(users[0]["email"], user["email"])

    def test_01_register_user(self):
        ret, err = user_service.register_user(users[0])
        self.assert_user(ret)
        self.assertIsNone(err)

    def test_02_login_user(self):
        # user_model.add({"id": "234", **Data.users[0]})  # add user object to db
        user_service.register_user(users[0])
        ret, err = user_service.login_user(
            {"email": users[0]["email"], "password": users[0]["password"]}
        )
        self.assert_user(ret)
        self.assertIsNone(err)
        self.assertIn("access_token", ret)
        self.assertIn("refresh_token", ret)

    def test_03_refresh_credentials(self):
        user_service.register_user(users[0])
        data, _ = user_service.login_user(
            {"email": users[0]["email"], "password": users[0]["password"]}
        )
        ret, err = user_service.refresh_credentials(data["refresh_token"])
        self.assertIsNone(err)
        self.assertIn("access_token", ret)

    def test_04_logout_user(self):
        user_service.register_user(users[0])
        data, _ = user_service.login_user(
            {"email": users[0]["email"], "password": users[0]["password"]}
        )
        msg = user_service.logout_user(data["refresh_token"])
        self.assertIsInstance(msg, str)
