from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# Импорты aiogram ---------------------------------------------------------------------------------


# Импорты проекта ---------------------------------------------------------------------------------
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TGbot.config import settings
from DataBase import Func
from DataBase.settings.models import level, kvant
# Импорты проекта ---------------------------------------------------------------------------------


# Инициализация бота и диспетчера -----------------------------------------------------------------
bot = Bot(token=settings.get_token)
dp = Dispatcher()
# Инициализация бота и диспетчера -----------------------------------------------------------------


# Определение состояний для FSM -------------------------------------------------------------------
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
# Определение состояний для FSM -------------------------------------------------------------------

# Команда /start ----------------------------------------------------------------------------------
@dp.message(Command("start"))
async def cmd_start(message: Message):
    if Func.log_teacher(message.from_user.id)["status"]:
        Teacher = Func.get_FIO_teacher(message.from_user.id)

        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="Добавить студента",
            callback_data="add_student__cd"))
        builder.add(InlineKeyboardButton(
            text="Удалить студента",
            callback_data="delete_student__cd"))
        builder.add(InlineKeyboardButton(
            text="Получить код ученика",
            callback_data="get_code__cd"))
        builder.add(InlineKeyboardButton(
            text="Выйти из аккаунта",
            callback_data="exit_teacher"))
        builder.adjust(2, 1, 1)

        welcome_message = f"""Здравствуйте, {Teacher["name"]} {Teacher["patronymic"]}!
С помощью этого бота вы можете редактировать базу данных проекта "Lobby"
Выберете что хотите сделать:"""

        await message.answer(
            welcome_message, 
            reply_markup=builder.as_markup()
        )

    elif Func.log_student_tg(message.from_user.id)["status"]:
        Student = Func.get_FIO_student_tg(message.from_user.id)

        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="Lobby",
            web_app=WebAppInfo(url=f"https://uplus1f34c.github.io/Lobby/FrontEnd/Pages?student_id={message.from_user.id}")))
        builder.add(InlineKeyboardButton(
            text="Отправить опрос",
            callback_data="post_que__cd"))
        builder.add(InlineKeyboardButton(
            text="Предложить идею",
            callback_data="post_idea__cd"))
        builder.add(InlineKeyboardButton(
            text="Выйти из аккаунта",
            callback_data="exit_student__cd"))
        builder.adjust(1, 2, 1)

        welcome_message = f"""Привет, {Student["name"]}!
Этот бот - универсальный инструмент для любого кванторианца!
Он может:
● Открыть "Lobby" - сайт, геймифицирующий кванториум
● Отправить опрос для твоего проекта другим ученикам
● Выслушать и передать твои идеи по улучшению этого бота и "Lobby" """

        await message.answer(
            welcome_message,
            reply_markup=builder.as_markup()
        )

    else:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="Учитель",
            callback_data="role_teacher__cd"))
        builder.add(InlineKeyboardButton(
            text="Ученик",
            callback_data="role_student__cd"))
        builder.add(InlineKeyboardButton(
            text="Гость",
            callback_data="role_guest__cd"))

        welcome_message = "Выберете вашу роль:"

        await message.answer(
            welcome_message,
            reply_markup=builder.as_markup()
        )
# Команда /start ----------------------------------------------------------------------------------
        

# Регистрация учителя -----------------------------------------------------------------------------
@dp.callback_query(F.data == "role_teacher__cd")
async def reg_teacher(callback: CallbackQuery, state: FSMContext):
    message = "Введите код регистрации:"
    
    await state.set_state(WaitCode.reg_teacher)
    await callback.message.answer(message)
    await callback.answer()

@dp.message(WaitCode.reg_teacher)
async def reg_teacher_2(message: Message, state: FSMContext):
    registration_code = message.text.strip()

    result = Func.reg_teacher(message.from_user.id, registration_code)

    if result["status"]:
        await message.answer("✅ Регистрация успешно пройдена!")
        await cmd_start(message)
    else:
        await message.answer(f"❌ {result["info"]}")

    await state.clear()
# Регистрация учителя -----------------------------------------------------------------------------


# Добавление ученкиа -----------------------------------------------------------------------------
@dp.callback_query(F.data == "add_student__cd")
async def start_adding_student(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите имя студента:")
    await state.set_state(AddStudent.name)
    await callback.answer()

@dp.message(AddStudent.name)
async def process_student_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Введите фамилию студента:")
    await state.set_state(AddStudent.surname)

@dp.message(AddStudent.surname)
async def process_student_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.strip())
    await message.answer("Введите отчество студента:")
    await state.set_state(AddStudent.patronymic)

@dp.message(AddStudent.patronymic)
async def process_student_patronymic(message: Message, state: FSMContext):
    await state.update_data(patronymic=message.text.strip())
    await message.answer(f"Введите квант студента({', '.join([l.value for l in kvant])}):")
    await state.set_state(AddStudent.kvant)

@dp.message(AddStudent.kvant)
async def process_student_kvant(message: Message, state: FSMContext):
    await state.update_data(kvant=message.text.strip())
    await message.answer(f"Введите уровень студента({', '.join([l.value for l in level])}):")
    await state.set_state(AddStudent.level)

@dp.message(AddStudent.level)
async def process_student_level(message: Message, state: FSMContext):
    await state.update_data(level=message.text.strip())
    await message.answer(f"Введите номер группы студента:")
    await state.set_state(AddStudent.num)

