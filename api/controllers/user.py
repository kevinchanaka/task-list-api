from flask import Blueprint, request, make_response, jsonify
from api.services import user_service
from api.helpers import refresh_token_required
from api.config import (
    ACCESS_TOKEN_EXPIRY,
    REFRESH_TOKEN_EXPIRY,
)
from api.models import User, user_login_schema, user_register_schema

bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@bp.route("/register", methods=["POST"])
def register():
    payload = request.get_json()
    user_obj = user_register_schema.load_validate(**payload)
    user = user_service.register_user(user_obj)
    return jsonify(user)


@bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json()
    user_obj: User = user_login_schema.load_validate(**payload)
    user, access_token, refresh_token = user_service.login_user(
        user_obj.email, user_obj.password
    )
    res = make_response(user)
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
    ret = user_service.logout_user(request.cookies.get("refresh_token"))
    res = make_response(ret)
    res.delete_cookie("access_token")
    res.delete_cookie("refresh_token")
    return res


@bp.route("/token", methods=["POST"])
@refresh_token_required
def token(refresh_token):
    msg, access_token = user_service.refresh_credentials(refresh_token)
    res = make_response(msg)
    res.set_cookie(
        "access_token",
        access_token,
        max_age=ACCESS_TOKEN_EXPIRY,
        httponly=True,
    )
    return res
