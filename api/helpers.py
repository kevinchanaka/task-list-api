# File used for various helper methods, including decorators

import functools
import math
import logging
from flask import request
from marshmallow import fields
from api.services import token_service
from api.exceptions import NotLoggedInError, InvalidPageNumber
from api.config import API_MAX_PAGES
from api.schemas import PageInfoSchema, BaseSchema
from api.exceptions import QueryError
from api.models import PageInfo

logger = logging.getLogger()
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
        kwargs["user_id"] = payload["user_id"]
        return func(*args, **kwargs)

    return wrapper


def get_page_info(page_info: PageInfo, count: int):
    if count == 0:
        max_page = 1
    else:
        max_page = math.ceil(count / page_info.limit)

    if page_info.page > max_page or page_info.page > API_MAX_PAGES:
        raise InvalidPageNumber

    return {
        "count": count,
        "max_page": max_page,
        "limit": page_info.limit,
        "page": page_info.page,
    }


def parse_request_body(schema: BaseSchema):
    def decorator_parse_request_body(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            body = request.get_json()
            parsed_data = schema.load_validate(**body)
            return func(data=parsed_data, *args, **kwargs)

        return wrapper

    return decorator_parse_request_body


def parse_request_params(schema: BaseSchema):
    def decorator_parse_request_params(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            params = {}
            for k in request.args.keys():
                schema_field = schema.fields.get(k)
                if schema_field is None:
                    raise QueryError
                value = request.args.getlist(k)
                if isinstance(schema_field, fields.List):
                    params[k] = value
                elif len(value) > 1:
                    raise QueryError
                else:
                    params[k] = value[0]
            processed_params = schema.load_validate(**params)
            return func(params=processed_params, *args, **kwargs)

        return wrapper

    return decorator_parse_request_params
