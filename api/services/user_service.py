import uuid
import boto3

# import botocore
import re
import jwt
from jwt import PyJWKClient
from aws_error_utils import errors, ClientError

# from werkzeug.security import generate_password_hash, check_password_hash
from api.services import token_service
from api.exceptions import InvalidUsageError
from api.models import User  # , db
from api.config import API_COGNITO_USER_POOL, API_COGNITO_CLIENT_ID


cognito_client = boto3.client("cognito-idp")

jwks_client = PyJWKClient(
    "https://cognito-idp.ap-southeast-2.amazonaws.com/"
    + f"{API_COGNITO_USER_POOL}/.well-known/jwks.json"
)


def register_user(user: User):
    user.id = uuid.uuid4()
    if is_valid_password(user.password) is False:
        raise InvalidUsageError("Invalid password")

    try:
        cognito_client.admin_create_user(
            UserPoolId=API_COGNITO_USER_POOL,
            Username=user.email,
            UserAttributes=[{"Name": "name", "Value": user.name}],
        )
    except errors.UsernameExistsException:
        raise InvalidUsageError("User already registered")

    cognito_client.admin_set_user_password(
        UserPoolId=API_COGNITO_USER_POOL,
        Username=user.email,
        Permanent=True,
        Password=user.password,
    )


def login_user(user: User):
    try:
        user_info = cognito_client.admin_get_user(
            UserPoolId=API_COGNITO_USER_POOL, Username=user.email
        )
        auth_info = cognito_client.admin_initiate_auth(
            UserPoolId=API_COGNITO_USER_POOL,
            AuthFlow="ADMIN_NO_SRP_AUTH",
            ClientId=API_COGNITO_CLIENT_ID,
            AuthParameters={"USERNAME": user.email, "PASSWORD": user.password},
        )
    except ClientError:
        raise InvalidUsageError("Incorrect username or password")

    auth_result = auth_info["AuthenticationResult"]
    print(auth_result)

    # NEED TO RETURN ID TOKEN AS WELL
    return (
        get_user_attributes(user_info),
        auth_result["AccessToken"],
        auth_result["RefreshToken"],
    )


def logout_user(token: str):
    if token:
        try:
            cognito_client.revoke_token(Token=token, ClientId=API_COGNITO_CLIENT_ID)
        except ClientError as error:
            print(error)
            pass


def refresh_credentials(refresh_token: str):
    payload = token_service.verify_refresh_token(refresh_token)
    access_token = token_service.generate_access_token(payload["user_id"])
    return access_token


def is_valid_password(password: str):
    password_regex = "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#\$%\^&\*\(\)\-_=\+;:,<\.>])[\S]{8,128}$"  # noqa
    return re.match(password_regex, password) is not None


def get_user_attributes(user_info: dict):
    user = user_info["UserAttributes"]
    user = {x["Name"]: x["Value"] for x in user}
    user["id"] = user["sub"]
    del user["sub"]
    return user


def verify_access_token(token: str):
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        return jwt.decode(token, signing_key.key, algorithms=["RS256"])
    except jwt.exceptions.InvalidTokenError:
        raise InvalidTokenError
