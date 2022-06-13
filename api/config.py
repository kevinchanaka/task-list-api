import os
from dotenv import load_dotenv
from datetime import timedelta

NAME_LENGTH = 60
DEFAULT_LENGTH = 255

ENV = os.getenv("ENV", "development")

if ENV != "production":
    load_dotenv()


PORT = os.getenv("PORT", 5000)

NAME_LENGTH = 60
UUID_LENGTH = 36
HASH_LENGTH = 102
TIMESTAMP_LENGTH = 11
DEFAULT_LENGTH = 255

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_TEST_PORT = os.getenv("DB_TEST_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CONNECTION_STRING = "mysql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
)

SQLALCHEMY_ENGINE_STRING = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
)

DB_ADMIN_USER = os.getenv("DB_ADMIN_USER")
DB_ADMIN_PASSWORD = os.getenv("DB_ADMIN_PASSWORD")

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
ACCESS_TOKEN_EXPIRY = timedelta(minutes=5)
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
REFRESH_TOKEN_EXPIRY = timedelta(days=1)
