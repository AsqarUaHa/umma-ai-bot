import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import config
from core.logger import setup_logger
from database.db import init_db
from handlers.user import router
from knowledge.vector_store import VectorStore

logger = setup_logger(__name__)


async def main():
    """Главная функция запуска бота"""
    logger.info("Запуск бота...")

    # Инициализация БД (опционально)
    if config.USE_DATABASE:
        await init_db()
        logger.info("База данных инициализирована")
    else:
        logger.info("База данных отключена (USE_DATABASE=false)")

    # Инициализация векторного хранилища
    vector_store = VectorStore()
    await vector_store.initialize()
    logger.info("Векторное хранилище инициализировано")

    # Инициализация бота
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(router)

    # Добавляем vector_store в контекст
    dp["vector_store"] = vector_store

    logger.info("Бот запущен и готов к работе")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
