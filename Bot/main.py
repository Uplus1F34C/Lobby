import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.types import Message

# Добавляем корень проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Bot.settings.config import settings
from Bot.handlers import common, teacher, student

async def main():
    bot = Bot(token=settings.get_token)
    dp = Dispatcher()
    
    dp.include_routers(
        common.common_router,
        teacher.teacher_router,
        student.student_router
    )
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    print("Бот запущен")
    asyncio.run(main())