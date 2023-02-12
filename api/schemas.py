from typing import Callable
from marshmallow import fields, validate, Schema, post_dump, post_load, exceptions
from api.config import NAME_LENGTH, DEFAULT_LENGTH
from api.exceptions import ValidationError, QueryError
from api import models


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class BaseSchema(Schema):
    _model: Callable

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_load
    def convert_to_model(self, data, many, **kwargs):
        return self._model(**data)

    @post_dump
    def remove_none_fields(self, data, many, **kwargs):
        return {x: data[x] for x in data if data[x] is not None}

    def load_validate(self, **dict_data):
        try:
            data = self.load(dict_data)
        except exceptions.ValidationError as e:
            print(e)
            raise ValidationError
        return data


class BaseDictSchema(Schema):
    def load_validate(self, **dict_data):
        try:
            data = self.load(dict_data)
        except exceptions.ValidationError as e:
            print(e)
            raise ValidationError
        return data


class TaskSchema(BaseSchema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=NAME_LENGTH))
    description = fields.Str(
        required=True, validate=validate.Length(min=1, max=DEFAULT_LENGTH)
    )
    user_id = fields.UUID(required=True)
    completed = fields.Boolean(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    labels = fields.List(fields.Nested("LabelSchema", only=("id", "name", "colour")))

    _model = models.Task


class TaskLabelSchema(BaseDictSchema):
    labels = fields.List(fields.UUID)


class TokenSchema(Schema):
    token = fields.Str()
    expiry = fields.Int()

    _model = models.Token


class UserSchema(BaseSchema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=NAME_LENGTH))
    email = fields.Email(
        required=True, validate=validate.Length(min=1, max=NAME_LENGTH)
    )
    password = fields.Str(
        required=True, validate=validate.Length(min=1, max=NAME_LENGTH)
    )
    password_hash = fields.Str(required=True)

    _model = models.User


class LabelSchema(BaseSchema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=NAME_LENGTH))
    colour = fields.Str(required=True, validate=validate.Length(min=7, max=7))
    user_id = fields.UUID(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    _model = models.Label


class QueryParamsSchema(Schema):
    limit = fields.Int(load_default=10)
    page = fields.Int(load_default=1)

    def load_validate(self, **dict_data):
        try:
            data = self.load(dict_data)
        except exceptions.ValidationError as e:
            print(e)
            raise QueryError
        return data


class TaskParamsSchema(QueryParamsSchema):
    labels = fields.List(fields.UUID, load_default=[])


class PageInfoSchema(Schema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    limit = fields.Int()
    page = fields.Int()
    count = fields.Int()
    max_page = fields.Int()
