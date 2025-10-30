import httpx  # Импортируем библиотеку HTTPX

# Данные для входа в систему
login_payload = {
    "email": "pashq@example.com",
    "password": "pashq"
}

# Выполняем запрос на аутентификацию
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
token_response_data = login_response.json()

print(f'Код ответа {login_response.status_code}')
print(f'Ответ содержит {token_response_data}')


# Формируем header для вставки токена
access_token = {
    "Authorization": f'bearer {token_response_data["token"]["accessToken"]}'
}


me_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=access_token)
me_response_data = me_response.json()

# Выводим мои данные код ответа

print("Код ответа", me_response.status_code)
print("JSON-ответ от сервера с данными о пользователе ", me_response_data)
