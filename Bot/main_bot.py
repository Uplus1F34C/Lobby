# ======================== ВЫБОР ДЕРИКТОРИИ ========================

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ======================== ИМПОРТЫ БИБЛИОТЕК ========================

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# ======================== ИМПОРТЫ ПРОЕКТА ========================

from Bot.config import settings
from DataBase import Func
from DataBase.settings.models import level, kvant

# ======================== НАСТРЙКА БОТА ========================

bot = Bot(token=settings.get_token)
dp = Dispatcher()

# ======================== КЛАССЫ СОСТОЯНИЙ FSM ========================

class WaitCode(StatesGroup):
    reg_teacher = State()
    reg_student = State()
    del_student = State()

class AddStudent(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()
    kvant = State()
    level = State()
    num = State()

class GetCode(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()

class DeleteStudent(StatesGroup):
    id = State()
    name = State()
    surname = State()
    patronymic = State()

# ======================== КОМАНДЫ ========================

@dp.message(Command("start"))
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()

     # Проверка на учителя
    teacher_info = await Func.log_teacher(message.from_user.id)
    student_info = await Func.log_student(message.from_user.id)
    if teacher_info["status"]:
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
            "🌐 Чтобы открыть Lobby - нажмите на кнопку слево от поля ввода\n\n"
            "🔹 Для дополнительных функций нажмите на кнопку ниже:"
        )

    # Проверка на студента
    elif student_info["status"]:
        builder.add(InlineKeyboardButton(
            text="📊 Отправить опрос",
            callback_data="post_que__cd"))
        builder.add(InlineKeyboardButton(
            text="💡 Предложить идею",
            callback_data="post_idea__cd"))
        builder.add(InlineKeyboardButton(
            text="📅 Узнать расписание",
            callback_data="schedule__cd"))
        builder.add(InlineKeyboardButton(
            text="🚪 Выйти из аккаунта",
            callback_data="exit_student__cd"))
        builder.adjust(1, 1, 1, 1)

        welcome_message = (
            f"👋 Привет, {student_info['name']}!\n\n"
            "🌐 Чтобы открыть Lobby - нажми на кнопку слево от поля ввода\n"
            "🔹 Для дополнительных функций нажми на кнопку ниже:"
            )
    
    # Меню для неавторизованных пользователей
    else:
        builder.add(InlineKeyboardButton(
            text="👨‍🏫 Я учитель",
            callback_data="role_teacher__cd"))
        builder.add(InlineKeyboardButton(
            text="👨‍🎓 Я ученик",
            callback_data="role_student__cd"))
        builder.adjust(2)

        welcome_message = (
            "👋 Приветствую!\n\n"
            "🤖 Этот бот - универсальный инструмент любого кванторианца\n\n"
            "🔹 Он может:\n"
            """• 🌐 Открыть "Lobby" - интерактивную платформу ученика\n"""
            "• 📊 Отправить опрос в конкретные группы\n"
            "• 📰 Делать рассылки (уведомления о мероприятиях, работе кванториума и образовательном процессе)\n"
            "• 📅 Отобразить расписание занятий и мероприятий\n\n"
            """• 💡 А так же принять идеи по улучшению проекта "Lobby" или записать ошибку\n\n"""
            "🟢 Для начала работы выберите свою роль:"
        )

    try:
        await message.message.answer(welcome_message, reply_markup=builder.as_markup())
    except:
        await message.answer(welcome_message, reply_markup=builder.as_markup())



@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    builder = InlineKeyboardBuilder()

    # Проверка на учителя
    teacher_auth = await Func.log_teacher(message.from_user.id)
    student_auth = await Func.log_student(message.from_user.id)
    if teacher_auth["status"]:
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

    # Проверка на студента
    elif student_auth["status"]:
        builder.add(InlineKeyboardButton(
            text="📊 Отправить опрос",
            callback_data="post_que__cd"))
        builder.add(InlineKeyboardButton(
            text="💡 Предложить идею",
            callback_data="post_idea__cd"))
        builder.add(InlineKeyboardButton(
            text="📅 Узнать расписание",
            callback_data="schedule__cd"))
        builder.add(InlineKeyboardButton(
            text="🚪 Выйти из аккаунта",
            callback_data="exit_student__cd"))
        builder.adjust(1, 1, 1, 1)
    # Меню для неавторизованных пользователей
    else:
        await cmd_start(message)
        return
    
    welcome_message = (
        "🌐 Чтобы открыть Lobby - нажми на кнопку слево от поля ввода\n"
        "🔹 Для дополнительных функций нажми на кнопку ниже:")
    try:
        await message.message.answer(welcome_message, reply_markup=builder.as_markup())
    except:
        await message.answer(welcome_message, reply_markup=builder.as_markup())

# ======================== ФУНКЦИИ УЧИТЕЛЕЙ ========================

# ==== РЕГИСТРАЦИЯ УЧИТЕЛЯ ====
@dp.callback_query(F.data == "role_teacher__cd")
async def reg_teacher(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WaitCode.reg_teacher)
    await callback.message.answer(
        "🔑 Для регистрации введите ваш уникальный код доступа:\n\n"
        "❗ Если у вас нет кода, обратитесь к администратору системы"
    )
    await callback.answer()

@dp.message(WaitCode.reg_teacher)
async def reg_teacher_2(message: Message, state: FSMContext):
    registration_code = message.text.strip()
    result = await Func.reg_teacher(message.from_user.id, registration_code)

    if result["status"]:
        await message.answer("✅ Регистрация успешно завершена!")
        print(f"{message.from_user.username} - Зарегестрировался как учитель")
        await cmd_start(message)
    else:
        await message.answer(f"❌ Ошибка регистрации: {result['info']}\n\nПопробуйте еще раз или обратитесь к администратору.")

    await state.clear()

# ==== ОТМЕНА ОПЕРАЦИИ ====
@dp.callback_query(F.data == "cancel_operation__cd")
async def cancel_operation(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Операция отменена")
    await cmd_menu(callback)
    await callback.answer()

cancel_button = InlineKeyboardBuilder()
cancel_button.add(InlineKeyboardButton(
    text="❌ Отменить добавление",
    callback_data="cancel_operation__cd"))

# ==== ДОБАВЛЕНИЕ СТУДЕНТА ====
@dp.callback_query(F.data == "add_student__cd")
async def start_adding_student(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddStudent.name)
    await callback.message.answer(
        "🤖 Начинаем процесс добавления нового студента\n\n"
        "👤 Введите имя студента:",
        reply_markup=cancel_button.as_markup()
    )
    await callback.answer()

@dp.message(AddStudent.name)
async def process_student_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer(
        "📛 Введите фамилию студента:",
        reply_markup=cancel_button.as_markup()
    )
    await state.set_state(AddStudent.surname)

@dp.message(AddStudent.surname)
async def process_student_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.strip())
    await message.answer(
        "🔤 Введите отчество студента:",
        reply_markup=cancel_button.as_markup()
    )
    await state.set_state(AddStudent.patronymic)

@dp.message(AddStudent.patronymic)
async def process_student_patronymic(message: Message, state: FSMContext):
    await state.update_data(patronymic=message.text.strip())
    await message.answer(
        f"📚 Введите направление (квант) студента:\n\nДоступные варианты: {', '.join([l.value for l in kvant])}",
        reply_markup=cancel_button.as_markup()
    )
    await state.set_state(AddStudent.kvant)

@dp.message(AddStudent.kvant)
async def process_student_kvant(message: Message, state: FSMContext):
    await state.update_data(kvant=message.text.strip())
    await message.answer(
        f"📊 Введите уровень студента:\n\nДоступные варианты: {', '.join([l.value for l in level])}",
        reply_markup=cancel_button.as_markup()
    )
    await state.set_state(AddStudent.level)

@dp.message(AddStudent.level)
async def process_student_level(message: Message, state: FSMContext):
    await state.update_data(level=message.text.strip())
    await message.answer(
        "🔢 Введите номер группы студента:",
        reply_markup=cancel_button.as_markup()
    )
    await state.set_state(AddStudent.num)

@dp.message(AddStudent.num)
async def process_student_num(message: Message, state: FSMContext):
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
        
    )
    
    if result['status']:
        await message.answer(
            f"{student_info}"
            f"🗝️ Код: {result["code"]}\n\n"
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

# ==== УДАЛЕНИЕ СТУДЕНТА ====
@dp.callback_query(F.data == "delete_student__cd")
async def delete_student_by_fio(callback: CallbackQuery, state: FSMContext):
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
    await state.set_state(DeleteStudent.id)
    await callback.message.answer(
        "🔢 Введите ID студента для удаления:",
        reply_markup=cancel_button.as_markup()
    )
    await callback.answer()

@dp.message(DeleteStudent.id)
async def process_delete_id(message: Message, state: FSMContext):
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
    await state.set_state(DeleteStudent.name)
    await callback.message.answer(
        "🤖 Начинаем процесс удаления студента\n\n"
        "👤 Введите имя студента:",
        reply_markup=cancel_button.as_markup()
    )
    await callback.answer()

@dp.message(DeleteStudent.name)
async def process_delete_name(message: Message, state: FSMContext):    
    await state.update_data(name=message.text.strip())
    await message.answer(
        "📛 Введите фамилию студента:",
        reply_markup=cancel_button.as_markup()
    )
    await state.set_state(DeleteStudent.surname)

@dp.message(DeleteStudent.surname)
async def process_delete_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.strip())
    await message.answer(
        "🔤 Введите отчество студента:",
        reply_markup=cancel_button.as_markup()
    )
    await state.set_state(DeleteStudent.patronymic)

