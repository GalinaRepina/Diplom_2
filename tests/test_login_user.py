import allure
import pytest
from data.test_data import TestData


class TestLoginUser:
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(self, api, registered_user):
        """Тест успешного входа под существующим пользователем"""
        response = api.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]
        assert response_data["user"]["name"] == registered_user["name"]

    @allure.title("Вход с неверным email")
    def test_login_with_wrong_email_fail(self, api, registered_user):
        """Тест входа с неверным email"""
        response = api.login_user(
            email="wrong_email@example.com",
            password=registered_user["password"]
        )

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] == False
        assert "email or password are incorrect" in response_data["message"]

    @allure.title("Вход с неверным паролем")
    def test_login_with_wrong_password_fail(self, api, registered_user):
        """Тест входа с неверным паролем"""
        response = api.login_user(
            email=registered_user["email"],
            password="wrong_password"
        )

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] == False
        assert "email or password are incorrect" in response_data["message"]

    @allure.title("Вход без email")
    def test_login_without_email_fail(self, api, registered_user):
        """Тест входа без email"""
        response = api.login_user(
            email="",
            password=registered_user["password"]
        )

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] == False
        assert "email or password are incorrect" in response_data["message"]

    @allure.title("Вход без пароля")
    def test_login_without_password_fail(self, api, registered_user):
        """Тест входа без пароля"""
        response = api.login_user(
            email=registered_user["email"],
            password=""
        )

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] == False
        assert "email or password are incorrect" in response_data["message"]