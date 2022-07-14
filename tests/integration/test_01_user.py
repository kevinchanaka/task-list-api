from unittest import TestCase
from tests.integration import clean_up_db_table, create_test_client
from tests.data import test_user

PATH = "/api/v1/users"


class TestUser(TestCase):
    @classmethod
    def setUpClass(cls):
        clean_up_db_table("tasks")
        clean_up_db_table("users")
        cls.app = create_test_client()

    def setUp(self):
        res = self.app.post(f"{PATH}/register", json=test_user)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json()["user"], dict)

    def tearDown(self):
        clean_up_db_table("users")

    def test_01_login_correct_creds(self):
        payload = {"email": test_user["email"], "password": test_user["password"]}
        res = self.app.post(f"{PATH}/login", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.headers.get_all("Set-Cookie")), 2)

    def test_02_login_incorrect_creds(self):
        payload = {"email": test_user["email"], "password": "foo"}
        res = self.app.post(f"{PATH}/login", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(len(res.headers.get_all("Set-Cookie")), 0)

    def test_03_refresh_credentials(self):
        payload = {"email": test_user["email"], "password": test_user["password"]}
        res = self.app.post(f"{PATH}/login", json=payload)
        token_res = self.app.post(f"{PATH}/token", headers=res.headers)
        self.assertEqual(len(token_res.headers.get_all("Set-Cookie")), 1)

    def test_04_logout_invalidate_token(self):
        payload = {"email": test_user["email"], "password": test_user["password"]}
        res = self.app.post(f"{PATH}/login", json=payload)
        self.app.post(f"{PATH}/logout", headers=res.headers)
        token_res = self.app.post(f"{PATH}/token", headers=res.headers)
        self.assertEqual(len(token_res.headers.get_all("Set-Cookie")), 0)
        self.assertEqual(token_res.status_code, 401)
