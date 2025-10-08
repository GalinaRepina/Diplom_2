# Diplom 2 - API Tests for Stellar Burgers

## Описание проекта
Автотесты для API сервиса Stellar Burgers

## Структура проекта
- `tests/` - тестовые сценарии
- `helpers/` - вспомогательные классы
- `data/` - тестовые данные
- `config.py` - конфигурация

## Запуск тестов
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest

# Запуск с Allure отчетом
pytest --alluredir=allure-results
allure serve allure-results