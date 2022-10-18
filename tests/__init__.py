import sqlalchemy as sa
import logging
from unittest import TestCase
from api.config import DB_CONNECTION_STRING
from app import init_app
from flask.testing import FlaskClient
from tests.data import test_user, tables


def clean_tables():
    engine = sa.create_engine(DB_CONNECTION_STRING)
    for table_name in tables:
        table = sa.Table(table_name, sa.MetaData(), autoload=True, autoload_with=engine)
        query = table.delete()
        with engine.connect() as conn:
            conn.execute(query)


class TestClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        headers = kwargs.pop("headers", None)
        if headers:
            self.headers = headers
        else:
            self.headers = None
        super(TestClient, self).__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        if self.headers:
            kwargs["headers"] = self.headers
        return super().open(*args, **kwargs)


class BaseTestClass(TestCase):
    app_context = None
    client = None

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.INFO)
        app = init_app(testing=True)
        app.test_client_class = TestClient
        cls.app_context = app.app_context()
        cls.client = app.test_client()

    def setUp(self, auth=True):
        clean_tables()
        if auth:
            self.client.post("/api/v1/users/register", json=test_user)
            self.client.post(
                "/api/v1/users/login",
                json={"email": test_user["email"], "password": test_user["password"]},
            )

    def tearDown(self):
        clean_tables()
