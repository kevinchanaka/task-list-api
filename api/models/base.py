import sqlalchemy as db


class BaseModel:
    def __init__(self, table_name: str, engine: db.engine.Engine):
        metadata = db.MetaData()
        self.engine = engine
        self.table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)

    @staticmethod
    def __to_dict__(data):
        if data is None:
            return {}
        if type(data) is list:
            return [dict(r) for r in data]
        return dict(data)

    def list(self, obj: dict = {}):
        """
        Lists records in table based on match when compared to input dictionary
        Returns list of records, this list will be empty if no records match
        """
        query = self.table.select()
        for k, v in obj.items():
            query = query.where(getattr(self.table.c, k) == v)
        with self.engine.connect() as conn:
            result = conn.execute(query).mappings().all()
            return self.__to_dict__(result)

    def get(self, obj: dict):
        """
        Fetches record in table based on match when compared to input dictionary
        Returns fetched record or None
        """
        query = self.table.select()
        for k, v in obj.items():
            query = query.where(getattr(self.table.c, k) == v)
        with self.engine.connect() as conn:
            result = conn.execute(query).mappings().first()
            return self.__to_dict__(result)

    def get_by_id(self, id: str):
        """
        Fetches record in table based on ID
        Returns fetched record or None
        """
        query = self.table.select().where(self.table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(query).mappings().first()
            return self.__to_dict__(result)

    def add(self, data: dict):
        """
        Populates additional data to dictionary
        Returns True if add was successful, False otherwise
        """
        query = self.table.insert().values(**data)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)

    def delete(self, obj: dict):
        """
        Deletes record from DB based on match when compared to input dictionary
        Returns True if delete was successful, False otherwise
        """
        if not obj:
            return False
        query = self.table.delete()
        for k, v in obj.items():
            query = query.where(getattr(self.table.c, k) == v)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)

    def delete_by_id(self, id: str):
        """
        Deletes record from DB based on ID
        Returns True if delete was successful, False otherwise
        """
        query = self.table.delete().where(self.table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)

    def update(self, obj: dict, data: dict):
        """
        Updates record from DB based on match when compared to input dictionary
        Returns True if update was successful, False otherwise
        """
        if not obj or not data:
            return False
        query = self.table.update()
        for k, v in obj.items():
            query = query.where(getattr(self.table.c, k) == v)
        query = query.values(**data)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)

    def update_by_id(self, id: str, data: dict):
        """
        Updates record from DB using ID
        Returns True if update was successful, False otherwise
        """
        query = self.table.update().where(self.table.c.id == id).values(**data)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)
