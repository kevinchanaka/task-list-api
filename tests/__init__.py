import sqlalchemy as db
from api.config import DB_CONNECTION_STRING

# from app import init_app
from flask.testing import FlaskClient


class MockModel:
    def __init__(self):
        self.data_list = []

    def add(self, data):
        self.data_list.append(data)
        return data

    def findByEmail(self, addr):
        elements = [x for x in self.data_list if x["email"] == addr]
        if len(elements) == 0:
            return {}
        return elements[0]

    def get(self, field):
        for i in range(0, len(self.data_list)):
            for v in self.data_list[i].values():
                if v == field:
                    return self.data_list[i]
        return {}

    def delete(self, field):
        self.data_list = [x for x in self.data_list if field not in x.values()]

    def list(self):
        return self.data_list

    def update(self, data):
        for i in range(0, len(self.data_list)):
            if data["id"] == self.data_list[i]["id"]:
                self.data_list[i].update(data)
        return data


def clean_up_db_table(table_name: str):
    engine = db.create_engine(DB_CONNECTION_STRING)
    table = db.Table(table_name, db.MetaData(), autoload=True, autoload_with=engine)
    query = table.select().delete()
    with engine.connect() as conn:
        conn.execute(query)


# Need a function to setup and login as user to test protected endpoints
class CustomClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        self.headers = {"content-type": "application/json"}
        super(CustomClient, self).__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        kwargs["headers"] = self.headers
        return super().open(*args, **kwargs)


# def app():
#    app = init_app(testing=True)
#    yield app


# def client(app):
#    app.test_client_class = CustomClient
#    return app.test_client()
