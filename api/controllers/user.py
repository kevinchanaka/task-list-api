from flask import Blueprint, request, make_response, jsonify
from api.services import user_service
from api.decorators import validator, refresh_token_required
from api.config import (
    NAME_LENGTH,
    DEFAULT_LENGTH,
    ACCESS_TOKEN_EXPIRY,
    REFRESH_TOKEN_EXPIRY,
)

bp = Blueprint("users", __name__, url_prefix="/api/v1/users")

email_regex = "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"

user_register_schema = {
    "name": {"type": "string", "required": True, "maxlength": NAME_LENGTH},
    "email": {
        "type": "string",
        "regex": email_regex,
        "required": True,
        "maxlength": NAME_LENGTH,
    },
    "password": {"type": "string", "required": True, "maxlength": DEFAULT_LENGTH},
}

user_login_schema = {
    "email": {
        "type": "string",
        "regex": email_regex,
        "required": True,
        "maxlength": NAME_LENGTH,
    },
    "password": {"type": "string", "required": True, "maxlength": DEFAULT_LENGTH},
}


@bp.route("/register", methods=["POST"])
@validator(user_register_schema)
def register():
    data = request.get_json()
    user = user_service.register_user(data)
    return jsonify(user)


@bp.route("/login", methods=["POST"])
@validator(user_login_schema)
def login():
    data = request.get_json()
    user, tokens = user_service.login_user(data)
    res = make_response(user)
    res.set_cookie(
        "access_token",
        tokens["access_token"],
        max_age=ACCESS_TOKEN_EXPIRY,
        httponly=True,
    )
    res.set_cookie(
        "refresh_token",
        tokens["refresh_token"],
        max_age=REFRESH_TOKEN_EXPIRY,
        httponly=True,
    )
    return res


@bp.route("/logout", methods=["POST"])
def logout():
    ret = user_service.logout_user(request.cookies.get("refresh_token"))
    res = make_response(ret)
    res.delete_cookie("access_token")
    res.delete_cookie("refresh_token")
    return res


@bp.route("/token", methods=["POST"])
@refresh_token_required
def token():
    refresh_token = request.cookies["refresh_token"]
    token, msg = user_service.refresh_credentials(refresh_token)
    res = make_response(msg)
    res.set_cookie(
        "access_token",
        token["access_token"],
        max_age=ACCESS_TOKEN_EXPIRY,
        httponly=True,
    )
    return res