@dp.message(AddStudent.num)
async def process_student_num(message: Message, state: FSMContext):
    
    # Получаем все сохраненные данные
    data = await state.get_data()

    name = data.get('name')
    surname = data.get('surname')
    patronymic = data.get('patronymic')
    level = data.get('level')
    kvant = data.get('kvant')
    group_num = message.text.strip()

    result = Func.insert_student(name, surname, patronymic, level, kvant, group_num)
    
    # Для примера просто выведем полученные данные
    student_info = f"Имя: {name}\nФамилия: {surname}\nОтчество: {patronymic}\nГруппа: {level}-{kvant}-{group_num}"
    await message.answer(f"{student_info}\n\nСтатус: {result['status']}\nИнформация: {result['info']}")
    
    await state.clear()
# Добавление ученкиа -----------------------------------------------------------------------------

# Удалить ученкиа -----------------------------------------------------------------------------
@dp.callback_query(F.data == "delete_student__cd")
async def delete_student(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите id студента:")
    await state.set_state(WaitCode.del_student)
    await callback.answer()

@dp.message(WaitCode.del_student)
async def delete_student_2(message: Message, state: FSMContext):
    id = message.text.strip()
    result = Func.delete_student(student_id=id)
    await message.answer(f"Статус: {result['status']}\nИнформация: {result['info']}")
    await state.clear()
# Удалить ученикиа -----------------------------------------------------------------------------

# Получить код ученика -----------------------------------------------------------------------------
@dp.callback_query(F.data == "get_code__cd")
async def start_adding_student(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите имя студента:")
    await state.set_state(GetCode.name)
    await callback.answer()

@dp.message(GetCode.name)
async def process_student_surname(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Введите фамилию студента:")
    await state.set_state(GetCode.surname)

@dp.message(GetCode.surname)
async def process_student_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.strip())
    await message.answer("Введите отчество студента:")
    await state.set_state(GetCode.patronymic)


@dp.message(GetCode.patronymic)
async def process_student_name(message: Message, state: FSMContext):
    data = await state.get_data()

    name = data.get('name')
    surname = data.get('surname')
    patronymic = message.text.strip()

    result = Func.get_code_student(name, surname, patronymic)
    await message.answer(f"Статус: {result['status']}\nИнформация: {result['info']}\nКод: {result['code']}")
    await state.clear()
# Получить код ученкиа -----------------------------------------------------------------------------

# Выйти из аккаунта ---------------------------------------------------------------
@dp.callback_query(F.data == "exit_teacher")
async def exit_teacher(callback: CallbackQuery):
    result = Func.del_tg_id_teacher(teacher_tg_id=callback.from_user.id)

    if result["status"]:
        await callback.message.answer("✅ Вы успешно вышли из аккаунта")
        await cmd_start(callback.message)
    else:
        await callback.answer(f"❌ {result["info"]}")

    await callback.answer()
# Выйти из аккаунта ---------------------------------------------------------------






# Регистрация ученика ---------------------------------------------------------------
@dp.callback_query(F.data == "role_student__cd")
async def reg_student(callback: CallbackQuery, state: FSMContext):
    message = "Введите код регистрации:"
    
    await state.set_state(WaitCode.reg_student)
    await callback.message.answer(message)
    await callback.answer()

@dp.message(WaitCode.reg_student)
async def reg_student_2(message: Message, state: FSMContext):
    registration_code = message.text.strip()

    result = Func.reg_student_tg(student_tg_id=message.from_user.id, code=registration_code)

    if result["status"]:
        await message.answer("✅ Регистрация успешно пройдена!")
        await cmd_start(message)
    else:
        await message.answer(f"❌ Произошла ошибка: {result["info"]}")

    await state.clear()
# Регистрация ученика ---------------------------------------------------------------

# Отправить опрос ---------------------------------------------------------------
@dp.callback_query(F.data == "post_que__cd")
async def post_que(callback: CallbackQuery):
    await callback.message.answer(f"Программа опросов, к сожалению, пока недоступна")
    await callback.answer()
# Отправить опрос ---------------------------------------------------------------

# Отправить идею ---------------------------------------------------------------
@dp.callback_query(F.data == "post_idea__cd")
async def post_ide(callback: CallbackQuery):
    await callback.message.answer(f"Программа предложений, к сожалению, пока недоступна")
    await callback.answer()
# Отправить идею ---------------------------------------------------------------

# Выйти из аккаунта ---------------------------------------------------------------
@dp.callback_query(F.data == "exit_student__cd")
async def exit_student(callback: CallbackQuery):
    
    result = Func.del_tg_id_student(student_tg_id=callback.from_user.id)

    if result["status"]:
        await callback.message.answer("✅ Вы успешно вышли из аккаунта")
        await cmd_start(callback.message)
    else:
        await callback.answer(f"❌ {result["info"]}")

    await callback.answer()
# Выйти из аккаунта ---------------------------------------------------------------






# Гость ---------------------------------------------------------------
@dp.callback_query(F.data == "role_guest__cd")
async def reg_guest(callback: CallbackQuery):
    await callback.message.answer(f"Программа гостей, к сожалению, пока недоступна")
    await callback.answer()
# Гость ---------------------------------------------------------------


# Удаляем все остальные сообщения ---------------------------------------------------------------
@dp.message()
async def handle_other_messages(message: Message):
    await message.delete()  
# Удаляем все остальные сообщения ---------------------------------------------------------------


# Запуск бота ---------------------------------------------------------------
async def main():
    print("Бот готов к запуску.\nЗапуск...")
    await dp.start_polling(bot)

import asyncio
asyncio.run(main())
# Запуск бота ---------------------------------------------------------------