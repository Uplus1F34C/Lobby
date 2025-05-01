from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Импорты проекта
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TGbot.config import settings
from DataBase import Func
from DataBase.settings.models import level, kvant

# =================================================================================
# НАСТРОЙКА БОТА
# =================================================================================

# Инициализация бота и диспетчера
bot = Bot(token=settings.get_token)
dp = Dispatcher()

# =================================================================================
# СОСТОЯНИЯ FSM (Finite State Machine)
# =================================================================================

class WaitCode(StatesGroup):
    """Состояния для ожидания кода регистрации"""
    reg_teacher = State()
    reg_student = State()
    del_student = State()

class AddStudent(StatesGroup):
    """Состояния для добавления нового студента"""
    name = State()
    surname = State()
    patronymic = State()
    kvant = State()
    level = State()
    num = State()

class GetCode(StatesGroup):
    """Состояния для получения кода студента по ФИО"""
    name = State()
    surname = State()
    patronymic = State()

class DeleteStudent(StatesGroup):
    """Состояния для удаления студента по ФИО"""
    id = State()
    name = State()
    surname = State()
    patronymic = State()

# =================================================================================
# ОСНОВНЫЕ КОМАНДЫ
# =================================================================================

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обработчик команд /start
    Определяет роль пользователя и показывает соответствующее меню
    """
    # Проверка на учителя
    teacher_auth = await Func.log_teacher(message.from_user.id)
    if teacher_auth["status"]:
        teacher_info = await Func.log_teacher(message.from_user.id)
        
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="👨‍🎓 Добавить студента",
            callback_data="add_student__cd"))
        builder.add(InlineKeyboardButton(
            text="🗑️ Удалить студента",
            callback_data="delete_student__cd"))
        builder.add(InlineKeyboardButton(
            text="🔑 Получить код ученика",
            callback_data="get_code__cd"))
        builder.add(InlineKeyboardButton(
            text="🚪 Выйти из аккаунта",
            callback_data="exit_teacher__cd"))
        builder.adjust(1, 1, 1, 1)

        welcome_message = (
            f"👋 Здравствуйте, {teacher_info['name']} {teacher_info['patronymic']}!\n\n"
            "📚 С помощью этого бота вы можете управлять базой данных проекта 'Lobby'\n\n"
            "🔹 Выберите действие из меню ниже:"
        )
        try:
            await message.message.answer(welcome_message, reply_markup=builder.as_markup())
        except:
            await message.answer(welcome_message, reply_markup=builder.as_markup())
        return

    # Проверка на студента
    student_auth = await Func.log_student_tg(message.from_user.id)
    if student_auth["status"]:
        student_info = await Func.log_student_tg(message.from_user.id)

        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="🌐 Lobby",
            web_app=WebAppInfo(url=f"{settings.get_url()}?student_id={message.from_user.id}")))
        builder.add(InlineKeyboardButton(
            text="📊 Отправить опрос",
            callback_data="post_que__cd"))
        builder.add(InlineKeyboardButton(
            text="💡 Предложить идею",
            callback_data="post_idea__cd"))
        builder.add(InlineKeyboardButton(
            text="🚪 Выйти из аккаунта",
            callback_data="exit_student__cd"))
        builder.adjust(1, 2, 1)

        welcome_message = (
            f"👋 Привет, {student_info['name']}!\n\n"
            "🤖 Этот бот - универсальный инструмент любого кванторианца!\n\n"
            "🔹 Я могу:\n"
            "• 🌐 Открыть 'Lobby' - интерактивную платформу ученика\n"
            "• 📊 Отправить опрос для проекта в концретные группы\n"
            "• 💡 Принять идеи по улучшению проекта"
            "• 📰 Делать рассылки конкретным группам (уведомления о мероприятиях, работе кванториума и образовательном процессе)\n"
        )

        try:
            await message.message.answer(welcome_message, reply_markup=builder.as_markup())
        except:
            await message.answer(welcome_message, reply_markup=builder.as_markup())
        return

    # Меню для неавторизованных пользователей
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="👨‍🏫 Я учитель",
        callback_data="role_teacher__cd"))
    builder.add(InlineKeyboardButton(
        text="👨‍🎓 Я ученик",
        callback_data="role_student__cd"))
    builder.add(InlineKeyboardButton(
        text="👀 Я гость",
        callback_data="role_guest__cd"))
    builder.adjust(1, 2)

    welcome_message = "👋 Добро пожаловать! Для начала работы выберите свою роль:"

    try:
        await message.message.answer(welcome_message, reply_markup=builder.as_markup())
    except:
        await message.answer(welcome_message, reply_markup=builder.as_markup())



@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    """
    Обработчик команды /menu\
    """
    # Проверка на учителя
    teacher_auth = await Func.log_teacher(message.from_user.id)
    if teacher_auth["status"]:
        teacher_info = await Func.log_teacher(message.from_user.id)
        
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="👨‍🎓 Добавить студента",
            callback_data="add_student__cd"))
        builder.add(InlineKeyboardButton(
            text="🗑️ Удалить студента",
            callback_data="delete_student__cd"))
        builder.add(InlineKeyboardButton(
            text="🔑 Получить код ученика",
            callback_data="get_code__cd"))
        builder.add(InlineKeyboardButton(
            text="🚪 Выйти из аккаунта",
            callback_data="exit_teacher__cd"))
        builder.adjust(1, 1, 1, 1)

        welcome_message = (
            "🔹 Выберите действие из меню ниже:"
        )
        try:
            await message.message.answer(welcome_message, reply_markup=builder.as_markup())
        except:
            await message.answer(welcome_message, reply_markup=builder.as_markup())
        return

    # Проверка на студента
    student_auth = await Func.log_student_tg(message.from_user.id)
    if student_auth["status"]:
        student_info = await Func.log_student_tg(message.from_user.id)

        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="🌐 Lobby",
            web_app=WebAppInfo(url=f"{settings.get_url()}?student_id={message.from_user.id}")))
        builder.add(InlineKeyboardButton(
            text="📊 Отправить опрос",
            callback_data="post_que__cd"))
        builder.add(InlineKeyboardButton(
            text="💡 Предложить идею",
            callback_data="post_idea__cd"))
        builder.add(InlineKeyboardButton(
            text="🚪 Выйти из аккаунта",
            callback_data="exit_student__cd"))
        builder.adjust(1, 2, 1)

        welcome_message = (
            "🔹 Выбери действие из меню ниже:"
        )

        try:
            await message.message.answer(welcome_message, reply_markup=builder.as_markup())
        except:
            await message.answer(welcome_message, reply_markup=builder.as_markup())
        return

    await cmd_start(message)


# =================================================================================
# ОБРАБОТЧИКИ ДЛЯ УЧИТЕЛЕЙ
# =================================================================================

@dp.callback_query(F.data == "role_teacher__cd")
async def reg_teacher(callback: CallbackQuery, state: FSMContext):
    """Начало регистрации учителя"""
    await state.set_state(WaitCode.reg_teacher)
    await callback.message.answer(
        "🔑 Для регистрации введите ваш уникальный код доступа:\n\n"
        "❗ Если у вас нет кода, обратитесь к администратору системы"
    )
    await callback.answer()

@dp.message(WaitCode.reg_teacher)
async def reg_teacher_2(message: Message, state: FSMContext):
    """Завершение регистрации учителя"""
    registration_code = message.text.strip()
    result = await Func.reg_teacher(message.from_user.id, registration_code)

    if result["status"]:
        await message.answer("✅ Регистрация успешно завершена! Теперь у вас есть доступ к управлению базой данных.")
        await cmd_start(message)
    else:
        await message.answer(f"❌ Ошибка регистрации: {result['info']}\n\nПопробуйте еще раз или обратитесь к администратору.")

    await state.clear()

@dp.callback_query(F.data == "cancel_operation__cd")
async def cancel_operation(callback: CallbackQuery, state: FSMContext):
    """Отмена текущей операции"""
    await state.clear()
    await callback.message.answer("❌ Операция отменена")
    await cmd_menu(callback)
    await callback.answer()

@dp.callback_query(F.data == "add_student__cd")
async def start_adding_student(callback: CallbackQuery, state: FSMContext):
    """Начало процесса добавления студента"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить добавление",
        callback_data="cancel_operation__cd"))
    
    await state.set_state(AddStudent.name)
    await callback.message.answer(
        "🤖 Начинаем процесс добавления нового студента\n\n"
        "👤 Введите имя студента:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

@dp.message(AddStudent.name)
async def process_student_name(message: Message, state: FSMContext):
    """Обработка имени студента"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить добавление",
        callback_data="cancel_operation__cd"))
    
    await state.update_data(name=message.text.strip())
    await message.answer(
        "📛 Введите фамилию студента:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(AddStudent.surname)

@dp.message(AddStudent.surname)
async def process_student_surname(message: Message, state: FSMContext):
    """Обработка фамилии студента"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить добавление",
        callback_data="cancel_operation__cd"))
    
    await state.update_data(surname=message.text.strip())
    await message.answer(
        "🔤 Введите отчество студента:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(AddStudent.patronymic)

@dp.message(AddStudent.patronymic)
async def process_student_patronymic(message: Message, state: FSMContext):
    """Обработка отчества студента"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить добавление",
        callback_data="cancel_operation__cd"))
    
    await state.update_data(patronymic=message.text.strip())
    await message.answer(
        f"📚 Введите направление (квант) студента:\n\nДоступные варианты: {', '.join([l.value for l in kvant])}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(AddStudent.kvant)

@dp.message(AddStudent.kvant)
async def process_student_kvant(message: Message, state: FSMContext):
    """Обработка направления (кванта) студента"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить добавление",
        callback_data="cancel_operation__cd"))
    
    await state.update_data(kvant=message.text.strip())
    await message.answer(
        f"📊 Введите уровень студента:\n\nДоступные варианты: {', '.join([l.value for l in level])}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(AddStudent.level)

@dp.message(AddStudent.level)
async def process_student_level(message: Message, state: FSMContext):
    """Обработка уровня студента"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить добавление",
        callback_data="cancel_operation__cd"))
    
    await state.update_data(level=message.text.strip())
    await message.answer(
        "🔢 Введите номер группы студента (от 1 до 4):",
        reply_markup=builder.as_markup()
    )
    await state.set_state(AddStudent.num)

@dp.message(AddStudent.num)
async def process_student_num(message: Message, state: FSMContext):
    """Завершение добавления студента"""
    data = await state.get_data()
    
    result = await Func.insert_student(
        name=data.get('name'),
        surname=data.get('surname'),
        patronymic=data.get('patronymic'),
        level=data.get('level'),
        kvant=data.get('kvant'),
        group_num=message.text.strip()
    )
    
    student_info = (
        f"📋 Информация о студенте:\n\n"
        f"👤 Имя: {data.get('name')}\n"
        f"📛 Фамилия: {data.get('surname')}\n"
        f"🔤 Отчество: {data.get('patronymic')}\n"
        f"🏷️ Группа: {data.get('level')}-{data.get('kvant')}-{message.text.strip()}\n"
        f"🗝️ Код: {result["code"]}"
    )
    
    if result['status']:
        await message.answer(
            f"{student_info}\n\n"
            f"✅ Студент успешно добавлен в базу данных!\n"
            f"📌 ID: {result.get('id', 'не указан')}"
        )
    else:
        await message.answer(
            f"{student_info}\n\n"
            f"❌ Ошибка при добавлении студента:\n"
            f"{result['info']}"
        )

    await cmd_menu(message)
    await state.clear()


@dp.callback_query(F.data == "delete_student__cd")
async def delete_student_by_fio(callback: CallbackQuery, state: FSMContext):
    """Начало процесса удаления студента с выбором метода"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🔢 По ID",
        callback_data="delete_student_by_id__cd"))
    builder.add(InlineKeyboardButton(
        text="👤 По ФИО",
        callback_data="delete_student_by_fio__cd"))
    builder.add(InlineKeyboardButton(
        text="❌ Отменить",
        callback_data="cancel_operation__cd"))
    builder.adjust(2, 1)
    
    await callback.message.answer(
        "🤖 Выберите способ удаления студента:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@dp.callback_query(F.data == "delete_student_by_id__cd")
async def delete_student_by_id_start(callback: CallbackQuery, state: FSMContext):
    """Начало процесса удаления студента по ID"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить удаление",
        callback_data="cancel_operation__cd"))
    
    await state.set_state(DeleteStudent.id)
    await callback.message.answer(
        "🔢 Введите ID студента для удаления:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

@dp.message(DeleteStudent.id)
async def process_delete_id(message: Message, state: FSMContext):
    """Обработка ID для удаления"""
    student_id = message.text.strip()
    
    try:
        student_id = int(student_id)  # Проверяем, что ID - число
        result = await Func.delete_student(student_id=student_id)
        
        if result["status"]:
            await message.answer(f"✅ Студент с ID {student_id} успешно удален из системы!")
        else:
            await message.answer(f"❌ Ошибка при удалении студента:\n{result['info']}")
    except ValueError:
        await message.answer("❌ ID должен быть числом. Пожалуйста, введите корректный ID.")
        return
    
    await cmd_menu(message)
    await state.clear()


@dp.callback_query(F.data == "delete_student_by_fio__cd")
async def delete_student_by_fio(callback: CallbackQuery, state: FSMContext):
    """Начало процесса удаления студента по ФИО"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить удаление",
        callback_data="cancel_operation__cd"))
    
    await state.set_state(DeleteStudent.name)
    await callback.message.answer(
        "🤖 Начинаем процесс удаления студента\n\n"
        "👤 Введите имя студента:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

@dp.message(DeleteStudent.name)
async def process_delete_name(message: Message, state: FSMContext):
    """Обработка имени для удаления"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить удаление",
        callback_data="cancel_operation__cd"))
    
    await state.update_data(name=message.text.strip())
    await message.answer(
        "📛 Введите фамилию студента:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(DeleteStudent.surname)

@dp.message(DeleteStudent.surname)
async def process_delete_surname(message: Message, state: FSMContext):
    """Обработка фамилии для удаления"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить удаление",
        callback_data="cancel_operation__cd"))
    
    await state.update_data(surname=message.text.strip())
    await message.answer(
        "🔤 Введите отчество студента:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(DeleteStudent.patronymic)

@dp.message(DeleteStudent.patronymic)
async def process_delete_patronymic(message: Message, state: FSMContext):
    """Завершение ввода ФИО для удаления"""
    data = await state.get_data()
    
    # Здесь будет логика удаления студента по ФИО
    # Пока просто выводим собранные данные
    student_info = (
        f"📋 Информация о студенте:\n\n"
        f"👤 Имя: {data.get('name')}\n"
        f"📛 Фамилия: {data.get('surname')}\n"
        f"🔤 Отчество: {message.text.strip()}"
    )

    result = await Func.delete_student(name=data.get('name'), surname=data.get('surname'), patronymic=message.text.strip())
    
    if result["status"]:
        await message.answer(f"{student_info}\n\n✅ Студент успешно удален из системы!")
    else:
        await message.answer(f"{student_info}\n\n❌ Ошибка при удалении студента:\n{result['info']}")
    
    await cmd_menu(message)

    await state.clear()

@dp.callback_query(F.data == "get_code__cd")
async def start_getting_code(callback: CallbackQuery, state: FSMContext):
    """Начало процесса получения кода студента"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить удаление",
        callback_data="cancel_operation__cd"))
    
    await callback.message.answer(
        "🤖 Начинаем процесс получения кода доступка студента\n\n"
        "👤 Введите имя студента:", reply_markup=builder.as_markup())
    await state.set_state(GetCode.name)
    await callback.answer()

@dp.message(GetCode.name)
async def process_student_name_for_code(message: Message, state: FSMContext):
    """Обработка имени для получения кода"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить удаление",
        callback_data="cancel_operation__cd"))
    
    await state.update_data(name=message.text.strip())
    await message.answer("📛 Введите фамилию студента:", reply_markup=builder.as_markup())
    await state.set_state(GetCode.surname)

