import sqlalchemy as db
from api.config import DB_CONNECTION_STRING
from api.models import Model, Task, Token, User

engine = db.create_engine(DB_CONNECTION_STRING)


class Database:
    def __init__(self, table_name: str, engine: db.engine.Engine, model: Model):
        metadata = db.MetaData()
        self.engine = engine
        self.table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
        self.model = model

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
            return [self.model.deserialise(**r) for r in result]

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
            return self.model.deserialise(**result)

    def add(self, obj: Model):
        """
        Populates additional data to dictionary
        Returns True if add was successful, False otherwise
        """
        query = self.table.insert().values(obj.serialise())
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

    def update(self, obj: Model, **filter):
        """
        Updates record from DB based on match when compared to input dictionary
        Returns True if update was successful, False otherwise
        """
        query = self.table.update()
        for k, v in filter.items():
            query = query.where(getattr(self.table.c, k) == v)
        query = query.values(obj.serialise())
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)


task_db = Database(table_name="tasks", engine=engine, model=Task)
user_db = Database(table_name="users", engine=engine, model=User)
token_db = Database(table_name="refresh_tokens", engine=engine, model=Token)
