WEB_APP_URL = "https://uplus1f34c.github.io/Lobby/FrontEnd"  # Замените на URL вашего веб-приложения

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram import F

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from TGbot.config import settings

# Инициализация бота и диспетчера
bot = Bot(token=settings.get_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()



@dp.message(Command("start", "help", "h"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Кто ты?")],
        [types.KeyboardButton(text="Отправить опрос")],
        [types.KeyboardButton(text="Предложить свою идею")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери действие"
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
        reply_markup=keyboard
    )

@dp.message(F.text == "Кто ты?")
async def handle_idea(message: types.Message):
    await message.answer(
        "Привет!✌️ Я - телеграмм бот кванториума🤖\n"
        "Я могу:\n"
        "• Открыть \"Lobby\" - сайт-игру кванториума🎮\n"
        "• Принять твой опрос и отправить его всем ученикам концретных групп✍️\n"
        "• Выслушать твои идеи по улучшению меня и Lobby👂\n"
        "• Уведомить тебя о предстоящих событиях или изменениях🗞️\n"
        "Удачи тебе в постижении новых целей!😉")


@dp.message(F.text == "Предложить свою идею")
async def handle_idea(message: types.Message):
    await message.answer("К сожалению эта функция все еще находится в разработке")

@dp.message(F.text == "Отправить опрос")
async def handle_survey(message: types.Message):
    await message.answer("К сожалению эта функция все еще находится в разработке")

@dp.message()
async def handle_other_messages(message: types.Message):
    await message.delete()  # Удаляем все остальные сообщения


# Запуск бота
async def main():
    print("Бот готов к запуску.\nЗапуск...")
    await dp.start_polling(bot)

import asyncio
asyncio.run(main())