import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение пути к корневой директории проекта
BASE_DIR = Path(__file__).parent.parent

class Config:
    # Основные настройки бота
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")  # Токен бота
    ADMIN_ID = os.getenv("ADMIN_ID", "")    # ID администратора
    DEFAULT_RATE_LIMIT = 0.5  # Лимит запросов в секунду

    # Пути к файлам
    USERS_DATA_PATH = BASE_DIR / "data/users.json"  # Путь к файлу с данными пользователей
    CASES_DATA_PATH = BASE_DIR / "data/cases.json"  # Путь к файлу с кейсами
    

    # Настройки базы данных (можно расширить при необходимости)
    DB_CONFIG = {
        'drivername': 'sqlite',
        'database': BASE_DIR / 'data/database.db'  # Путь к SQLite базе данных
    }

    # Настройки демо-режимов
    DEMO_SETTINGS = {
        'beauty': {
            'services': ['Стрижка', 'Маникюр', 'Массаж'],  # Услуги для демо-режима "салон красоты"
            'time_slots': ['20 ноября, 15:00', '21 ноября, 10:00']  # Доступные временные слоты
        },
        'shop': {
            'products': ['Кроссовки', 'Куртка', 'Рюкзак'],  # Товары для демо-режима "магазин"
            'delivery_types': ['Самовывоз', 'Доставка']  # Типы доставки
        },
        'support': {
            'faq': ['Как оформить возврат?', 'Где мой заказ?', 'Как связаться с поддержкой?']  # Вопросы для демо-режима "поддержка"
        }
    }

    # Стоимость функций бота
    PRICING = {
        'feature_order': 5000,      # Стоимость функции "Онлайн-заказ"
        'feature_support': 3000,   # Стоимость функции "Чат с поддержкой"
        'feature_payment': 4000,   # Стоимость функции "Оплата"
        'feature_analytics': 2500, # Стоимость функции "Аналитика"
        'base_price': 10000        # Базовая стоимость бота
    }

    # Настройки уведомлений
    NOTIFICATION_SETTINGS = {
        'admin_chat_id': ADMIN_ID,  # ID чата администратора
        'new_user_template': (      # Шаблон уведомления о новой заявке
            "Новая заявка!\n"
            "Имя: {name}\n"
            "Ниша: {niche}\n"
            "Выбранные функции: {features}\n"
            "Контакты: {contacts}"
        ),
        'reminder_before_consultation': 3600  # За сколько секунд отправлять напоминание о консультации
    }

    # Настройки верификации
    VERIFICATION = {
        'email_code_length': 6,    # Длина кода для email
        'sms_code_length': 4,      # Длина кода для SMS
        'code_expiration': 300     # Время жизни кода в секундах
    }

    # Настройки примеров ботов
    EXAMPLES = {
        'example_bot_1': {
            'name': "Бот для кофейни",
            'description': "Увеличил продажи на 30%!",
            'url': "https://t.me/example_bot_1"
        },
        'example_bot_2': {
            'name': "Бот для интернет-магазина",
            'description': "Автоматизировал 80% заказов!",
            'url': "https://t.me/example_bot_2"
        }
    }

    # Настройки консультаций
    CONSULTATION_SETTINGS = {
        'available_slots': [        # Доступные слоты для консультации
            "20 ноября, 15:00",
            "21 ноября, 10:00"
        ],
        'reminder_message': (       # Шаблон напоминания о консультации
            "Напоминаем о вашей консультации сегодня в {time}.\n"
            "Ссылка на Zoom: {link}"
        )
    }

    @classmethod
    def check_required_vars(cls):
        """Проверка обязательных переменных окружения"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не задан в .env файле")
        if not cls.ADMIN_ID:
            raise ValueError("ADMIN_ID не задан в .env файле")

# Проверка при импорте конфига
Config.check_required_vars()
