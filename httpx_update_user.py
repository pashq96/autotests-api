import httpx
from tools.fakers import get_random_email

# Создание пользователя
body = {
    "email": get_random_email(),
    "password": "pashq",
    "lastName": "pashq",
    "firstName": "pashq",
    "middleName": "pashq"
}

response = httpx.post("http://localhost:8000/api/v1/users", json=body)
data_user = response.json()

# Получение токена
body = {
    "email": data_user["user"]["email"],
    "password": "pashq"
}

response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=body)
tokens = response.json()

# Изменение данных пользователя
body = {
    "email": get_random_email(),
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

headers = {
    "Authorization": f'bearer {tokens["token"]["accessToken"]}'
}

response = httpx.patch(f"http://localhost:8000/api/v1/users/{data_user['user']['id']}", headers=headers, json=body)

print(response.json())  # Ответ после изменения данных пользователя
