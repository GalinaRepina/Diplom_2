import random
import string


class TestData:
    # Базовые тестовые данные
    EMAIL = "test_user@example.com"
    PASSWORD = "password123"
    NAME = "Test User"
    
    # Невалидные данные
    INVALID_EMAIL = "invalid_email"
    INVALID_PASSWORD = "123"
    SHORT_PASSWORD = "12345"
    
    # Данные для тестов заказов
    ORDER_SUCCESS_MESSAGE = "Order created successfully"
    ORDER_NO_INGREDIENTS_MESSAGE = "Ingredient ids must be provided"
    ORDER_INVALID_INGREDIENTS_MESSAGE = "Internal Server Error"
    LOGIN_INVALID_CREDENTIALS_MESSAGE = "email or password are incorrect"
    USER_EXISTS_MESSAGE = "User already exists"
    REQUIRED_FIELDS_MESSAGE = "required fields"
    
    @staticmethod
    def generate_email():
        """Генерация уникального email"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"test_{random_string}@example.com"
    
    @staticmethod
    def generate_name():
        """Генерация уникального имени"""
        random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"User_{random_string}"
    
    @staticmethod
    def get_valid_user_data():
        """Получить валидные данные пользователя"""
        return {
            "email": TestData.generate_email(),
            "password": TestData.PASSWORD,
            "name": TestData.generate_name()
        }
    
    @staticmethod
    def get_existing_user_data():
        """Получить данные существующего пользователя"""
        return {
            "email": TestData.EMAIL,
            "password": TestData.PASSWORD,
            "name": TestData.NAME
        }
    
    @staticmethod
    def get_user_without_email():
        """Получить данные пользователя без email"""
        return {
            "password": TestData.PASSWORD,
            "name": TestData.NAME
        }
    
    @staticmethod
    def get_user_without_password():
        """Получить данные пользователя без пароля"""
        return {
            "email": TestData.generate_email(),
            "name": TestData.NAME
        }
    
    @staticmethod
    def get_user_without_name():
        """Получить данные пользователя без имени"""
        return {
            "email": TestData.generate_email(),
            "password": TestData.PASSWORD
        }
    
    @staticmethod
    def get_invalid_ingredients():
        """Получить невалидные ингредиенты"""
        return ['invalid_hash_1', 'invalid_hash_2']
    
    @staticmethod
    def get_empty_ingredients():
        """Получить пустой список ингредиентов"""
        return []