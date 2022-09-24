import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from api.services import token_service
from api.exceptions import InvalidUsageError
from api.models import User, db
from sqlalchemy import select


def register_user(user: User):
    query = select(User).where(User.email == user.email)
    result = db.session.execute(query).scalars().first()
    if result:
        raise InvalidUsageError("User already registered")

    user.id = uuid.uuid4()
    user.password_hash = generate_password_hash(user.password)
    user.password = None
    db.session.add(user)
    db.session.commit()


def login_user(user: User):
    query = select(User).where(User.email == user.email)
    user_obj = db.session.execute(query).scalars().first()
    if not user_obj or not check_password_hash(user_obj.password_hash, user.password):
        raise InvalidUsageError("Email or password is incorrect")

    user.password = None

    access_token = token_service.generate_access_token(str(user_obj.id))
    refresh_token = token_service.generate_refresh_token(str(user_obj.id))
    return (
        user_obj,
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
