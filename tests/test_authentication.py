from http import HTTPStatus

import pytest

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from tests.conftest import UserFixture
from tools.assertions.assert_login_response import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema


@pytest.mark.authentication
@pytest.mark.regression
def test_login(function_user: UserFixture, authentication_client: AuthenticationClient):
    user_creds = LoginRequestSchema(
        email=function_user.email,
        password=function_user.password
    )

    login_api_response = authentication_client.login_api(user_creds)
    login_response_data = LoginResponseSchema.model_validate_json(login_api_response.text)

    assert_status_code(login_api_response.status_code, HTTPStatus.OK)

    assert_login_response(login_response_data)

    validate_json_schema(login_api_response.json(), login_response_data.model_json_schema())
