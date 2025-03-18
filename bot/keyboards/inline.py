from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_EXAMPLES = [
    "https://t.me/Flowershop_labot",  # Первый бот
    "https://t.me/LaSell_LaBot",     # Второй бот
    # Добавьте другие ссылки по мере необходимости
]

# Главное меню (Выбор ниши бизнеса)
def main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="1. Торговля", callback_data="niche_trade")
    builder.button(text="2. Услуги", callback_data="niche_services")
    builder.button(text="3. Образование", callback_data="niche_education")
    builder.button(text="4. Производство", callback_data="niche_production")
    builder.button(text="5. Общественное питание", callback_data="niche_food")
    builder.button(text="6. Творчество и искусство", callback_data="niche_art")
    builder.button(text="7. Здоровье и красота", callback_data="niche_health")
    builder.button(text="8. IT и технологии", callback_data="niche_it")
    builder.button(text="9. Маркетинг и реклама", callback_data="niche_marketing")
    builder.button(text="10. Другое", callback_data="niche_other")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Подменю для торговли
def trade_submenu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Онлайн-магазин", callback_data="trade_online_shop")
    builder.button(text="Оффлайн-магазин", callback_data="trade_offline_shop")
    builder.button(text="Маркетплейс", callback_data="trade_marketplace")
    builder.button(text="Дропшиппинг", callback_data="trade_dropshipping")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Подменю для услуг
def services_submenu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Салоны красоты", callback_data="services_beauty")
    builder.button(text="Фитнес-клубы", callback_data="services_fitness")
    builder.button(text="Ремонтные услуги", callback_data="services_repair")
    builder.button(text="Клининговые услуги", callback_data="services_cleaning")
    builder.button(text="Риелторские услуги", callback_data="services_realty")
    builder.button(text="Юридические услуги", callback_data="services_legal")
    builder.button(text="Медицинские услуги", callback_data="services_medical")
    builder.button(text="Туристические агентства", callback_data="services_tourism")
    builder.button(text="Образовательные курсы", callback_data="services_education")
    builder.button(text="IT-услуги", callback_data="services_it")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Подменю для образования
def education_submenu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Онлайн-школы", callback_data="education_online_schools")
    builder.button(text="Репетиторство", callback_data="education_tutoring")
    builder.button(text="Языковые курсы", callback_data="education_language")
    builder.button(text="Курсы по программированию", callback_data="education_programming")
    builder.button(text="Курсы по маркетингу", callback_data="education_marketing")
    builder.button(text="Курсы по дизайну", callback_data="education_design")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Подменю для производства
def production_submenu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Производство товаров", callback_data="production_goods")
    builder.button(text="Пищевое производство", callback_data="production_food")
    builder.button(text="Производство одежды", callback_data="production_clothing")
    builder.button(text="Производство мебели", callback_data="production_furniture")
    builder.button(text="Ремесленные мастерские", callback_data="production_craft")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Подменю для общественного питания
def food_submenu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Кафе и рестораны", callback_data="food_cafe")
    builder.button(text="Кофейни", callback_data="food_coffee")
    builder.button(text="Фудтраки", callback_data="food_foodtruck")
    builder.button(text="Доставка еды", callback_data="food_delivery")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Подменю для творчества и искусства
def art_submenu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Фотостудии", callback_data="art_photo")
    builder.button(text="Музыкальные школы", callback_data="art_music")
    builder.button(text="Художественные мастерские", callback_data="art_art")
    builder.button(text="Рукоделие и хендмейд", callback_data="art_craft")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Подменю для здоровья и красоты
def health_submenu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Спа-салоны", callback_data="health_spa")
    builder.button(text="Массажные кабинеты", callback_data="health_massage")
    builder.button(text="Стоматологические клиники", callback_data="health_dentistry")
    builder.button(text="Фитнес-тренеры", callback_data="health_fitness")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Подменю для IT и технологий
def it_submenu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Разработка ПО", callback_data="it_software")
    builder.button(text="Веб-студии", callback_data="it_web")
    builder.button(text="Кибербезопасность", callback_data="it_cybersecurity")
    builder.button(text="Облачные сервисы", callback_data="it_cloud")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Подменю для маркетинга и рекламы
