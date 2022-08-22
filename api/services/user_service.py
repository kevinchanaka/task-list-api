import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from api.database import user_db
from api.services import token_service
from api.exceptions import InvalidUsageError
from api.schemas import user_schema, user_output_schema
from api.models import User


def register_user(user: User):
    exists = user_db.get(email=user.email)
    if exists:
        raise InvalidUsageError("User already registered")

    user.id = uuid.uuid4()
    user.password_hash = generate_password_hash(user.password)
    user.password = None
    user_db.add(user_schema.dump(user))
    return user_output_schema.dump(user)


def login_user(email: str, password: str):
    user: User = user_db.get(email=email)

    if not user or not check_password_hash(user.password_hash, password):
        raise InvalidUsageError("Email or password is incorrect")

    access_token = token_service.generate_access_token(str(user.id))
    refresh_token = token_service.generate_refresh_token(str(user.id))
    return (
        user_output_schema.dump(user),
        access_token,
        refresh_token,
    )


def logout_user(token: str):
    if token:
        token_service.delete_refresh_token(token)


def refresh_credentials(refresh_token: str):
    payload = token_service.verify_refresh_token(refresh_token)
    access_token = token_service.generate_access_token(payload["user_id"])
    return access_token
