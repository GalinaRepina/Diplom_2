import requests
import allure
import sys
import os

# Добавляем корневую папку в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config


class ApiClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or Config.BASE_URL
        self.session = requests.Session()
    
    @allure.step("POST запрос к {endpoint}")
    def post(self, endpoint, json=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=json, headers=headers)
    
    @allure.step("GET запрос к {endpoint}") 
    def get(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, headers=headers)
    
    @allure.step("DELETE запрос к {endpoint}")
    def delete(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        return self.session.delete(url, headers=headers)


class StellarBurgersApi:
    def __init__(self):
        self.client = ApiClient()
        self.token = None
    
    def set_token(self, token):
        """Установка токена авторизации"""
        self.token = token
    
    def get_headers(self):
        """Получение заголовков с авторизацией"""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = self.token
        return headers
    
    def create_user(self, email, password, name):
        """Создание пользователя"""
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        return self.client.post("/auth/register", json=payload)
    
    def login_user(self, email, password):
        """Авторизация пользователя"""
        payload = {
            "email": email,
            "password": password
        }
        response = self.client.post("/auth/login", json=payload)
        if response.status_code == 200:
            self.set_token(response.json().get("accessToken"))
        return response
    
    def get_ingredients(self):
        """Получение списка ингредиентов"""
        return self.client.get("/ingredients")
    
    def create_order(self, ingredients, token=None):
        """Создание заказа"""
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = token
        elif self.token:
            headers['Authorization'] = self.token
            
        payload = {'ingredients': ingredients}
        return self.client.post("/orders", json=payload, headers=headers)
    
    def delete_user(self, token=None):
        """Удаление пользователя (требуется авторизация)"""
        headers = self.get_headers()
        if token:
            headers['Authorization'] = token
        return self.client.delete("/auth/user", headers=headers)