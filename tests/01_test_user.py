from tests import BaseTestClass
from tests.data import test_user

PATH = "/api/v1/users"


class TestUser(BaseTestClass):
    def setUp(self):
        super().setUp(auth=False)
        res = self.client.post(f"{PATH}/register", json=test_user)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(test_user["name"], data["user"]["name"])
        self.assertEqual(test_user["email"], data["user"]["email"])

    def test_user_01_login_correct_creds(self):
        payload = {"email": test_user["email"], "password": test_user["password"]}
        res = self.client.post(f"{PATH}/login", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.headers.get_all("Set-Cookie")), 2)

    def test_user_02_login_incorrect_creds(self):
        payload = {"email": test_user["email"], "password": "foo"}
        res = self.client.post(f"{PATH}/login", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(len(res.headers.get_all("Set-Cookie")), 0)

    def test_user_03_refresh_credentials(self):
        payload = {"email": test_user["email"], "password": test_user["password"]}
        res = self.client.post(f"{PATH}/login", json=payload)
        token_res = self.client.post(f"{PATH}/token", headers=res.headers)
        self.assertEqual(len(token_res.headers.get_all("Set-Cookie")), 1)

    def test_user_04_logout_invalidate_token(self):
        payload = {"email": test_user["email"], "password": test_user["password"]}
        res = self.client.post(f"{PATH}/login", json=payload)
        self.client.post(f"{PATH}/logout", headers=res.headers)
        token_res = self.client.post(f"{PATH}/token", headers=res.headers)
        self.assertEqual(len(token_res.headers.get_all("Set-Cookie")), 0)
        self.assertEqual(token_res.status_code, 401)
