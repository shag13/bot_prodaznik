from aiogram.fsm.state import State, StatesGroup

class AddExample(StatesGroup):
    name = State()        # Имя бота
    description = State() # Описание
    link = State()        # Ссылка

class Form(StatesGroup):
    # Основной опрос
    business_niche = State()        # Выбор ниши бизнеса

    start = State()              # Начальное состояние
    learn_more = State()         # Состояние "Узнать больше"
    business_subniche = State()     # Выбор подкатегории
    goals = State()                 # Цели клиента
    current_situation = State()     # Текущая ситуация
    budget = State()                # Бюджет
    timeline = State()              # Сроки
    readiness = State()             # Готовность к действию
    delete_example = State()
    bot_constructor = State()
    user_phone_input = State()
    # Подтверждение боли и предложение примеров
    examples_offer = State()  # Предложение посмотреть примеры

    # Примеры ботов
    examples_show = State()   # Показ примеров
    example_next = State()    # Переход к следующему примеру

    # Демо-режимы
    demo_type_selection = State()   # Выбор типа демо-режима
    demo_beauty_service = State()   # Выбор услуги в салоне красоты
    demo_beauty_time = State()      # Выбор времени в салоне красоты
    demo_beauty_reminder = State()  # Подтверждение напоминания
    demo_shop_product = State()     # Выбор товара в магазине
    demo_shop_address = State()     # Указание адреса доставки
    demo_shop_payment = State()     # Оплата в магазине
    demo_support_question = State() # Выбор вопроса в поддержке
    demo_support_followup = State() # Дополнительные действия в поддержке
    after_demo = State()
    
    # Сбор контактов
    contact_method = State()       # Выбор способа связи
    contact_email_input = State()  # Ввод email
    contact_phone_input = State()  # Ввод телефона
    contact_verification = State()  # Подтверждение контакта

    # Конструктор бота
    constructor_features = State()  # Выбор функций
    consultation_time = State()     # Выбор времени консультации
    constructor_confirm = State()   # Подтверждение выбора функций

    # Расчет стоимости
    price_calculation = State()     # Расчет итоговой стоимости

    # Запись на консультацию
    consultation_time = State()    # Выбор времени консультации
    consultation_confirm = State()  # Подтверждение записи

    # Уведомление администратора
    admin_notification = State()   # Уведомление о новой заявке

    # Обработка текстовых ответов
    other_answer = State()         # Обработка ответа "Другое"

    # Общие состояния
    cancel_action = State()        # Отмена действия
    back_action = State()          # Возврат к предыдущему шагу

    considering_options = State()   # Состояние для обработки "Рассматриваю варианты"
    user_vision_input = State()     # Состояние для ввода видения пользователя

    user_name_input = State()       # Ввод имени пользователя
    user_phone_input = State()      # Ввод телефона пользователя
    user_email_input = State()      # Ввод email пользователя
