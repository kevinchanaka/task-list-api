import sqlalchemy as db
from api.config import DB_CONNECTION_STRING
from api.models.base import BaseModel

engine = db.create_engine(DB_CONNECTION_STRING)

task_model = BaseModel(table_name="tasks", engine=engine)
user_model = BaseModel(table_name="users", engine=engine)
token_model = BaseModel(table_name="refresh_tokens", engine=engine)
