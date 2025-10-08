import pytest
from helpers.api_client import StellarBurgersApi
from data.test_data import TestData
import allure


@pytest.fixture
def api():
    return StellarBurgersApi()


@pytest.fixture
def registered_user(api):
    """Фикстура для зарегистрированного пользователя"""
    user_data = TestData.get_valid_user_data()
    
    # Регистрируем пользователя
    response = api.create_user(
        email=user_data["email"],
        password=user_data["password"],
        name=user_data["name"]
    )
    
    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "accessToken": response.json().get("accessToken") if response.status_code == 200 else None
    }
    
    # Очистка после теста
    api.delete_user()


@pytest.fixture
def valid_ingredients(api):
    """Фикстура для получения валидных ингредиентов"""
    response = api.get_ingredients()
    assert response.status_code == 200
    ingredients_data = response.json()
    return [ingredient['_id'] for ingredient in ingredients_data['data'][:2]]