@dp.message(GetCode.surname)
async def process_student_surname_for_code(message: Message, state: FSMContext):
    """Обработка фамилии для получения кода"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить удаление",
        callback_data="cancel_operation__cd"))
    
    await state.update_data(surname=message.text.strip())
    await message.answer("🔤 Введите отчество студента:", reply_markup=builder.as_markup())
    await state.set_state(GetCode.patronymic)

@dp.message(GetCode.patronymic)
async def process_student_patronymic_for_code(message: Message, state: FSMContext):
    """Завершение получения кода студента"""
    data = await state.get_data()
    result = await Func.get_student_code(
        name=data.get('name'),
        surname=data.get('surname'),
        patronymic=message.text.strip()
    )
    
    response = (
        f"{'✅ Студент найден' if result['status'] else '❌ Студент не найден'}"
        f"{f'\n🔑 Код: {result["code"]}' if result['status'] else f''}\n"
    )
    
    await message.answer(response)

    await cmd_menu(message)
    
    await state.clear()

@dp.callback_query(F.data == "exit_teacher__cd")
async def exit_teacher(callback: CallbackQuery):
    """Выход учителя из аккаунта"""
    result = await Func.del_teachers_tg_id(teacher_tg_id=callback.from_user.id)

    if result["status"]:
        await callback.message.answer("✅ Вы успешно вышли из аккаунта")
        await cmd_start(callback.message)
    else:
        await callback.answer(f"❌ {result['info']}")

    await callback.answer()

# =================================================================================
# ОБРАБОТЧИКИ ДЛЯ СТУДЕНТОВ
# =================================================================================

@dp.callback_query(F.data == "role_student__cd")
async def reg_student(callback: CallbackQuery, state: FSMContext):
    """Начало регистрации студента"""
    await state.set_state(WaitCode.reg_student)
    await callback.message.answer(
        "🔑 Для регистрации введи твой уникальный код доступа:\n\n"
        "❗ Если у тебя его нет - обратись к своему учителю"
    )
    await callback.answer()

@dp.message(WaitCode.reg_student)
async def reg_student_2(message: Message, state: FSMContext):
    """Завершение регистрации студента"""
    result = await Func.reg_student_tg(
        student_tg_id=message.from_user.id,
        code=message.text.strip()
    )

    if result["status"]:
        await message.answer("✅ Регистрация успешно пройдена!")
        await cmd_start(message)
    else:
        await message.answer(f"❌ Произошла ошибка: {result['info']}")

    await state.clear()

@dp.callback_query(F.data == "post_que__cd")
async def post_que(callback: CallbackQuery):
    """Обработчик отправки опроса (временно недоступен)"""
    await callback.answer("❌ Программа опросов пока что недоступна")

@dp.callback_query(F.data == "post_idea__cd")
async def post_idea(callback: CallbackQuery):
    """Обработчик предложения идей (временно недоступен)"""
    await callback.answer("❌ Программа предложений пока что недоступна")

@dp.callback_query(F.data == "exit_student__cd")
async def exit_student(callback: CallbackQuery):
    """Выход студента из аккаунта"""
    result = await Func.del_students_tg_id(student_tg_id=callback.from_user.id)

    if result["status"]:
        await callback.message.answer("✅ Вы успешно вышли из аккаунта")
        await cmd_start(callback.message)
    else:
        await callback.answer(f"❌ {result['info']}")

    await callback.answer()

# =================================================================================
# ОБРАБОТЧИКИ ДЛЯ ГОСТЕЙ
# =================================================================================

@dp.callback_query(F.data == "role_guest__cd")
async def guest(callback: CallbackQuery):
    """Обработчик для гостей"""

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🌐 Lobby",
        web_app=WebAppInfo(url=settings.get_url())))
    builder.add(InlineKeyboardButton(
        text="📊 Отправить опрос",
        callback_data="post_que__cd"))
    builder.add(InlineKeyboardButton(
        text="💡 Предложить идею",
        callback_data="post_idea__cd"))
    builder.add(InlineKeyboardButton(
        text="📝 Управление БД",
        callback_data="edit_db_guest__cd"))
    
    builder.adjust(2,2)
    
    welcome_message = (
            "👋 Здравствуйте!\n\n"
            "🤖 Этот бот - универсальный инструмент любого кванторианца, а так же пульт управления базой данных для учителей\n\n"
            "🔹 Я могу:\n"
            "• 🌐 Открыть 'Lobby' - интерактивную платформу ученика\n"
            "• 📊 Отправить опрос для проекта в концретные группы\n"
            "• 💡 Принять идеи по улучшению проекта\n"
            "• ✏️ Добавить, удалить, изменить или показать информацию о студенте\n"
            "• 📰 Делать рассылки конкретным группам (уведомления о мероприятиях, работе кванториума и образовательном процессе)\n"
    )
    
    await callback.message.answer(
        welcome_message, reply_markup=builder.as_markup()
    )
    await callback.answer()

@dp.callback_query(F.data == "edit_db_guest__cd")
async def edit_db_guest(callback: CallbackQuery):
    await callback.answer("❌ Гости не могут редактировать базу данных")
    

# =================================================================================
# ДОПОЛНИТЕЛЬНЫЕ ОБРАБОТЧИКИ
# =================================================================================

@dp.message()
async def handle_other_messages(message: Message):
    """Удаление всех необработанных сообщений"""
    await message.delete()

# =================================================================================
# ЗАПУСК БОТА
# =================================================================================

async def main():
    """Основная функция запуска бота"""
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())