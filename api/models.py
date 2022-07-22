from dataclasses import dataclass
from typing import Optional
from marshmallow import Schema, fields, validate, exceptions
from api.config import NAME_LENGTH, DEFAULT_LENGTH
from api.exceptions import ValidationError


class Model:
    @classmethod
    def load(cls, schema: Schema, **data):
        try:
            dict_data = schema.load(data)
        except exceptions.ValidationError:
            raise ValidationError

        return cls(**dict_data)

    def dump(self, schema: Schema):
        return schema.dump(self)


class TaskSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=NAME_LENGTH))
    description = fields.Str(
        required=True, validate=validate.Length(min=1, max=DEFAULT_LENGTH)
    )
    user_id = fields.UUID(required=True)


@dataclass
class Task(Model):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[str] = None


class TokenSchema(Schema):
    token = fields.Str()
    expiry = fields.Int()


@dataclass
class Token(Model):
    token: str
    expiry: int


class UserSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=NAME_LENGTH))
    email = fields.Email(
        required=True, validate=validate.Length(min=1, max=NAME_LENGTH)
    )
    password = fields.Str(
        required=True, validate=validate.Length(min=1, max=NAME_LENGTH)
    )
    password_hash = fields.Str(required=True)


@dataclass
class User(Model):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password_hash: Optional[str] = None


task_schema = TaskSchema()
task_create_schema = TaskSchema(dump_only=("id",), load_only=("user_id",))
task_update_schema = TaskSchema(load_only=("user_id",))
task_output_schema = TaskSchema(exclude=("user_id",))

token_schema = TokenSchema()

user_schema = UserSchema(exclude=("password",))
user_register_schema = UserSchema(
    exclude=("password_hash", "id"), load_only=("password",)
)
user_login_schema = UserSchema(exclude=("id", "name", "password_hash"))
user_output_schema = UserSchema(exclude=("password_hash", "password"))
