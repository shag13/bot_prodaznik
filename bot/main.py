import logging
import json
from pathlib import Path
import re
import os
import asyncio
from keyboards.inline import BOT_EXAMPLES
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, PhotoSize
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
# Импорт собственных модулей
from config import Config
from states.form import Form
from keyboards.inline import (
    main_menu_kb, goals_kb, current_situation_kb, budget_kb,
    timeline_kb, readiness_kb, examples_offer_kb, examples_kb,
    demo_types_kb, beauty_services_kb, time_slots_kb,
    reminder_confirmation_kb, contact_request_kb, bot_constructor_kb,
    consultation_confirmation_kb, trade_submenu_kb, services_submenu_kb,
    education_submenu_kb, production_submenu_kb, food_submenu_kb,
    art_submenu_kb, health_submenu_kb, it_submenu_kb, marketing_submenu_kb,
    other_submenu_kb, considering_options_kb, shop_products_kb, support_questions_kb,
    delivery_options_kb, payment_kb, after_demo_kb, followup_kb
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Middleware для отслеживания активности
class ActivityMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = data.get('event_from_user')
        if user:
            user_id = user.id
            users_data.setdefault(user_id, {})['last_active'] = datetime.now()
        return await handler(event, data)

class AddExample(StatesGroup):
    name = State()        # Имя бота
    description = State() # Описание
    link = State()        # Ссылка

def load_images():
    if Path("images.json").exists():
        with open("images.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return {"message_2": []}  # Только для второго сообщения

def save_images(data):
    with open("images.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_examples():
    file_path = Path("examples.json")
    try:
        # Если файл существует и не пуст
        if file_path.exists() and file_path.stat().st_size > 0:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        # Если файл пуст или не существует
        return []
    except (json.JSONDecodeError, Exception) as e:
        print(f"Ошибка при загрузке файла: {e}. Будет использован пустой список.")
        return []

def save_examples(data):
    with open("examples.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Загружаем данные о примерах
examples_data = load_examples()

# Инициализация бота и диспетчера
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
ADMIN_ID = int(os.getenv("ADMIN_ID"))

dp.update.middleware(ActivityMiddleware())
# Временное хранилище данных
users_data = {}
verification_codes = {}
images_data = load_images()
  
# Словарь для анализа главной задачи
GOALS_ANALYSIS = {
    "goal_sales": "Будет автоматизировать процесс с помощью бота, чтобы сократить время на выполнение рутинных задач и минимизировать ошибки",
    "goal_orders": "Будет принимать заказы через мессенджеры или сайт, автоматически обрабатывать их и передавать в систему учета (например, ERP или CRM)",
    "goal_support": "Будет отвечать на часто задаваемые вопросы (FAQ), обработки жалоб и перенаправления сложных запросов на оператора",
    "goal_promotion": "Будет рассылать информацию о новых услугах, акциях и событиях, а также проводить опросы для сбора обратной связи",
    "goal_leads": "Будет автоматически собирать контактные данные и предпочтения клиентов через формы или диалоги",
}

# Словарь для анализа текущей ситуации
SITUATION_ANALYSIS = {
    "situation_manual": "Также нужно автоматизировать процесс с помощью бота, чтобы сократить время на выполнение рутинных задач и минимизировать ошибки",
    "situation_other_software": "Также нужно интегрировать бота с существующим ПО для расширения функционала и улучшения взаимодействия с клиентами",
    "situation_none": "Также нужно разработать бота с нуля, учитывая специфику задачи и потребности бизнеса",
}

BOT_EXAMPLES = [
    "https://t.me/Flowershop_labot",  # Первый бот
    "https://t.me/LaSell_LaBot",     # Второй бот
    # Добавьте другие ссылки по мере необходимости
]

# Валидация email и телефона
def validate_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

def validate_phone(phone):
    return re.match(r"^\+7\d{10}$", phone)

# Генерация кода подтверждения
def generate_code(length):
    import random
    return ''.join(random.choices('0123456789', k=length))

# Сохранение данных пользователя
def save_user_data(user_id: int):
    try:
        with open(Config.USERS_DATA_PATH, 'a') as f:
            user_data = users_data.get(user_id, {})
            user_data['timestamp'] = datetime.now().isoformat()
            json.dump({str(user_id): user_data}, f)
            f.write('\n')
    except Exception as e:
        logging.error(f"Error saving user data: {e}")

# Уведомление администратора
async def notify_admin(user_data: dict):
    try:
        text = Config.NOTIFICATION_SETTINGS['new_user_template'].format(
            name=user_data.get('name', 'Не указано'),
            niche=user_data.get('niche', 'Не указано'),
            features=', '.join(user_data.get('features', [])),
            contacts=user_data.get('contacts', 'Не указано')
        )
        await bot.send_message(
            chat_id=Config.ADMIN_ID,
            text=text
        )
    except Exception as e:
        logging.error(f"Error notifying admin: {e}")

@dp.message(lambda message: message.from_user.id == ADMIN_ID and message.photo)
async def handle_admin_photo(message: Message):
    global images_data
    
    # Получаем ID картинки
    photo_id = message.photo[-1].file_id  # Берем самую большую версию картинки
    
    # Добавляем картинку только для второго сообщения
    images_data["message_2"].append(photo_id)
    
    # Сохраняем данные
    save_images(images_data)
    
    await message.answer(f"Картинка сохранена для второго сообщения!")

@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    # Отправляем первое сообщение без картинки
    await message.answer(
        "Меня зовут BotCraftedBots, и я — твой помощник в автоматизации бизнеса.\n\n"
        "Мои создатели — семейная пара, которая знает, как сделать твой бизнес эффективнее. Позволь рассказать о них:\n\n"
        "Андрей — автор моего кода, мастер No-code программирования.\n"
        "Высшее образование в направлении 'Товароведение и экспертиза товаров'\n."
        "10 лет опыта в прямых продажах.\n"
        "2 года руководил отделом качества на пищевом производстве.\n"
        "6 лет занимает руководящую должность на градообразующем предприятии.\n\n"
        "Оксана — автор моего интерфейса и контентных воронок.\n"
        "15 лет опыта в продажах B2C и B2B.\n"
        "2 года руководила филиалом типографии, занималась адаптацией и подготовкой персонала.\n"
        "2 года работала с маркетплейсами.\n"
        "Бизнес-аналитик с глубоким пониманием бизнес процессов.\n"
        "Они объединили свой опыт, чтобы создавать ботов, которые действительно помогают бизнесу расти.\n\n"
        "Хочешь узнать, как я могу помочь твоему бизнесу?",
        reply_markup=InlineKeyboardBuilder().button(text="Узнать больше", callback_data="learn_more").as_markup()
    )
    await state.set_state(Form.start)

@dp.callback_query(Form.start, lambda c: c.data == "learn_more")
async def learn_more_handler(callback: CallbackQuery, state: FSMContext):
    global images_data
    
    # Загружаем картинки для второго сообщения
    if images_data["message_2"]:
        photo_id = images_data["message_2"][-1]  # Последняя добавленная картинка
        await callback.message.answer_photo(photo_id)
    
    # Отправляем второе сообщение
    await callback.message.answer(
        "Telegram-боты — это мощный инструмент для бизнеса, который помогает оптимизировать процессы, улучшить взаимодействие с клиентами и повысить эффективность работы. Их внедрение может стать конкурентным преимуществом для компании, особенно в условиях растущей цифровизации.\n\n"
        "Ответьте на 5 вопросов, и я подскажу, какой бот подойдет вашему бизнесу.",
        reply_markup=InlineKeyboardBuilder().button(text="Начнем!", callback_data="start_main").as_markup()
    )
    await state.set_state(Form.learn_more)

@dp.callback_query(Form.learn_more, lambda c: c.data == "start_main")
async def start_main_handler(callback: CallbackQuery, state: FSMContext):
    # Переходим к основному функционалу
    await callback.message.edit_text(
        "👋 Привет! Я помогу создать эффективного Telegram-бота для твоего бизнеса.\n"
        "Давай начнем с нескольких вопросов.\n"
        "Каким видом деятельности ты занимаешься?",
        reply_markup=main_menu_kb()
    )
    await state.set_state(Form.business_niche)



# Функция для проверки неактивных пользователей
async def check_inactive_users():
    while True:
        await asyncio.sleep(60)
        now = datetime.now()
        for user_id in list(users_data.keys()):
            data = users_data.get(user_id, {})
            last_active = data.get('last_active')
            if not last_active:
                continue
            
            inactive_time = now - last_active
            reminders_sent = data.get('reminders_sent', 0)
            
            if inactive_time >= timedelta(minutes=5) and reminders_sent == 0:
                try:
                    state = await dp.storage.get_state(user_id)
                    data['saved_state'] = state
                    builder = InlineKeyboardBuilder()
                    builder.button(text="Продолжить", callback_data="resume_interaction")
                    await bot.send_message(user_id, "Прошло 5 минут, а я все жду, когда ты вернешься ко мне, чтобы собрать своего собственного бота!", reply_markup=builder.as_markup())
                    data['reminders_sent'] = 1
                except Exception as e:
                    logging.error(f"Reminder error: {e}")
            
            elif inactive_time >= timedelta(hours=1) and reminders_sent == 1:
                try:
                    builder = InlineKeyboardBuilder()
                    builder.button(text="Продолжить", callback_data="resume_interaction")
                    await bot.send_message(user_id, "Прошел уже час... а я все еще жду... Жду, когда ты вернешься ко мне, чтобы собрать своего собственного бота!", reply_markup=builder.as_markup())
                    data['reminders_sent'] = 2
                except Exception as e:
                    logging.error(f"Reminder error: {e}")

# Обработчик для кнопки "Продолжить"
@dp.callback_query(lambda c: c.data == "resume_interaction")
async def handle_resume(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = users_data.get(user_id, {})
    saved_state = data.get('saved_state')
    
    if saved_state:
        await state.set_state(saved_state)
        data['reminders_sent'] = 0
        del data['saved_state']
        
        current_state = await state.get_state()
        
        if current_state == Form.business_niche.state:
            await callback.message.answer("Выберите нишу вашего бизнеса:", reply_markup=main_menu_kb())
        elif current_state == Form.goals.state:
            await callback.message.answer("🎯 Выберите главную задачу:", reply_markup=goals_kb())
        elif current_state == Form.current_situation.state:
            await callback.message.answer("🔄 Как вы справляетесь сейчас?", reply_markup=current_situation_kb())
        elif current_state == Form.budget.state:
            await callback.message.answer("💰 Ваш бюджет?", reply_markup=budget_kb())
        elif current_state == Form.timeline.state:
            await callback.message.answer("⏳ Когда планируете начать?", reply_markup=timeline_kb())
        elif current_state == Form.readiness.state:
            await callback.message.answer("Готовы обсудить детали?", reply_markup=readiness_kb())
        else:
            await callback.message.answer("Давайте продолжим!")
    else:
        await callback.message.answer("Начнем сначала! Выберите нишу:", reply_markup=main_menu_kb())
        await state.set_state(Form.business_niche)
    
    await callback.answer()

# Запуск задачи проверки неактивных пользователей
async def on_startup():
    asyncio.create_task(check_inactive_users())

# Регистрация задачи при запуске бота
dp.startup.register(on_startup)

# Основной опрос
@dp.callback_query(Form.business_niche)
async def process_niche(callback: CallbackQuery, state: FSMContext):
    niche = callback.data.split('_')[1]
    
    if niche == "trade":
        await callback.message.edit_text(
            "Выберите сферу торговли:",
            reply_markup=trade_submenu_kb()
        )
    elif niche == "services":
        await callback.message.edit_text(
            "Выберите сферу услуг:",
            reply_markup=services_submenu_kb()
        )
    elif niche == "education":
        await callback.message.edit_text(
            "Выберите сферу образования:",
            reply_markup=education_submenu_kb()
        )
    elif niche == "production":
        await callback.message.edit_text(
            "Выберите сферу производства:",
            reply_markup=production_submenu_kb()
        )
    elif niche == "food":
        await callback.message.edit_text(
            "Выберите сферу общественного питания:",
            reply_markup=food_submenu_kb()
        )
    elif niche == "art":
        await callback.message.edit_text(
            "Выберите сферу творчества и искусства:",
            reply_markup=art_submenu_kb()
        )
    elif niche == "health":
        await callback.message.edit_text(
            "Выберите сферу здоровья и красоты:",
            reply_markup=health_submenu_kb()
        )
    elif niche == "it":
        await callback.message.edit_text(
            "Выберите IT-направление:",
            reply_markup=it_submenu_kb()
        )
    elif niche == "marketing":
        await callback.message.edit_text(
            "Выберите сферу маркетинга:",
            reply_markup=marketing_submenu_kb()
        )
    elif niche == "other":
        await callback.message.edit_text(
            "Выберите категорию:",
            reply_markup=other_submenu_kb()
        )
        
    # Сохраняем выбранную основную категорию
    users_data[callback.from_user.id] = {'main_niche': niche}
    await state.set_state(Form.business_subniche)

@dp.callback_query(lambda c: c.data.startswith("trade_") or
                             c.data.startswith("services_") or
                             c.data.startswith("education_") or
                             c.data.startswith("production_") or
                             c.data.startswith("food_") or
                             c.data.startswith("art_") or
                             c.data.startswith("health_") or
                             c.data.startswith("it_") or
                             c.data.startswith("marketing_") or
                             c.data.startswith("other_"))

async def process_submenu(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id] = {'niche': callback.data}
    await callback.message.edit_text(
        "🎯 Какую главную задачу вы хотите решить с помощью бота?",
        reply_markup=goals_kb()
    )
    await state.set_state(Form.goals)        

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Выберите нишу вашего бизнеса:",
        reply_markup=main_menu_kb()
    )
    await state.set_state(Form.business_niche)

@dp.callback_query(Form.goals)
async def process_goals(callback: CallbackQuery, state: FSMContext):
    # Сохраняем выбранную цель
    users_data[callback.from_user.id] = {'goal': callback.data}  # callback.data = "goal_sales", "goal_orders", и т.д.
    await callback.message.edit_text(
        "🔄 Как вы сейчас справляетесь с этой задачей?",
        reply_markup=current_situation_kb()
    )
    await state.set_state(Form.current_situation)

@dp.callback_query(Form.current_situation)
async def process_current_situation(callback: CallbackQuery, state: FSMContext):
    # Сохраняем текущую ситуацию
    users_data[callback.from_user.id]['situation'] = callback.data  # callback.data = "situation_manual", "situation_other_software", и т.д.
    await callback.message.edit_text(
        "💰 Какой бюджет вы готовы выделить на решение задачи?",
        reply_markup=budget_kb()
    )
    await state.set_state(Form.budget)

@dp.callback_query(Form.budget)
async def process_budget(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id]['budget'] = callback.data.split('_')[1]
    await callback.message.edit_text(
        "⏳ Когда вы планируете начать работу над решением задачи?",
        reply_markup=timeline_kb()
    )
    await state.set_state(Form.timeline)

@dp.callback_query(Form.timeline)
async def process_timeline(callback: CallbackQuery, state: FSMContext):
    # Получаем данные пользователя
    user_data = users_data.get(callback.from_user.id, {})
    goal = user_data.get('goal', 'не указана')
    situation = user_data.get('situation', 'не указана')
    
    # Анализируем ответы пользователя
    goal_analysis = GOALS_ANALYSIS.get(goal, "Неизвестная задача")
    situation_analysis = SITUATION_ANALYSIS.get(situation, "Неизвестная ситуация")
    
    # Формируем итоговое сообщение
    summary_message = (
        f"Похоже, вам нужен бот, который:\n"
        f"- {goal_analysis}\n"
        f"- {situation_analysis}\n\n"
        f"Готовы ли вы обсудить детали и получить персональное предложение?"
    )
    
    # Клавиатура с вариантами ответа
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да, готов обсудить", callback_data="readiness_yes")
    builder.button(text="👀 Нужны примеры", callback_data="readiness_examples")
    builder.button(text="🤔 Рассматриваю варианты", callback_data="readiness_maybe")
    builder.adjust(1)  # Одна кнопка в строке
    
    await callback.message.edit_text(
        summary_message,
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.readiness)

# Обработчик команды /add
@dp.message(Command("add"))
async def add_example_start(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:  # Проверяем, что это админ
        await message.answer("Введите имя бота:")
        await state.set_state(AddExample.name)

# Обработчик для ввода имени
@dp.message(AddExample.name)
async def add_example_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание бота:")
    await state.set_state(AddExample.description)

# Обработчик для ввода описания
@dp.message(AddExample.description)
async def add_example_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите ссылку на бота:")
    await state.set_state(AddExample.link)

# Обработчик для ввода ссылки
@dp.message(AddExample.link)
async def add_example_link(message: Message, state: FSMContext):
    global examples_data
    
    # Получаем данные из состояния
    data = await state.get_data()
    name = data.get("name")
    description = data.get("description")
    link = message.text
    
    # Добавляем новый пример
    examples_data.append({
        "name": name,
        "description": description,
        "link": link,
    })
    
    # Сохраняем данные
    save_examples(examples_data)
    
    await message.answer(f"Пример бота '{name}' успешно добавлен!")
    await state.clear()
    
@dp.callback_query(Form.readiness)
async def process_readiness(callback: CallbackQuery, state: FSMContext):
    user_response = callback.data.split('_')[1]
    
    if user_response == "yes":
        await callback.message.edit_text(
            "Отлично! Давайте создадим вашего бота. Выберите необходимые функции:",
            reply_markup=bot_constructor_kb()
        )
        await state.set_state(Form.bot_constructor)
    elif user_response == "examples":
        # Показываем первый пример с полным описанием
        if examples_data:  # Проверяем, что есть примеры
            example = examples_data[0]  # Берем первый пример
            await callback.message.edit_text(
                f"Пример бота:\n\n"
                f"Имя: {example['name']}\n"
                f"Описание: {example['description']}\n"
                f"Ссылка: {example['link']}",
                reply_markup=examples_kb(examples_data, 0)  # Передаем данные и индекс
            )
            await state.set_state(Form.examples_show)
        else:
            await callback.message.edit_text(
                "Примеры ботов пока отсутствуют.",
                reply_markup=InlineKeyboardBuilder().button(text="🔙 Назад в меню", callback_data="back_to_readiness").as_markup()
            )
    elif user_response == "maybe":
        await callback.message.edit_text(
            "Так как все возможности ботов описать просто невозможно, укажите свое видение, и администратор свяжется с вами для уточнения деталей.",
            reply_markup=considering_options_kb()
        )
        await state.set_state(Form.considering_options)

@dp.callback_query(lambda c: c.data == "back_to_readiness")
async def back_to_readiness(callback: CallbackQuery, state: FSMContext):
    # Возвращаем пользователя в меню выбора готовности
    await callback.message.edit_text(
        "Готовы ли вы обсудить детали и получить персональное предложение?",
        reply_markup=readiness_kb()
    )
    await state.set_state(Form.readiness)

@dp.callback_query(Form.considering_options)
async def process_considering_options(callback: CallbackQuery, state: FSMContext):
    if callback.data == "write_vision":
        await callback.message.answer(
            "Напишите свое видение бота:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Form.user_vision_input)
    elif callback.data == "back_to_readiness":
        await callback.message.edit_text(
            "Готовы ли вы обсудить детали и получить персональное предложение?",
            reply_markup=readiness_kb()
        )
        await state.set_state(Form.readiness)

@dp.message(Form.user_vision_input)
async def process_user_vision(message: Message, state: FSMContext):
    user_vision = message.text
    admin_message = (
        f"Смотрящий {message.from_user.full_name} (@{message.from_user.username}) хочет:\n"
        f"{user_vision}"
    )
    
    # Отправляем уведомление администратору
    await bot.send_message(
        chat_id=Config.ADMIN_ID,
        text=admin_message
    )
    
    # Завершаем диалог
    await message.answer(
        "Спасибо! Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()

@dp.callback_query(Form.bot_constructor)
async def process_bot_constructor(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = callback.data
    
    if data == "features_done":
        # Получаем выбранные функции
        user_data = users_data.get(user_id, {})
        selected_features = user_data.get('selected_features', [])
        
        # Запрашиваем номер телефона
        await callback.message.answer("Пожалуйста, введите ваш номер телефона для связи:")
        await state.set_state(Form.user_phone_input)
        
    elif data == "back_to_readiness":
        # Возвращаемся к вопросу о готовности
        await callback.message.edit_text(
            "Готовы ли вы обсудить детали и получить персональное предложение?",
            reply_markup=readiness_kb()
        )
        await state.set_state(Form.readiness)
    else:
        # Обработка выбора функций
        feature = data.split('_')[1]
        user_data = users_data.get(user_id, {})
        
        if 'selected_features' not in user_data:
            user_data['selected_features'] = set()
        
        if feature in user_data['selected_features']:
            user_data['selected_features'].remove(feature)
        else:
            user_data['selected_features'].add(feature)
        
        users_data[user_id] = user_data
        
        # Обновляем клавиатуру
        await callback.message.edit_text(
            "Выберите необходимые функции:",
            reply_markup=bot_constructor_kb(user_data['selected_features'])
        )
        
@dp.callback_query(lambda c: c.data == "readiness_examples")
async def show_examples(callback: types.CallbackQuery, state: FSMContext):
    if examples_data:  # Проверяем, что есть примеры
        example = examples_data[0]  # Берем первый пример
        await callback.message.edit_text(
            f"Пример бота:\n\n"
            f"Имя: {example['name']}\n"
            f"Описание: {example['description']}\n"
            f"Ссылка: {example['link']}",
            reply_markup=examples_kb(examples_data, 0)  # Передаем данные и индекс
        )
        await state.set_state(Form.examples_show)
    else:
        await callback.message.edit_text(
            "Примеры ботов пока отсутствуют.",
            reply_markup=InlineKeyboardBuilder().button(text="🔙 Назад в меню", callback_data="back_to_readiness").as_markup()
        )

@dp.callback_query(lambda c: c.data == "demo_start")
async def start_demo(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Выберите тип демо-режима:",
        reply_markup=demo_types_kb()
    )
    await state.set_state(Form.demo_type_selection)

@dp.callback_query(lambda c: c.data.startswith("example_"))
async def handle_examples(callback: types.CallbackQuery, state: FSMContext):
    action, *data = callback.data.split("_")
    example_index = int(data[-1])  # Получаем индекс из callback.data

    # Проверяем границы индекса
    if example_index < 0 or example_index >= len(examples_data):
        example_index = 0

    # Получаем пример
    example = examples_data[example_index]

    # Обновляем сообщение
    await callback.message.edit_text(
        f"Пример бота:\n\n"
        f"Имя: {example['name']}\n"
        f"Описание: {example['description']}\n"
        f"Ссылка: {example['link']}",
        reply_markup=examples_kb(examples_data, example_index)  # Передаем оба аргумента
    )

@dp.callback_query(Form.demo_type_selection)
async def select_demo_type(callback: CallbackQuery, state: FSMContext):
    if callback.data == "back_to_examples":
        await callback.message.edit_text(
            "Вот примеры успешных ботов:",
            reply_markup=examples_kb(examples_data, 0)  # Добавляем examples_data
        )
        await state.set_state(Form.examples_show)
    else:
        demo_type = callback.data.split('_')[1]
        
        if demo_type == 'beauty':
            await callback.message.edit_text(
                "💅 Попробуй запись в салон красоты!\nВыбери услугу:",
                reply_markup=beauty_services_kb()
            )
            await state.set_state(Form.demo_beauty_service)
        elif demo_type == 'shop':
            await callback.message.edit_text(
                "🛍 Попробуй онлайн-заказ!\nВыбери товар:",
                reply_markup=shop_products_kb()
            )
            await state.set_state(Form.demo_shop_product)
        elif demo_type == 'support':
            await callback.message.edit_text(
                "💬 Попробуй чат с поддержкой!\nВыбери вопрос:",
                reply_markup=support_questions_kb()
            )
            await state.set_state(Form.demo_support_question)

@dp.callback_query(lambda c: c.data == "back_to_examples")
async def back_to_examples(callback: CallbackQuery, state: FSMContext):
    # Показываем первую страницу примеров
    current_link = BOT_EXAMPLES[0]  # Первая ссылка
    keyboard = examples_kb(0)       # Клавиатура для первой страницы
    await callback.message.edit_text(
        f"Пример бота:\n{current_link}",
        reply_markup=keyboard
    )
    await state.set_state(Form.examples_show)
            
# Демо: Онлайн-заказ (магазин)
@dp.callback_query(Form.demo_shop_product)
async def select_shop_product(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id]['demo_product'] = callback.data
    await callback.message.edit_text(
        "🏠 Укажи адрес доставки или выбери пункт самовывоза:",
        reply_markup=delivery_options_kb()
    )
    await state.set_state(Form.demo_shop_address)

@dp.callback_query(Form.demo_shop_address)
async def select_shop_address(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id]['demo_address'] = callback.data
    await callback.message.edit_text(
        "💳 Сумма к оплате: 5 000 руб.\n"
        "Оплати заказ через Telegram.",
        reply_markup=payment_kb()
    )
    await state.set_state(Form.demo_shop_payment)

@dp.callback_query(Form.demo_shop_payment)
async def confirm_shop_payment(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id]['demo_payment'] = callback.data
    
    # Формируем сообщение для администратора
    admin_message = (
        "Новый заказ через демо-режим!\n"
        f"Пользователь: {callback.from_user.full_name} (@{callback.from_user.username})\n"
        f"Товар: {users_data[callback.from_user.id]['demo_product']}\n"
        f"Адрес: {users_data[callback.from_user.id]['demo_address']}\n"
        f"Оплата: {'Оплачено' if callback.data == 'payment_confirm' else 'Не оплачено'}"
    )
    
    # Отправляем уведомление администратору
    await bot.send_message(
        chat_id=Config.ADMIN_ID,
        text=admin_message
    )
    
    # Завершаем демо-режим
    await callback.message.edit_text(
        "✅ Заказ успешно оформлен!\n"
        "Это упрощенный вариант функционала.\n\n"
        "Администратор получил уведомление о вашем заказе.",
        reply_markup=after_demo_kb()
    )
    await state.set_state(Form.after_demo)

# Демо: Поддержка клиентов (чат с FAQ)
@dp.callback_query(Form.demo_support_question)
async def select_support_question(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id]['demo_question'] = callback.data
    await callback.message.edit_text(
        "📦 Твой заказ в пути. Ожидай доставку 20 ноября.\n"
        "Хочешь отследить заказ?",
        reply_markup=followup_kb()
    )
    await state.set_state(Form.demo_support_followup)

@dp.callback_query(Form.demo_support_followup)
async def confirm_support_followup(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id]['demo_followup'] = callback.data
    
    # Формируем сообщение для администратора
    admin_message = (
        "Новый запрос через демо-режим поддержки!\n"
        f"Пользователь: {callback.from_user.full_name} (@{callback.from_user.username})\n"
        f"Вопрос: {users_data[callback.from_user.id]['demo_question']}\n"
        f"Дополнительные действия: {'Да' if callback.data == 'followup_yes' else 'Нет'}"
    )
    
    # Отправляем уведомление администратору
    await bot.send_message(
        chat_id=Config.ADMIN_ID,
        text=admin_message
    )
    
    # Завершаем демо-режим
    await callback.message.edit_text(
        "✅ Вот как будет работать твой бот!\n"
        "Это упрощенный вариант функционала.\n\n"
        "Администратор получил уведомление о вашем запросе.",
        reply_markup=after_demo_kb()
    )
    await state.set_state(Form.after_demo)

# После завершения демо-режима
@dp.callback_query(Form.after_demo)
async def after_demo(callback: CallbackQuery, state: FSMContext):
    if callback.data == "ready_to_discuss":
        await callback.message.answer(
            "Отлично! Давайте обсудим детали. Введите ваше имя:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Form.user_name_input)
    elif callback.data == "create_my_bot":
        await callback.message.edit_text(
            "Выберите необходимые функции:",
            reply_markup=bot_constructor_kb()
        )
        await state.set_state(Form.bot_constructor)

@dp.message(Form.user_name_input)
async def process_user_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer("Теперь введите ваш номер телефона:")
    await state.set_state(Form.user_phone_input)

@dp.message(Form.user_phone_input)
async def process_user_phone(message: types.Message, state: FSMContext):
    if validate_phone(message.text):
        await state.update_data(user_phone=message.text)
        
        # Формируем сообщение для администратора
        user_data = await state.get_data()
        admin_message = (
            "Новая заявка!\n"
            f"Пользователь: {message.from_user.full_name} (@{message.from_user.username})\n"
            f"Телефон: {user_data['user_phone']}\n"
            f"Выбранные функции: {', '.join(user_data.get('selected_features', []))}"
        )
        
        # Отправляем уведомление администратору
        await bot.send_message(
            chat_id=Config.ADMIN_ID,
            text=admin_message
        )
        
        # Завершаем диалог
        await message.answer(
            "Спасибо! Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.",
            reply_markup=InlineKeyboardBuilder().button(text="Нужны примеры", callback_data="readiness_examples").as_markup()
        )
        await state.clear()
    else:
        await message.answer("Некорректный номер телефона. Попробуйте еще раз.")

@dp.message(Form.user_email_input)
async def process_user_email(message: Message, state: FSMContext):
    if validate_email(message.text):
        await state.update_data(user_email=message.text)
        user_data = await state.get_data()
        
        # Формируем сообщение для администратора
        admin_message = (
            "Новая заявка на обсуждение!\n"
            f"Пользователь: {user_data['user_name']}\n"
            f"Телефон: {user_data['user_phone']}\n"
            f"Email: {user_data['user_email']}\n"
            f"Демо-режим: Интернет-магазин"
        )
        
        # Отправляем уведомление администратору
        await bot.send_message(
            chat_id=Config.ADMIN_ID,
            text=admin_message
        )
        
        # Завершаем диалог
        await message.answer(
            "Наш менеджер свяжется с вами в ближайшее время.",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
    else:
        await message.answer("Некорректный email. Попробуйте еще раз.")
        
@dp.callback_query(Form.demo_beauty_service)
async def select_beauty_service(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id]['demo_service'] = callback.data
    await callback.message.edit_text(
        "📅 Выбери удобное время:",
        reply_markup=time_slots_kb()
    )
    await state.set_state(Form.demo_beauty_time)

@dp.callback_query(Form.demo_beauty_time)
async def select_beauty_time(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id]['demo_time'] = callback.data
    await callback.message.edit_text(
        "⏰ Хочешь получить напоминание за час до записи?",
        reply_markup=reminder_confirmation_kb()
    )
    await state.set_state(Form.demo_beauty_reminder)

@dp.callback_query(Form.demo_beauty_reminder)
async def confirm_beauty_reminder(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id]['demo_reminder'] = callback.data == 'reminder_yes'
    await callback.message.edit_text(
        "✅ Запись успешно оформлена!\n"
        "Хочешь создать такого бота для своего бизнеса?",
        reply_markup=examples_offer_kb()
    )
    await state.set_state(Form.examples_offer)

# Сбор контактов
@dp.callback_query(Form.contact_method)
async def select_contact_method(callback: CallbackQuery, state: FSMContext):
    method = callback.data.split('_')[1]
    if method == 'email':
        await callback.message.answer("Введите ваш email:")
        await state.set_state(Form.contact_email_input)
    elif method == 'phone':
        await callback.message.answer("Введите ваш телефон в формате +79991234567:")
        await state.set_state(Form.contact_phone_input)

@dp.message(Form.contact_email_input)
async def process_email(message: Message, state: FSMContext):
    if validate_email(message.text):
        code = generate_code(Config.VERIFICATION['email_code_length'])
        verification_codes[message.from_user.id] = code
        await message.answer(f"Код подтверждения отправлен на {message.text}. Введите его:")
        await state.set_state(Form.contact_verification)
    else:
        await message.answer("Некорректный email. Попробуйте еще раз.")

@dp.message(Form.contact_phone_input)
async def process_phone(message: Message, state: FSMContext):
    if validate_phone(message.text):
        code = generate_code(Config.VERIFICATION['sms_code_length'])
        verification_codes[message.from_user.id] = code
        await message.answer(f"Код подтверждения отправлен на {message.text}. Введите его:")
        await state.set_state(Form.contact_verification)
    else:
        await message.answer("Некорректный телефон. Попробуйте еще раз.")

@dp.message(Form.contact_verification)
async def verify_code(message: Message, state: FSMContext):
    if message.text == verification_codes.get(message.from_user.id):
        await message.answer("Код подтвержден! Спасибо.")
        await state.set_state(Form.constructor_features)
    else:
        await message.answer("Неверный код. Попробуйте еще раз.")

# Конструктор бота
@dp.callback_query(Form.constructor_features)
async def select_features(callback: CallbackQuery, state: FSMContext):
    feature = callback.data.split('_')[1]
    user_id = callback.from_user.id
    
    if 'features' not in users_data[user_id]:
        users_data[user_id]['features'] = []
    
    if feature == 'done':
        total = Config.PRICING['base_price']
        for f in users_data[user_id]['features']:
            total += Config.PRICING[f]
        
        await callback.message.edit_text(
            f"💰 Итоговая стоимость: {total} руб.\n"
            "Хочешь записаться на консультацию?",
            reply_markup=consultation_confirmation_kb()
        )
        await state.set_state(Form.consultation_time)
    else:
        users_data[user_id]['features'].append(feature)
        await callback.message.edit_text(
            "✅ Функция добавлена!\nПродолжи выбор:",
            reply_markup=bot_constructor_kb()
        )

@dp.message(Command("del"))
async def delete_example_start(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:  # Проверяем, что это админ
        await message.answer("Введите название бота, который нужно удалить:")
        await state.set_state(Form.delete_example)

@dp.message(Form.delete_example)
async def delete_example_by_name(message: Message, state: FSMContext):
    global examples_data
    
    # Получаем название бота из сообщения
    bot_name = message.text.strip()
    
    # Ищем бота по названию
    found = False
    for example in examples_data:
        if example["name"].lower() == bot_name.lower():
            examples_data.remove(example)
            found = True
            break
    
    if found:
        # Сохраняем обновленные данные
        save_examples(examples_data)
        await message.answer(f"Пример бота '{bot_name}' успешно удален!")
    else:
        await message.answer(f"Пример бота с названием '{bot_name}' не найден.")
    
    await state.clear()

# Запись на консультацию
@dp.callback_query(Form.consultation_time)
async def select_consultation_time(callback: CallbackQuery, state: FSMContext):
    users_data[callback.from_user.id]['consultation_time'] = callback.data
    await callback.message.edit_text(
        "✅ Запись на консультацию оформлена!\n"
        "Ссылка на Zoom придет за час до встречи.",
        reply_markup=ReplyKeyboardRemove()
    )
    await notify_admin(users_data[callback.from_user.id])
    await state.clear()

# Запуск бота
if __name__ == '__main__':
    try:
        logging.info("Бот запущен")
        dp.run_polling(bot)
    except Exception as e:
        logging.critical(f"Ошибка при запуске бота: {e}")
