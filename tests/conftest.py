import pytest
from helpers.api_client import ApiClient
import allure

@pytest.fixture
def api_client():
    return ApiClient()

@pytest.fixture
def registered_user(api_client):
    # Фикстура для зарегистрированного пользователя
    user_data = {
        "email": "test_user@example.com",
        "password": "password123",
        "name": "Test User"
    }
    
    # Регистрируем пользователя
    response = api_client.create_user(user_data)
    if response.status_code == 200:
        return response.json()
    else:
        # Если пользователь уже существует, логинимся
        login_response = api_client.login_user({
            "email": user_data["email"],
            "password": user_data["password"]
        })
        return login_response.json()