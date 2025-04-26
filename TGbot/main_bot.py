from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TGbot.config import settings


# Инициализация бота и диспетчера ---------------------------------------------------------------
bot = Bot(token=settings.get_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
# Инициализация бота и диспетчера ---------------------------------------------------------------


# Команда /start ---------------------------------------------------------------
@dp.message(Command("start"))
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
            text="Узнать свой Tg id",
            callback_data="get_tg_id"
        )
    )

    welcome_message = ( 
        "Привет!✌️ Я - телеграмм бот кванториума🤖\n"
        "Я могу:\n"
        "• Открыть \"Lobby\" - сайт-игру кванториума🎮\n"
        "• Принять твой опрос и отправить его всем ученикам концретных групп✍️\n"
        "• Выслушать твои идеи по улучшению меня и Lobby👂\n"
        "• Уведомить тебя о предстоящих событиях или изменениях🗞️\n"
        "Удачи тебе в постижении новых целей!😉"
    )
    await message.answer(
        welcome_message,
        reply_markup=builder.as_markup()
    )
# Команда /start ---------------------------------------------------------------


# Полученеи ID ---------------------------------------------------------------
@dp.callback_query(F.data == "get_tg_id")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(f"Ваш Tg id: {callback.from_user.id}")
    await callback.answer()
# Полученеи ID ---------------------------------------------------------------


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