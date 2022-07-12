from flask import Blueprint, request, make_response, jsonify
from api.services import user_service
from api.decorators import validator, refresh_token_required
from api.config import (
    ACCESS_TOKEN_EXPIRY,
    REFRESH_TOKEN_EXPIRY,
)
from api.models import User, UserLogin

bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@bp.route("/register", methods=["POST"])
@validator(User)
def register(payload):
    user_obj = User.deserialise_public(**payload)
    user = user_service.register_user(user_obj)
    return jsonify(user)


@bp.route("/login", methods=["POST"])
@validator(UserLogin)
def login(payload):
    user, access_token, refresh_token = user_service.login_user(
        payload["email"], payload["password"]
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
