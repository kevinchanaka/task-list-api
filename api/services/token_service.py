import jwt
from datetime import datetime, timezone
from api.config import (
    ACCESS_TOKEN_SECRET,
    REFRESH_TOKEN_SECRET,
    ACCESS_TOKEN_EXPIRY,
    REFRESH_TOKEN_EXPIRY,
)
from api.models import Token, db
from api.exceptions import InvalidTokenError
from sqlalchemy import select

# TODO: use Token model here


def generate_access_token(user_id: str):
    current_date = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "exp": int((current_date + ACCESS_TOKEN_EXPIRY).timestamp()),
    }
    return jwt.encode(payload, ACCESS_TOKEN_SECRET, algorithm="HS256")


def generate_refresh_token(user_id: str):
    current_date = datetime.now(timezone.utc)
    expiry = int((current_date + REFRESH_TOKEN_EXPIRY).timestamp())
    payload = {
        "user_id": user_id,
        "exp": expiry,
    }
    token = jwt.encode(payload, REFRESH_TOKEN_SECRET, algorithm="HS256")
    token_obj = Token(token=token, expiry=expiry)
    db.session.add(token_obj)
    db.session.commit()
    return token


def verify_access_token(token: str):
    try:
        return jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        raise InvalidTokenError


def verify_refresh_token(token: str):
    if db.session.execute(select(Token).where(Token.token == token)).scalars().first():
        try:
            return jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            raise InvalidTokenError


def delete_refresh_token(token: str):
    query = select(Token).where(Token.token == token)
    token = db.session.execute(query).scalars().first()
    if token:
        db.session.delete(token)
        db.session.commit()
