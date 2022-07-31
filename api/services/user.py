import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from api.database import user_db
from api.services.token import token_service
from api.exceptions import InvalidUsageError
from api.models import User, user_output_schema


class UserService:
    def register_user(self, user: User):
        exists = user_db.get(email=user.email)
        if exists:
            raise InvalidUsageError("User already registered")

        user.id = uuid.uuid4()
        user.password_hash = generate_password_hash(user.password)
        user.password = None
        user_db.add(user)
        return {
            "user": user_output_schema.dump(user),
            "message": "User registered",
        }

    def login_user(self, email: str, password: str):
        user: User = user_db.get(email=email)
        print(user)
        if not user or not check_password_hash(user.password_hash, password):
            raise InvalidUsageError("Email or password is incorrect")

        access_token = token_service.generate_access_token(str(user.id))
        refresh_token = token_service.generate_refresh_token(str(user.id))
        return (
            {"user": user_output_schema.dump(user)},
            access_token,
            refresh_token,
        )

    def logout_user(self, token: str):
        if token:
            token_service.delete_refresh_token(token)

        return {"message": "User logged out"}

    def refresh_credentials(self, refresh_token: str):
        payload = token_service.verify_refresh_token(refresh_token)
        access_token = token_service.generate_access_token(payload["user_id"])
        return {"message": "Token refreshed"}, access_token
