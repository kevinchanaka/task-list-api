import jwt
from datetime import datetime, timezone
from api.config import (
    ACCESS_TOKEN_SECRET,
    REFRESH_TOKEN_SECRET,
    ACCESS_TOKEN_EXPIRY,
    REFRESH_TOKEN_EXPIRY,
)
from api.database import token_db
from api.models import token_schema
from api.exceptions import InvalidTokenError


class TokenService:
    def generate_access_token(self, user_id: str):
        current_date = datetime.now(timezone.utc)
        payload = {
            "user_id": user_id,
            "exp": int((current_date + ACCESS_TOKEN_EXPIRY).timestamp()),
        }
        return jwt.encode(payload, ACCESS_TOKEN_SECRET, algorithm="HS256")

    def generate_refresh_token(self, user_id: str):
        current_date = datetime.now(timezone.utc)
        expiry = int((current_date + REFRESH_TOKEN_EXPIRY).timestamp())
        payload = {
            "user_id": user_id,
            "exp": expiry,
        }
        token = jwt.encode(payload, REFRESH_TOKEN_SECRET, algorithm="HS256")
        token_obj = token_schema.load({"token": token, "expiry": expiry})
        token_db.add(token_obj)
        return token

    def verify_access_token(self, token: str):
        try:
            return jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            raise InvalidTokenError

    def verify_refresh_token(self, token: str):
        if token_db.get(token=token):
            try:
                return jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=["HS256"])
            except jwt.exceptions.InvalidTokenError:
                raise InvalidTokenError

    def delete_refresh_token(self, token: str):
        token_db.delete(token=token)


token_service = TokenService()
