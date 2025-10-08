import allure
import pytest
from data.test_data import TestData


class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, api):
        """Тест успешного создания уникального пользователя"""
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

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user_fail(self, api):
        """Тест попытки создания уже существующего пользователя"""
        # Сначала создаем пользователя
        user_data = TestData.get_valid_user_data()
        api.create_user(
            email=user_data["email"],
            password=user_data["password"],
            name=user_data["name"]
        )

        # Пытаемся создать такого же пользователя еще раз
        response = api.create_user(
            email=user_data["email"],
            password=user_data["password"],
            name=user_data["name"]
        )

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False
        assert response_data["message"] == "User already exists"

    @allure.title("Создание пользователя без email")
    def test_create_user_without_email_fail(self, api):
        """Тест создания пользователя без обязательного поля email"""
        user_data = TestData.get_user_without_email()

        response = api.create_user(
            email="",  # Пустой email
            password=user_data["password"],
            name=user_data["name"]
        )

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False
        assert "required fields" in response_data["message"]

    @allure.title("Создание пользователя без пароля")
    def test_create_user_without_password_fail(self, api):
        """Тест создания пользователя без обязательного поля password"""
        user_data = TestData.get_user_without_password()

        response = api.create_user(
            email=user_data["email"],
            password="",  # Пустой пароль
            name=user_data["name"]
        )

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False
        assert "required fields" in response_data["message"]

    @allure.title("Создание пользователя без имени")
    def test_create_user_without_name_fail(self, api):
        """Тест создания пользователя без обязательного поля name"""
        user_data = TestData.get_user_without_name()

        response = api.create_user(
            email=user_data["email"],
            password=user_data["password"],
            name=""  # Пустое имя
        )

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False
        assert "required fields" in response_data["message"]