from dataclasses import dataclass
from typing import Optional
from marshmallow import Schema, fields, validate
import uuid
from api.config import NAME_LENGTH, DEFAULT_LENGTH


class Model:
    _schema_validator: Schema  # Validate data provided by user
    _schema_client: Schema  # Serialise/deserialise to and from users
    _schema_database: Schema  # Serialise/deserialise data to and from DB

    @classmethod
    def deserialise_public(cls, **data):
        dict_data = cls._schema_client.load(data)
        return cls(**dict_data)

    def serialise_public(self):
        return self._schema_client.dump(self)

    @classmethod
    def deserialise(cls, **data):
        dict_data = cls._schema_database.load(data)
        return cls(**dict_data)

    def serialise(self):
        return self._schema_database.dump(self)

    @classmethod
    def validate(cls, data):
        return cls._schema_validator.validate(data)


class TaskSchema(Schema):
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

    _schema_client = TaskSchema(exclude=("user_id",))
    _schema_database = TaskSchema()
    _schema_validator = TaskSchema(exclude=("id", "user_id"))


class TokenSchema(Schema):
    token = fields.Str()
    expiry = fields.Int()


@dataclass
class Token(Model):
    token: str
    expiry: int

    _schema_database = TokenSchema()


class UserSchema(Schema):
    id = fields.UUID(load_default=uuid.uuid4)
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
    id: str
    name: str
    email: str
    password: Optional[str] = None
    password_hash: Optional[str] = None

    _schema_validator = UserSchema(exclude=("id", "password_hash"))
    _schema_client = UserSchema(exclude=("password_hash",), load_only=("password",))
    _schema_database = UserSchema(exclude=("password",))


@dataclass
class UserLogin(Model):
    _schema_validator = UserSchema(exclude=("id", "name", "password_hash"))