@dp.message(DeleteStudent.patronymic)
async def process_delete_patronymic(message: Message, state: FSMContext):
    data = await state.get_data()
    
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

# ==== ПОЛУЧЕНИЕ КОДА СТУДЕНТА ====
@dp.callback_query(F.data == "get_code__cd")
async def start_getting_code(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🤖 Начинаем процесс получения кода доступка студента\n\n"
        "👤 Введите имя студента:", reply_markup=cancel_button.as_markup())
    await state.set_state(GetCode.name)
    await callback.answer()

@dp.message(GetCode.name)
async def process_student_name_for_code(message: Message, state: FSMContext):    
    await state.update_data(name=message.text.strip())
    await message.answer("📛 Введите фамилию студента:", reply_markup=cancel_button.as_markup())
    await state.set_state(GetCode.surname)

@dp.message(GetCode.surname)
async def process_student_surname_for_code(message: Message, state: FSMContext):    
    await state.update_data(surname=message.text.strip())
    await message.answer("🔤 Введите отчество студента:", reply_markup=cancel_button.as_markup())
    await state.set_state(GetCode.patronymic)

@dp.message(GetCode.patronymic)
async def process_student_patronymic_for_code(message: Message, state: FSMContext):
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

# ==== ВЫХОД ИЗ АККАУНТА УЧИТЕЛЯ ====
@dp.callback_query(F.data == "exit_teacher__cd")
async def exit_teacher(callback: CallbackQuery):
    result = await Func.del_teachers_id(teacher_tg_id=callback.from_user.id)

    if result["status"]:
        await callback.message.answer("✅ Вы успешно вышли из аккаунта")
        await cmd_start(callback.message)
    else:
        await callback.answer(f"❌ {result['info']}")

    await callback.answer()

