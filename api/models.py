from dataclasses import dataclass
from marshmallow import Schema, fields, post_dump, validate
import uuid
from api.config import NAME_LENGTH, DEFAULT_LENGTH


class Model:
    _schema: Schema
    _schema_public: Schema
    _validator: Schema

    def serialise(self):
        return self._schema.dump(self)

    def serialise_public(self):
        return self._schema_public.dump(self)

    @classmethod
    def validate(cls, **data):
        return cls._validator.validate(data)

    @classmethod
    def deserialise(cls, **data):
        serialised_data = cls._schema.load(data)
        return cls(**serialised_data)


class BaseSchema(Schema):
    @post_dump
    def remove_null_values(self, data, **kwargs):
        return {key: value for key, value in data.items() if value is not None}


class TaskSchema(BaseSchema):
    id = fields.UUID(load_default=uuid.uuid4)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=NAME_LENGTH))
    description = fields.Str(
        required=True, validate=validate.Length(min=1, max=DEFAULT_LENGTH)
    )
    user_id = fields.UUID(required=True)


@dataclass
class Task(Model):
    id: str
    name: str
    description: str
    user_id: str

    _schema = TaskSchema()
    _schema_public = TaskSchema(exclude=("user_id",))
    _validator = TaskSchema(exclude=("id", "user_id"))


class TokenSchema(Schema):
    token = fields.Str()
    expiry = fields.Int()


@dataclass
class Token(Model):
    token: str
    expiry: int

    _schema = TokenSchema()


class UserSchema(BaseSchema):
    id = fields.UUID(load_default=uuid.uuid4)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=NAME_LENGTH))
    email = fields.Email(
        required=True, validate=validate.Length(min=1, max=NAME_LENGTH)
    )
    password = fields.Str(
        load_default=None, validate=validate.Length(min=1, max=NAME_LENGTH)
    )
    password_hash = fields.Str(load_default=None)


@dataclass
class User(Model):
    id: str
    name: str
    email: str
    password: str
    password_hash: str

    _schema = UserSchema()
    _schema_public = UserSchema(exclude=("password", "password_hash"))


# NOTE: Need 4 schemas here:
# user input schema, database schema, user output schema and validation schema
# most of the time user output schema equals user input
# Additional validation schema needed to stop certain fields from being passed in
# (e.g. "id")
