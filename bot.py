import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_config
from handlers import user


async def main():
    logging.basicConfig(level=logging.DEBUG)
    # Загрузка конфигурации
    config = load_config()

    # Инициализация бота
    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
    dp.include_router(user.router)

    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
