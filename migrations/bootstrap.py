# Script to bootstrap database
import sqlalchemy as db

from api.config import DB_NAME, DB_USER, DB_PASSWORD, DB_ADMIN_CONNECTION_STRING


engine = db.create_engine(DB_ADMIN_CONNECTION_STRING)

with engine.connect() as conn:
    conn.execute(db.text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
    conn.execute(
        db.text(
            f"CREATE USER IF NOT EXISTS '{DB_USER}'@'%' IDENTIFIED BY '{DB_PASSWORD}'"
        )
    )
    conn.execute(db.text(f"GRANT ALL ON {DB_NAME}.* TO '{DB_USER}'@'%'"))