def marketing_submenu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="SMM-агентства", callback_data="marketing_smm")
    builder.button(text="Контент-студии", callback_data="marketing_content")
    builder.button(text="Рекламные агентства", callback_data="marketing_ads")
    builder.button(text="Таргетированная реклама", callback_data="marketing_targeting")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Подменю для других ниш
def other_submenu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Некоммерческие организации", callback_data="other_nonprofit")
    builder.button(text="Благотворительные фонды", callback_data="other_charity")
    builder.button(text="Стартапы", callback_data="other_startups")
    builder.button(text="Фриланс", callback_data="other_freelance")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()

# Добавьте это в файл inline.py после существующих функций

# Клавиатура для выбора целей
def goals_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Увеличение продаж", callback_data="goal_sales")
    builder.button(text="Автоматизация заказов", callback_data="goal_orders")
    builder.button(text="Поддержка клиентов", callback_data="goal_support")
    builder.button(text="Продвижение услуг", callback_data="goal_promotion")
    builder.button(text="Сбор заявок", callback_data="goal_leads")
    builder.adjust(1)
    return builder.as_markup()

# Клавиатура текущей ситуации
def current_situation_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Вручную", callback_data="situation_manual")
    builder.button(text="Другое ПО", callback_data="situation_other_software")
    builder.button(text="Нет решения", callback_data="situation_none")
    builder.adjust(1)
    return builder.as_markup()

# Клавиатура бюджета
def budget_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="До 10 тыс.", callback_data="budget_10k")
    builder.button(text="10-30 тыс.", callback_data="budget_30k")
    builder.button(text="30-50 тыс.", callback_data="budget_50k")
    builder.button(text="50+ тыс.", callback_data="budget_50k_plus")
    builder.adjust(2)
    return builder.as_markup()

# Клавиатура сроков
def timeline_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Сразу", callback_data="timeline_now")
    builder.button(text="1-2 недели", callback_data="timeline_2week")
    builder.button(text="1 месяц", callback_data="timeline_1month")
    builder.button(text="Пока изучаю", callback_data="timeline_research")
    builder.adjust(2)
    return builder.as_markup()

# Клавиатура готовности
def readiness_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Да, готов обсудить", callback_data="readiness_yes")
    builder.button(text="Нужны примеры", callback_data="readiness_examples")
    builder.button(text="Рассматриваю варианты", callback_data="readiness_maybe")
    builder.adjust(1)
    return builder.as_markup()

# Остальные недостающие клавиатуры
def examples_offer_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Показать примеры", callback_data="examples_show")
    builder.button(text="Попробовать демо", callback_data="demo_start")
    builder.adjust(1)
    return builder.as_markup()

# Исправленная функция (inline.py)
def examples_kb(examples_data: list, example_index: int):
    builder = InlineKeyboardBuilder()

    # Кнопки для пагинации
    if example_index > 0:
        builder.button(text="⬅️ Назад", callback_data=f"example_back_{example_index - 1}")
    if example_index < len(examples_data) - 1:
        builder.button(text="Далее ➡️", callback_data=f"example_next_{example_index + 1}")

    # Остальные кнопки
    builder.button(text="🎮 Демо-режим", callback_data="demo_start")
    builder.button(text="🔙 Назад в меню", callback_data="back_to_readiness")

    builder.adjust(1)
    return builder.as_markup()

def demo_types_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="💅 Запись на услуги", callback_data="demo_beauty")
    builder.button(text="🛍 Онлайн-заказ", callback_data="demo_shop")
    builder.button(text="💬 Поддержка клиентов", callback_data="demo_support")
    builder.button(text="🔙 Назад", callback_data="back_to_examples")
    builder.adjust(1)  # Одна кнопка в строке
    return builder.as_markup()

# Кнопки для демо-режимов
def shop_products_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Кроссовки", callback_data="product_sneakers")
    builder.button(text="Куртка", callback_data="product_jacket")
    builder.button(text="Рюкзак", callback_data="product_backpack")
    builder.button(text="🔙 Назад", callback_data="back_to_demo")
    builder.adjust(1)  # Одна кнопка в строке
    return builder.as_markup()

def delivery_options_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Доставка", callback_data="delivery_home")
    builder.button(text="Самовывоз", callback_data="delivery_pickup")
    builder.button(text="🔙 Назад", callback_data="back_to_products")
    builder.adjust(1)  # Одна кнопка в строке
    return builder.as_markup()

