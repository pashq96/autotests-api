from http import HTTPStatus

import pytest

from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import GetUserResponseSchema
from fixtures.users import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_get_user_response


@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(function_user: UserFixture, private_users_client: PrivateUsersClient):
    # вызов апи метода GET /api/v1/users/me
    api_response = private_users_client.get_user_me_api()
    # Преобразовали тело ответа в пайдантик модель
    data_response = GetUserResponseSchema.model_validate_json(api_response.text)

    assert_status_code(api_response.status_code, HTTPStatus.OK)

    assert_get_user_response(data_response, function_user.response)  # Сравнили с ответом запроса на создание юзера

    validate_json_schema(api_response.json(), data_response.model_json_schema())
