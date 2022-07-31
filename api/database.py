import sqlalchemy as db
from api.config import DB_CONNECTION_STRING
from api.models import (
    BaseSchema,
    task_schema,
    user_schema,
    token_schema,
)

engine = db.create_engine(DB_CONNECTION_STRING)


class Database:
    def __init__(self, table_name: str, engine: db.engine.Engine, schema: BaseSchema):
        metadata = db.MetaData()
        self.engine = engine
        self.table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
        self.schema = schema

    def list(self, **filter):
        """
        Lists records in table based on match when compared to input dictionary
        Returns list of records, this list will be empty if no records match
        """
        query = self.table.select()
        for k, v in filter.items():
            query = query.where(getattr(self.table.c, k) == v)
        with self.engine.connect() as conn:
            result = conn.execute(query).mappings().all()
            return [self.schema.load(r) for r in result]

    def get(self, **filter):
        """
        Fetches record in table based on match when compared to input dictionary
        Returns fetched record or None
        """
        query = self.table.select()
        for k, v in filter.items():
            query = query.where(getattr(self.table.c, k) == v)
        with self.engine.connect() as conn:
            result = conn.execute(query).mappings().first()
            if result is None:
                return None
            return self.schema.load(result)

    def add(self, obj):
        """
        Populates additional data to dictionary
        Returns True if add was successful, False otherwise
        """
        query = self.table.insert().values(self.schema.dump(obj))
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)

    def delete(self, **filter):
        """
        Deletes record from DB based on match when compared to input dictionary
        Returns True if delete was successful, False otherwise
        """
        if not filter:
            return False
        query = self.table.delete()
        for k, v in filter.items():
            query = query.where(getattr(self.table.c, k) == v)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)

    def update(self, obj, **filter):
        """
        Updates record from DB based on match when compared to input dictionary
        Returns True if update was successful, False otherwise
        """
        query = self.table.update()
        for k, v in filter.items():
            query = query.where(getattr(self.table.c, k) == v)
        query = query.values(self.schema.dump(obj))
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)


task_db = Database(table_name="tasks", engine=engine, schema=task_schema)
user_db = Database(table_name="users", engine=engine, schema=user_schema)
token_db = Database(table_name="refresh_tokens", engine=engine, schema=token_schema)