def payment_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить", callback_data="payment_confirm")
    builder.button(text="🔙 Назад", callback_data="back_to_delivery")
    builder.adjust(1)  # Одна кнопка в строке
    return builder.as_markup()

def support_questions_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Как оформить возврат?", callback_data="question_return")
    builder.button(text="Где мой заказ?", callback_data="question_order")
    builder.button(text="Как связаться с поддержкой?", callback_data="question_contact")
    builder.button(text="🔙 Назад", callback_data="back_to_demo")
    builder.adjust(1)  # Одна кнопка в строке
    return builder.as_markup()

def followup_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="followup_yes")
    builder.button(text="Нет", callback_data="followup_no")
    builder.button(text="🔙 Назад", callback_data="back_to_questions")
    builder.adjust(1)  # Одна кнопка в строке
    return builder.as_markup()

# Кнопки после завершения демо-режима
def after_demo_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да, готов обсудить", callback_data="ready_to_discuss")
    builder.button(text="🛠 Создать своего бота", callback_data="create_my_bot")
    builder.adjust(1)  # Одна кнопка в строке
    return builder.as_markup()

# Кнопки для "Рассматриваю варианты"
def considering_options_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Написать свое видение", callback_data="write_vision")
    builder.button(text="🔙 Назад", callback_data="back_to_readiness")
    builder.adjust(1)  # Одна кнопка в строке
    return builder.as_markup()

def beauty_services_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Маникюр", callback_data="service_manicure")
    builder.button(text="Стрижка", callback_data="service_haircut")
    builder.button(text="Массаж", callback_data="service_massage")
    builder.adjust(1)
    return builder.as_markup()

def time_slots_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="10:00", callback_data="time_10")
    builder.button(text="12:00", callback_data="time_12")
    builder.button(text="14:00", callback_data="time_14")
    builder.button(text="16:00", callback_data="time_16")
    builder.adjust(2)
    return builder.as_markup()

def reminder_confirmation_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="reminder_yes")
    builder.button(text="Нет", callback_data="reminder_no")
    builder.adjust(2)
    return builder.as_markup()

def contact_request_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Email", callback_data="contact_email")
    builder.button(text="Телефон", callback_data="contact_phone")
    builder.adjust(2)
    return builder.as_markup()

def bot_constructor_kb(selected_features=None):
    if selected_features is None:
        selected_features = set()
    
    builder = InlineKeyboardBuilder()
    
    # Список функций с их стоимостью
    features = {
        "Онлайн-заказ": 5000,
        "Чат с поддержкой": 3000,
        "Оплата через Telegram": 4000,
        "Интеграция с CRM": 6000,
        "Автоматическая рассылка": 3500,
        "Сбор отзывов": 2500,
        "Аналитика продаж": 4500,
        "Бронирование услуг": 4000,
        "Интеграция с маркетплейсами": 7000,
    }
    
    # Добавляем кнопки для каждой функции
    for feature, price in features.items():
        if feature in selected_features:
            builder.button(text=f"✅ {feature} (+{price} руб.)", callback_data=f"feature_{feature}")
        else:
            builder.button(text=f"{feature} (+{price} руб.)", callback_data=f"feature_{feature}")
    
    # Кнопка "Готово"
    builder.button(text="✅ Готово", callback_data="features_done")
    builder.button(text="🔙 Назад", callback_data="back_to_readiness")
    
    builder.adjust(1)  # Одна кнопка в строке
    return builder.as_markup()

def consultation_confirmation_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Сегодня 15:00", callback_data="consult_today_15")
    builder.button(text="Завтра 10:00", callback_data="consult_tomorrow_10")
    builder.button(text="Выбрать другое время", callback_data="consult_custom")
    builder.adjust(1)
    return builder.as_markup()

# Кнопка "Назад" для возврата в главное меню
def back_to_main_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    return builder.as_markup()

def readiness_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да, готов обсудить", callback_data="readiness_yes")
    builder.button(text="👀 Нужны примеры", callback_data="readiness_examples")
    builder.button(text="🤔 Рассматриваю варианты", callback_data="readiness_maybe")
    builder.adjust(1)  # Одна кнопка в строке
    return builder.as_markup()

def after_submit_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Нужны примеры", callback_data="readiness_examples")
    return builder.as_markup()
