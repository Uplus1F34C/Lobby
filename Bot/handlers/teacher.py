from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Bot.keyboards import *
from Bot.states import *
from Bot.handlers.common import cmd_start
from DataBase.Services.auth_service import reg_teacher, logout_teacher
from DataBase.Services.student_service import add_student, get_student_code, del_student
from DataBase.Settings.models import level, kvant

teacher_router = Router()

# ==== РЕГИСТРАЦИЯ УЧИТЕЛЯ ====
@teacher_router.callback_query(F.data == "role_teacher")
async def start_teacher_registration(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WaitCode.reg_teacher)
    await callback.message.answer(
        "🔑 Для регистрации введите ваш уникальный код доступа:",
        reply_markup=cancel_kb()
    )
    await callback.answer()

@teacher_router.message(WaitCode.reg_teacher)
async def finish_teacher_registration(message: Message, state: FSMContext):
    result = await reg_teacher(tg_id=message.from_user.id, code=message.text.strip())
    
    if result["status"]:
        await message.answer("✅ Регистрация успешно завершена!")
        await cmd_start(message)
    else:
        await message.answer(f"❌ Ошибка: {result['info']}")
    
    await state.clear()

# ==== ДОБАВЛЕНИЕ СТУДЕНТА ====
@teacher_router.callback_query(F.data == "add_student")
async def start_adding_student(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddStudent.name)
    await callback.message.answer(
        "🤖 Начинаем процесс добавления нового студента\n\n"
        "👤 Введите имя студента:",
        reply_markup=cancel_kb()
    )
    await callback.answer()

@teacher_router.message(AddStudent.name)
async def process_student_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer(
        "📛 Введите фамилию студента:",
        reply_markup=cancel_kb()
    )
    await state.set_state(AddStudent.surname)

@teacher_router.message(AddStudent.surname)
async def process_student_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.strip())
    await message.answer(
        "🔤 Введите отчество студента:",
        reply_markup=cancel_kb()
    )
    await state.set_state(AddStudent.patronymic)

@teacher_router.message(AddStudent.patronymic)
async def process_student_patronymic(message: Message, state: FSMContext):
    await state.update_data(patronymic=message.text.strip())
    await message.answer(
        f"📚 Введите направление (квант) студента:\n\nДоступные варианты: {', '.join([l.value for l in kvant])}",
        reply_markup=cancel_kb()
    )
    await state.set_state(AddStudent.kvant)

@teacher_router.message(AddStudent.kvant)
async def process_student_kvant(message: Message, state: FSMContext):
    await state.update_data(kvant=message.text.strip())
    await message.answer(
        f"📊 Введите уровень студента:\n\nДоступные варианты: {', '.join([l.value for l in level])}",
        reply_markup=cancel_kb()
    )
    await state.set_state(AddStudent.level)

@teacher_router.message(AddStudent.level)
async def process_student_level(message: Message, state: FSMContext):
    await state.update_data(level=message.text.strip())
    await message.answer(
        "🔢 Введите номер группы студента:",
        reply_markup=cancel_kb()
    )
    await state.set_state(AddStudent.num)

@teacher_router.message(AddStudent.num)
async def process_student_num(message: Message, state: FSMContext):
    data = await state.get_data()
    
    result = await add_student(
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

    await cmd_start(message)
    await state.clear()

# ==== УДАЛЕНИЕ СТУДЕНТА ====
@teacher_router.callback_query(F.data == "delete_student")
async def delete_student_by_fio(callback: CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🔢 По ID",
        callback_data="delete_student_by_id"))
    builder.add(InlineKeyboardButton(
        text="👤 По ФИО",
        callback_data="delete_student_by_fio"))
    builder.add(InlineKeyboardButton(
        text="❌ Отменить",
        callback_data="cancel_operation"))
    builder.adjust(2, 1)
    
    await callback.message.answer(
        "🤖 Выберите способ удаления студента:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@teacher_router.callback_query(F.data == "delete_student_by_id")
async def delete_student_by_id_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteStudent.id)
    await callback.message.answer(
        "🔢 Введите ID студента для удаления:",
        reply_markup=cancel_kb()
    )
    await callback.answer()

