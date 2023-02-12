# File used for various helper methods, including decorators

import functools
import math
from flask import request
from api.services import token_service
from api.exceptions import NotLoggedInError, InvalidPageNumber
from api.config import API_MAX_PAGES
from api.schemas import PageInfoSchema

page_info_schema = PageInfoSchema()


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


def generate_page_info(query_params: dict, count: int):
    page = query_params["page"]
    limit = query_params["limit"]
    max_page = math.ceil(count / limit)

    if page > max_page or page > API_MAX_PAGES:
        raise InvalidPageNumber

    return page_info_schema.dump(
        {"limit": limit, "page": page, "count": count, "max_page": max_page}
    )
