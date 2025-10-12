import allure
import pytest
from helpers.api_client import StellarBurgersApi
from data.test_data import TestData


class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, registered_user, valid_ingredients):
        """Тест создания заказа с авторизацией и ингредиентами"""
        api = StellarBurgersApi()  # Создаем объект в тесте
        
        # Логинимся чтобы установить токен
        api.login_user(registered_user["email"], registered_user["password"])
        
        order_response = api.create_order(valid_ingredients)
        assert order_response.status_code == 200
        order_data = order_response.json()
        assert order_data['success'] == True
        assert 'name' in order_data
        assert 'order' in order_data
        assert 'number' in order_data['order']

    @allure.title("Создание заказа без авторизации с ингредиентами")
    def test_create_order_without_auth_with_ingredients(self, valid_ingredients):
        """Тест создания заказа без авторизации с ингредиентами"""
        api = StellarBurgersApi()  # Создаем объект в тесте
        
        order_response = api.create_order(valid_ingredients)
        assert order_response.status_code == 200
        order_data = order_response.json()
        assert order_data['success'] == True
        assert 'name' in order_data
        assert 'order' in order_data

    @allure.title("Создание заказа с авторизацией без ингредиентов")
    def test_create_order_with_auth_without_ingredients(self, registered_user):
        """Тест создания заказа с авторизацией без ингредиентов"""
        api = StellarBurgersApi()  # Создаем объект в тесте
        api.login_user(registered_user["email"], registered_user["password"])
        
        order_response = api.create_order(TestData.get_empty_ingredients())
        assert order_response.status_code == 400
        order_data = order_response.json()
        assert order_data['success'] == False
        assert TestData.ORDER_NO_INGREDIENTS_MESSAGE in order_data['message']

    @allure.title("Создание заказа без авторизации без ингредиентов")
    def test_create_order_without_auth_without_ingredients(self):
        """Тест создания заказа без авторизации без ингредиентов"""
        api = StellarBurgersApi()  # Создаем объект в тесте
        
        order_response = api.create_order(TestData.get_empty_ingredients())
        assert order_response.status_code == 400
        order_data = order_response.json()
        assert order_data['success'] == False
        assert TestData.ORDER_NO_INGREDIENTS_MESSAGE in order_data['message']

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, registered_user):
        """Тест создания заказа с невалидными хешами ингредиентов"""
        api = StellarBurgersApi()  # Создаем объект в тесте
        api.login_user(registered_user["email"], registered_user["password"])
        
        order_response = api.create_order(TestData.get_invalid_ingredients())
        
        # Сервер возвращает 500 с HTML страницей, поэтому не пытаемся парсить JSON
        assert order_response.status_code == 500
        # Проверяем что в ответе есть текст ошибки
        assert 'Internal Server Error' in order_response.text

    @allure.title("Создание заказа с одним невалидным ингредиентом")
    def test_create_order_with_mixed_ingredients(self, registered_user, valid_ingredients):
        """Тест создания заказа с mix валидных и невалидных ингредиентов"""
        api = StellarBurgersApi()  # Создаем объект в тесте
        api.login_user(registered_user["email"], registered_user["password"])
        
        # Берем первый валидный ингредиент и добавляем невалидный
        mixed_ingredients = [valid_ingredients[0], 'invalid_hash']
        order_response = api.create_order(mixed_ingredients)
        
        # На практике сервер принимает такой заказ и возвращает 200
        # Это нормальное поведение - сервер фильтрует невалидные ингредиенты
        assert order_response.status_code == 200
        order_data = order_response.json()
        assert order_data['success'] == True
        assert 'name' in order_data
        assert 'order' in order_data