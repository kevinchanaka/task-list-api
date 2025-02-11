from flask import Blueprint, request, make_response, jsonify
from api.services import user_service
from api.helpers import refresh_token_required, parse_request_body
from api.config import (
    ACCESS_TOKEN_EXPIRY,
    REFRESH_TOKEN_EXPIRY,
)
from api.schemas import UserSchema

bp = Blueprint("users", __name__, url_prefix="/api/v1/users")

user_register_schema = UserSchema(
    exclude=("password_hash", "id"), load_only=("password",)
)
user_login_schema = UserSchema(exclude=("id", "name", "password_hash"))
user_output_schema = UserSchema(exclude=("password_hash", "password"))


@bp.route("/register", methods=["POST"])
@parse_request_body(user_register_schema)
def register(data):
    user_service.register_user(data)
    return jsonify(
        {"user": user_output_schema.dump(data), "message": "User registered"}
    )


@bp.route("/login", methods=["POST"])
@parse_request_body(user_login_schema)
def login(data):
    user, access_token, refresh_token = user_service.login_user(data)
    res = make_response({"user": user_output_schema.dump(user)})
    res.set_cookie(
        "access_token",
        access_token,
        max_age=ACCESS_TOKEN_EXPIRY,
        httponly=True,
    )
    res.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=REFRESH_TOKEN_EXPIRY,
        httponly=True,
    )
    return res


@bp.route("/logout", methods=["POST"])
def logout():
    user_service.logout_user(request.cookies.get("refresh_token"))
    res = make_response({"message": "User logged out"})
    res.delete_cookie("access_token")
    res.delete_cookie("refresh_token")
    return res


@bp.route("/token", methods=["POST"])
@refresh_token_required
def token(refresh_token):
    access_token = user_service.refresh_credentials(refresh_token)
    res = make_response({"message": "Token refreshed"})
    res.set_cookie(
        "access_token",
        access_token,
        max_age=ACCESS_TOKEN_EXPIRY,
        httponly=True,
    )
    return res
