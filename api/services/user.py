import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import user_model
from api.services.token import token_service
from api.exceptions import InvalidUsageError


class UserService:
    def __make_user__(self, data):
        return {
            "id": uuid.uuid4().__str__(),
            "name": data["name"],
            "password_hash": generate_password_hash(data["password"]),
            "email": data["email"],
        }

    def __remove_password_hash__(self, user: dict):
        return {k: user[k] for k in user.keys() if k != "password_hash"}

    def register_user(self, data):
        exists = user_model.get({"email": data["email"]})
        if exists:
            raise InvalidUsageError("User already registered")
        user = self.__make_user__(data)
        user_model.add(user)
        return {"user": self.__remove_password_hash__(user)}

    def login_user(self, data):
        user = user_model.get({"email": data["email"]})
        if not user or not check_password_hash(user["password_hash"], data["password"]):
            raise InvalidUsageError("Email or password is incorrect")
        tokens = {
            "access_token": token_service.generate_access_token(user["id"]),
            "refresh_token": token_service.generate_refresh_token(user["id"]),
        }
        return {"user": self.__remove_password_hash__(user)}, tokens

    def logout_user(self, token: str):
        if token:
            token_service.delete_refresh_token(token)
        return {"message": "User logged out"}

    def refresh_credentials(self, refresh_token: str):
        payload = token_service.verify_refresh_token(refresh_token)
        return {
            "access_token": token_service.generate_access_token(payload["user_id"])
        }, {"message": "Token refreshed"}
