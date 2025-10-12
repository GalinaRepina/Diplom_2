import allure
import pytest
from helpers.api_client import StellarBurgersApi
from data.test_data import TestData


class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self):
        """Тест успешного создания уникального пользователя"""
        api = StellarBurgersApi()  # Создаем объект в тесте
        user_data = TestData.get_valid_user_data()

        response = api.create_user(
            email=user_data["email"],
            password=user_data["password"],
            name=user_data["name"]
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "accessToken" in response_data
        assert response_data["user"]["email"] == user_data["email"]
        assert response_data["user"]["name"] == user_data["name"]

        # Очистка после теста
        api.delete_user()

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user_fail(self, registered_user):
        """Тест попытки создания уже существующего пользователя"""
        api = StellarBurgersApi()  # Создаем объект в тесте
        
        # Пытаемся создать такого же пользователя еще раз (пользователь уже создан в фикстуре)
        response = api.create_user(
            email=registered_user["email"],
            password=registered_user["password"],
            name=registered_user["name"]
        )

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False
        assert response_data["message"] == TestData.USER_EXISTS_MESSAGE

    @pytest.mark.parametrize("test_data_method,empty_field,expected_message", [
        ("get_user_without_email", "email", TestData.REQUIRED_FIELDS_MESSAGE),
        ("get_user_without_password", "password", TestData.REQUIRED_FIELDS_MESSAGE),
        ("get_user_without_name", "name", TestData.REQUIRED_FIELDS_MESSAGE),
    ])
    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_without_required_field_fail(self, test_data_method, empty_field, expected_message):
        """Параметризованный тест создания пользователя без обязательных полей"""
        api = StellarBurgersApi()  # Создаем объект в тесте
        
        # Получаем данные пользователя
        user_data = getattr(TestData, test_data_method)()
        
        # Создаем payload с пустым полем
        payload = {
            "email": user_data.get("email", ""),
            "password": user_data.get("password", ""),
            "name": user_data.get("name", "")
        }

        response = api.create_user(**payload)

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False
        assert expected_message in response_data["message"]