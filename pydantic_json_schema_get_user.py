from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.users.users_schema import CreateUserRequestSchema, GetUserResponseSchema
from tools.assertions.schema import validate_json_schema

public_users_client = get_public_users_client()
new_create_user_data = CreateUserRequestSchema()
print("Данные которые отправляем на создание юзера(генерируются через pydantic):", new_create_user_data, "\n")

create_user_data_response = public_users_client.create_user(new_create_user_data)
print("Ответ на запрос создания пользователя", create_user_data_response, "\n")

user_cred = AuthenticationUserSchema(
    email=new_create_user_data.email,
    password=new_create_user_data.password
)
private_users_client = get_private_users_client(user_cred)

user_data = private_users_client.get_user(create_user_data_response.user.id)
print("Данные созданного юзера", user_data, "\n")

get_user_response_json_schema = GetUserResponseSchema.model_json_schema()  # Схема модели pydantic

# Валидация схемы
validate_json_schema(instance=user_data.model_dump(by_alias=True), schema=get_user_response_json_schema)