@teacher_router.message(DeleteStudent.id)
async def process_delete_id(message: Message, state: FSMContext):
    student_id = message.text.strip()
    
    try:
        student_id = int(student_id)  # Проверяем, что ID - число
        result = await del_student(tg_id=student_id)
        
        if result["status"]:
            await message.answer(f"✅ Студент с ID {student_id} успешно удален из системы!")
        else:
            await message.answer(f"❌ Ошибка при удалении студента:\n{result['info']}")
    except ValueError:
        await message.answer("❌ ID должен быть числом. Пожалуйста, введите корректный ID.")
        return
    
    await cmd_start(message)
    await state.clear()


@teacher_router.callback_query(F.data == "delete_student_by_fio")
async def delete_student_by_fio(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteStudent.name)
    await callback.message.answer(
        "🤖 Начинаем процесс удаления студента\n\n"
        "👤 Введите имя студента:",
        reply_markup=cancel_kb()
    )
    await callback.answer()

@teacher_router.message(DeleteStudent.name)
async def process_delete_name(message: Message, state: FSMContext):    
    await state.update_data(name=message.text.strip())
    await message.answer(
        "📛 Введите фамилию студента:",
        reply_markup=cancel_kb()
    )
    await state.set_state(DeleteStudent.surname)

@teacher_router.message(DeleteStudent.surname)
async def process_delete_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.strip())
    await message.answer(
        "🔤 Введите отчество студента:",
        reply_markup=cancel_kb()
    )
    await state.set_state(DeleteStudent.patronymic)

@teacher_router.message(DeleteStudent.patronymic)
async def process_delete_patronymic(message: Message, state: FSMContext):
    data = await state.get_data()
    
    student_info = (
        f"📋 Информация о студенте:\n\n"
        f"👤 Имя: {data.get('name')}\n"
        f"📛 Фамилия: {data.get('surname')}\n"
        f"🔤 Отчество: {message.text.strip()}"
    )

    result = await del_student(name=data.get('name'), surname=data.get('surname'), patronymic=message.text.strip())
    
    if result["status"]:
        await message.answer(f"{student_info}\n\n✅ Студент успешно удален из системы!")
    else:
        await message.answer(f"{student_info}\n\n❌ Ошибка при удалении студента:\n{result['info']}")
    
    await cmd_start(message)

    await state.clear()

@teacher_router.callback_query(F.data == "get_code")
async def start_getting_code(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🤖 Начинаем процесс получения кода доступка студента\n\n"
        "👤 Введите имя студента:", reply_markup=cancel_kb())
    await state.set_state(GetCode.name)
    await callback.answer()

@teacher_router.message(GetCode.name)
async def process_student_name_for_code(message: Message, state: FSMContext):    
    await state.update_data(name=message.text.strip())
    await message.answer("📛 Введите фамилию студента:", reply_markup=cancel_kb())
    await state.set_state(GetCode.surname)

@teacher_router.message(GetCode.surname)
async def process_student_surname_for_code(message: Message, state: FSMContext):    
    await state.update_data(surname=message.text.strip())
    await message.answer("🔤 Введите отчество студента:", reply_markup=cancel_kb())
    await state.set_state(GetCode.patronymic)

@teacher_router.message(GetCode.patronymic)
async def process_student_patronymic_for_code(message: Message, state: FSMContext):
    data = await state.get_data()
    result = await get_student_code(
        name=data.get('name'),
        surname=data.get('surname'),
        patronymic=message.text.strip()
    )
    
    response = (
        f"{'✅ Студент найден' if result['status'] else '❌ Студент не найден'}"
        f"{f'\n🔑 Код: {result["code"]}' if result['status'] else f''}\n"
    )
    
    await message.answer(response)
    await cmd_start(message)
    await state.clear()

# ==== ВЫХОД ИЗ АККАУНТА УЧИТЕЛЯ ====
@teacher_router.callback_query(F.data == "exit_teacher")
async def exit_teacher(callback: CallbackQuery):
    result = await logout_teacher(tg_id=callback.from_user.id)

    if result["status"]:
        await callback.message.answer("✅ Вы успешно вышли из аккаунта")
        await cmd_start(callback.message)
    else:
        await callback.answer(f"❌ {result['info']}")

    await callback.answer()