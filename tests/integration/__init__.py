import sqlalchemy as db
from api.config import DB_CONNECTION_STRING
from app import init_app
from flask.testing import FlaskClient

# from werkzeug.datastructures import Headers
from tests.data import test_user


def clean_up_db_table(table_name: str):
    engine = db.create_engine(DB_CONNECTION_STRING)
    table = db.Table(table_name, db.MetaData(), autoload=True, autoload_with=engine)
    query = table.delete()
    with engine.connect() as conn:
        conn.execute(query)


class TestClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        # if "headers" in kwargs:
        #    self.headers = kwargs.pop("headers")
        # else:
        #    self.headers = {"content-type": "application/json"}
        headers = kwargs.pop("headers", None)
        if headers:
            self.headers = headers
        else:
            self.headers = None
        super(TestClient, self).__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        # kwargs["headers"] = self.headers
        # print(kwargs["headers"])
        if self.headers:
            kwargs["headers"] = self.headers
        return super().open(*args, **kwargs)


def create_test_client():
    app = init_app(testing=True)
    app.test_client_class = TestClient
    return app.test_client()


def create_test_client_auth():
    app = init_app(testing=True)
    app.test_client_class = TestClient
    client = app.test_client()
    client.post("/api/v1/users/register", json=test_user)
    client.post(
        "/api/v1/users/login",
        json={"email": test_user["email"], "password": test_user["password"]},
    )
    # res.headers.pop("Content-Length")
    # foo = temp_client.post("/api/v1/users/token")
    return client
