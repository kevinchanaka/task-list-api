# from tests.data import users
# from tests import clean_up_db_table


# def test_health(client):
#    res = client.get("/api/v1/health/").get_json()
#    assert res == {"message": "API is running!"}


# Test cases
# Can create new user
# Can login as new user
# Can logout
# Can refresh session
PATH = "/api/v1/users"


# class TestUser:
#    def tearDown(self):
#        clean_up_db_table("users")

#    def test_user_create(self, client):
#        res = client.post(f"{PATH}/register", json=users[0]).get_json()
#        print(res)
#        assert res["user"]["id"]
#        assert res["user"]["email"] == users[0]["email"]

#    def test_user_login(self, client):
#        res = client.post(f"{PATH}/login", json=users[0]).get_json()
#        print(res)
#        assert res["user"]["id"]
#        assert res["user"]["access_token"]
#        assert res["user"]["refresh_token"]
