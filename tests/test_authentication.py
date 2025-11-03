from http import HTTPStatus

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.users.public_users_client import get_public_users_client
from pydantic_create_user import CreateUserRequestSchema
from tools.assertions.assert_login_response import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema


def test_login():
    public_users_client = get_public_users_client()

    create_user_request = CreateUserRequestSchema()
    print("Запрос на создание юзера", create_user_request)

    create_user_response = public_users_client.create_user(create_user_request)
    print('Create user data:', create_user_response)

    auth_client = get_authentication_client()

    user_creds = LoginRequestSchema(
        email=create_user_request.email,
        password=create_user_request.password
    )
    print("Запрос на создание токенов:", user_creds)

    login_api_response = auth_client.login_api(user_creds)
    login_response_data = LoginResponseSchema.model_validate_json(login_api_response.text)

    assert_status_code(login_api_response.status_code, HTTPStatus.OK)

    assert_login_response(login_response_data)

    validate_json_schema(login_api_response.json(), login_response_data.model_json_schema())
