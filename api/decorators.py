import functools
from flask import request
from api.services.token import token_service
from api.exceptions import ValidationError, NotLoggedInError
from api.models import Model


def validator(model: Model):
    def validator_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            payload = request.get_json()
            errors = model.validate(payload)
            if errors:
                print(errors)
                raise ValidationError
            else:
                return func(payload=payload, *args, **kwargs)

        return wrapper

    return validator_decorator


def refresh_token_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        refresh_token = request.cookies.get("refresh_token", None)
        if refresh_token:
            return func(refresh_token=refresh_token, *args, **kwargs)
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
        return func(user_id=user_id, *args, **kwargs)

    return wrapper
