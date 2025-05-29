from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Bot.keyboards import *
from DataBase.Services.auth_service import log_student, log_teacher

common_router = Router()

@common_router.message(Command("start", "menu"))
async def cmd_start(message: Message):
    teacher = await log_teacher(tg_id = message.from_user.id)
    student = await log_student(tg_id = message.from_user.id)
    
    if teacher["status"]:
        text = (
            f"👋 Здравствуйте, {teacher['name']} {teacher['patronymic']}!\n\n"
            "📚 С помощью этого бота вы можете управлять базой данных проекта 'Lobby'"
        )
        await message.answer(text, reply_markup=teacher_main_kb())
        
    elif student["status"]:
        text = f"👋 Привет, {student['name']}!"
        await message.answer(text, reply_markup=student_main_kb())
        
    else:
        text = (
            "👋 Приветствую!\n\n"
            "🤖 Этот бот - универсальный инструмент любого кванторианца\n"
            "😉C его помощью ученики могут:\n"
            "  🟣Просмотреть расписание занятий и мероприятий\n"
            "  🔴Узнать о событиях в кванториуме одним из первых\n"
            '  🟢Открыть платформу "Lobby" под своим аккаунтом\n\n'
            '🕛Сейчас вы можете открыить "Lobby"🛜 в качестве гостя👨‍🦰, нажмите на кнопку слева внизу!'
        )
        await message.answer(text, reply_markup=role_selection_kb())

@common_router.callback_query(F.data == "cancel_operation")
async def cancel_operation(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Операция отменена")
    await cmd_start(callback.message)
    await callback.answer()