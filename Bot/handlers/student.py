from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Bot.keyboards import *
from Bot.states import *
from Bot.handlers.common import cmd_start
from DataBase.Services.auth_service import reg_student, logout_student

student_router = Router()

# ==== РЕГИСТРАЦИЯ СТУДЕНТА ====
@student_router.callback_query(F.data == "role_student")
async def start_student_registration(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WaitCode.reg_student)
    await callback.message.answer(
        "🔑 Для регистрации введите ваш уникальный код доступа:",
        reply_markup=cancel_kb()
    )
    await callback.answer()

@student_router.message(WaitCode.reg_student)
async def finish_student_registration(message: Message, state: FSMContext):
    result = await reg_student(tg_id=message.from_user.id, code=message.text.strip())
    
    if result["status"]:
        await message.answer("✅ Регистрация успешно завершена!")
        await cmd_start(message)
    else:
        await message.answer(f"❌ Ошибка: {result['info']}")
    
    await state.clear()

# ==== ОТПРАВКА ОПРОСА ====
@student_router.callback_query(F.data == "post_que")
async def post_que(callback: CallbackQuery):
    await callback.answer("❌ Программа опросов пока что недоступна")

# ==== ПРЕДЛОЖЕНИЕ ИДЕЙ ====
@student_router.callback_query(F.data == "post_idea")
async def post_idea(callback: CallbackQuery):
    await callback.answer("❌ Программа предложений пока что недоступна")

    
# ==== ПРОСМОТР РАСПИСАНИЯ ====
@student_router.callback_query(F.data == "schedule")
async def post_idea(callback: CallbackQuery):
    await callback.answer("❌ Программа расписаний пока что недоступна")

# ==== ВЫXОД ИЗ АККАУНТА СТУДЕНТА ====
@student_router.callback_query(F.data == "exit_student")
async def exit_student(callback: CallbackQuery):
    result = await logout_student(tg_id=callback.from_user.id)

    if result["status"]:
        await callback.message.answer("✅ Вы успешно вышли из аккаунта")
        await cmd_start(callback.message)
    else:
        await callback.answer(f"❌ {result['info']}")

    await callback.answer()