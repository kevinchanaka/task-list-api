import sqlalchemy as db
from api.config import DB_CONNECTION_STRING


metadata = db.MetaData()
engine = db.create_engine(DB_CONNECTION_STRING)


class Database:
    def __init__(self, table_name: str):
        self.table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)

    def list(self, **filter):
        """
        Lists records in table based on match when compared to input dictionary
        Returns list of records, this list will be empty if no records match
        """
        query = self.table.select()
        for k, v in filter.items():
            query = query.where(getattr(self.table.c, k) == v)
        with engine.connect() as conn:
            return conn.execute(query).mappings().all()

    def list_or(self, field_name: str, field_values):
        query = self.table.select().where(
            getattr(self.table.c, field_name).in_(field_values)
        )
        with engine.connect() as conn:
            return conn.execute(query).mappings().all()

    def list_relationship(self, relation_name: str, id: str):
        """
        Lists records in mapping table, mainly intended for many-to-many relationships
        These relationships are stored in the 'db_relationships' variable
        """
        relation = db_relationships[relation_name]
        mapping_db = relation["mapping_db"]
        filter_dict = {}
        filter_dict[relation["local_field"]] = id
        results = mapping_db.list(**filter_dict)  # type: ignore[attr-defined]
        result_ids = [x[relation["relation_field"]] for x in results]
        query = self.table.select().where(getattr(self.table.c, "id").in_(result_ids))
        with engine.connect() as conn:
            return conn.execute(query).mappings().all()

    def get(self, **filter):
        """
        Fetches record in table based on match when compared to input dictionary
        Returns fetched record or None
        """
        query = self.table.select()
        for k, v in filter.items():
            query = query.where(getattr(self.table.c, k) == v)
        with engine.connect() as conn:
            return conn.execute(query).mappings().first()

    def add(self, data):
        """
        Populates additional data to dictionary
        Returns True if add was successful, False otherwise
        """
        query = self.table.insert().values(data)
        with engine.connect() as conn:
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
        with engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)

    def update(self, data, **filter):
        """
        Updates record from DB based on match when compared to input dictionary
        Returns True if update was successful, False otherwise
        """
        query = self.table.update()
        for k, v in filter.items():
            query = query.where(getattr(self.table.c, k) == v)
        query = query.values(data)
        with engine.connect() as conn:
            result = conn.execute(query)
            return bool(result.rowcount)


task_db = Database(table_name="tasks")
user_db = Database(table_name="users")
token_db = Database(table_name="refresh_tokens")
label_db = Database(table_name="labels")
task_label_db = Database(table_name="tasks_labels_mapping")

db_relationships = {
    "task_labels": {
        "relation_db": label_db,
        "mapping_db": task_label_db,
        "local_field": "task_id",
        "relation_field": "label_id",
    }
}