# ======================== ФУНКЦИИ СТУДЕНТОВ ========================

# ==== РЕГИСТРАЦИЯ СТУДЕНТА ====
@dp.callback_query(F.data == "role_student__cd")
async def reg_student(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WaitCode.reg_student)
    await callback.message.answer(
        "🔑 Для регистрации введи твой уникальный код доступа:\n\n"
        "❗ Если у тебя его нет - обратись к своему учителю"
    )
    await callback.answer()

@dp.message(WaitCode.reg_student)
async def reg_student_2(message: Message, state: FSMContext):
    result = await Func.reg_student(
        student_tg_id=message.from_user.id,
        code=message.text.strip()
    )

    if result["status"]:
        print(f"{message.from_user.username} - Зарегестрировался как ученик")
        await message.answer("✅ Регистрация успешно пройдена!")
        await cmd_start(message)
    else:
        await message.answer(f"❌ Произошла ошибка: {result['info']}")

    await state.clear()

# ==== ОТПРАВКА ОПРОСА ====
@dp.callback_query(F.data == "post_que__cd")
async def post_que(callback: CallbackQuery):
    """Обработчик отправки опроса (временно недоступен)"""
    await callback.answer("❌ Программа опросов пока что недоступна")

# ==== ПРЕДЛОЖЕНИЕ ИДЕЙ ====
@dp.callback_query(F.data == "post_idea__cd")
async def post_idea(callback: CallbackQuery):
    """Обработчик предложения идей (временно недоступен)"""
    await callback.answer("❌ Программа предложений пока что недоступна")

    
# ==== ПРОСМОТР РАСПИСАНИЯ ====
@dp.callback_query(F.data == "schedule__cd")
async def post_idea(callback: CallbackQuery):
    await callback.answer("❌ Программа расписаний пока что недоступна")

# ==== ВЫХОД ИЗ АККАУНТА СТУДЕНТА ====
@dp.callback_query(F.data == "exit_student__cd")
async def exit_student(callback: CallbackQuery):
    """Выход студента из аккаунта"""
    result = await Func.del_students_id(student_tg_id=callback.from_user.id)

    if result["status"]:
        await callback.message.answer("✅ Вы успешно вышли из аккаунта")
        await cmd_start(callback.message)
    else:
        await callback.answer(f"❌ {result['info']}")

    await callback.answer()

# ======================== ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ========================

@dp.message()
async def handle_other_messages(message: Message):
    """Удаление всех необработанных сообщений"""
    print("Сообщение удалено")
    await message.delete()

# ======================== ЗАПУСК БОТА ========================

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())