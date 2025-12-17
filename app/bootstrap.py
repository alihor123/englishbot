import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from loguru import logger
from app.middlewares import use_middlewares
from app.scheduler import scheduler
from app.exceptions import use_error_handlers
from app.router import use_routes
from app.settings import AppSettings


async def on_startup() -> None:
    scheduler.start()


async def on_shutdown() -> None:
    scheduler.shutdown()


async def create_app() -> None:
    """
    Иницилизация и запуск приложения
    """

    settings = AppSettings()  # type: ignore
    bot = Bot(settings.telegram.token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    use_error_handlers(dp)
    use_middlewares(dp)
    use_routes(dp)

    try:
        logger.debug("Starting application")
        await on_startup()
        await dp.start_polling(bot)  # type: ignore
    finally:
        logger.debug("Gracefully shutting down")
        await bot.session.close()
        await on_shutdown()


if __name__ == "__main__":
    asyncio.run(create_app())
