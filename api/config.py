import os
from dotenv import load_dotenv
from datetime import timedelta

ENV = os.getenv("ENV", "development")

if ENV != "production":
    load_dotenv()

if ENV == "test":
    DB_PORT = os.getenv("DB_TEST_PORT")
else:
    DB_PORT = os.getenv("DB_PORT")

PORT = os.getenv("PORT", 5000)

NAME_LENGTH = 60
UUID_LENGTH = 36
HASH_LENGTH = 102
TIMESTAMP_LENGTH = 11
DEFAULT_LENGTH = 255

API_MAX_PAGES = 100
API_DEFAULT_LIMIT = 10
API_COGNITO_USER_POOL = os.getenv("API_COGNITO_USER_POOL")
API_COGNITO_CLIENT_ID = os.getenv("API_COGNITO_CLIENT_ID")

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_ADMIN_USER = os.getenv("DB_ADMIN_USER")
DB_ADMIN_PASSWORD = os.getenv("DB_ADMIN_PASSWORD")

DB_CONNECTION_STRING = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DB_ADMIN_CONNECTION_STRING = (
    f"mysql://{DB_ADMIN_USER}:{DB_ADMIN_PASSWORD}@{DB_HOST}:{DB_PORT}"
)

SQLALCHEMY_ENGINE_STRING = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
)

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
ACCESS_TOKEN_EXPIRY = timedelta(minutes=60)  # timedelta(minutes=5)
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
REFRESH_TOKEN_EXPIRY = timedelta(days=1)

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)-8s "
            + "[%(name)s:%(filename)s:%(lineno)d] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
        }
    },
    "loggers": {"": {"level": "DEBUG", "handlers": ["console"]}},
}
