from dataclasses import dataclass
from typing import Callable, Optional
from datetime import datetime
from marshmallow import Schema, fields, validate, post_dump, post_load, exceptions
from api.config import NAME_LENGTH, DEFAULT_LENGTH
from api.exceptions import ValidationError

# Creating this custom field as a workaround,
# as SQLAlchemy returns timestamp fields as formatted datetime objects
# Should ideally implement this with SQLAlchemy custom fields


class CustomDateTimeField(fields.DateTime):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime):
            return value
        return super()._deserialize(value, attr, data, **kwargs)


class BaseSchema(Schema):
    _model: Callable

    @post_load
    def convert_to_dataclass(self, data, many, **kwargs):
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


@dataclass
class Task:
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[str] = None
    completed: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TaskSchema(BaseSchema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=NAME_LENGTH))
    description = fields.Str(
        required=True, validate=validate.Length(min=1, max=DEFAULT_LENGTH)
    )
    user_id = fields.UUID(required=True)
    completed = fields.Boolean(required=True)
    created_at = CustomDateTimeField()
    updated_at = CustomDateTimeField()

    _model = Task


@dataclass
class Token:
    token: str
    expiry: int


class TokenSchema(BaseSchema):
    token = fields.Str()
    expiry = fields.Int()

    _model = Token


@dataclass
class User:
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password_hash: Optional[str] = None


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

    _model = User


task_schema = TaskSchema()
task_create_schema = TaskSchema(exclude=("completed", "created_at", "updated_at", "id"))
task_update_schema = TaskSchema(exclude=("created_at", "updated_at"))
task_output_schema = TaskSchema(exclude=("user_id",))

token_schema = TokenSchema()

user_schema = UserSchema(exclude=("password",))
user_register_schema = UserSchema(
    exclude=("password_hash", "id"), load_only=("password",)
)
user_login_schema = UserSchema(exclude=("id", "name", "password_hash"))
user_output_schema = UserSchema(exclude=("password_hash", "password"))
