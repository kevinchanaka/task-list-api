import functools
from cerberus import Validator
from flask import request
from api.services.token import token_service
from api.exceptions import ValidationError, NotLoggedInError


def validator(schema: dict):
    data_valid = Validator(schema)

    def validator_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if data_valid(request.get_json()):
                return func(*args, **kwargs)
            else:
                raise ValidationError

        return wrapper

    return validator_decorator


def refresh_token_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if request.cookies.get("refresh_token"):
            return func(*args, **kwargs)
        else:
            raise NotLoggedInError

    return wrapper


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.cookies.get("access_token")
        if not access_token:
            raise NotLoggedInError

        payload = token_service.verify_access_token(access_token)
        user_id: str = payload["user_id"]
        return func(user_id, *args, **kwargs)

    return wrapper
