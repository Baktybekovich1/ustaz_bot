import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from app.config import BOT_TOKEN, REDIS_DSN
from app.handlers import start, courses, guides, signup, faq, admin
from app.db import engine
from app.models import Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    storage = RedisStorage.from_url(REDIS_DSN)
    dp = Dispatcher(storage=storage)
    dp.include_router(start.router)
    dp.include_router(courses.router)
    dp.include_router(guides.router)
    dp.include_router(signup.router)
    dp.include_router(faq.router)
    dp.include_router(admin.router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="export", description="Экспорт лидов (админ)")
    ])


    await init_db()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
