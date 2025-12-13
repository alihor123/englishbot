from typing import Self
from aiogram import F, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message
from loguru import logger


class BusinessLogicError(Exception):
    @property
    def msg(self: Self) -> str:
        return "Ошибка"


class ModelNotFoundError(BusinessLogicError):
    def __init__(self, *args: object, model: str) -> None:
        super().__init__(*args)
        self.model = model

    @property
    def msg(self: Self) -> str:
        return f"{self.model.capitalize()} не найден"


async def base_error_handler(event: ErrorEvent, message: Message) -> None:
    """
    Базовый обработчик ошибок
    """

    logger.error(f"Critical error caused by {event.exception}", exc_info=True)
    await message.answer("Случилась непредвиденная ошибка, попробуйте позже")


async def business_logic_error_handler(event: ErrorEvent, message: Message) -> None:
    """
    Обработчик ошибок бизнес логики
    """

    logger.error("Error {event.exception}", exc_info=True)
    await message.answer(event.exception.msg)  # type: ignore


def use_error_handlers(dp: Dispatcher) -> None:
    """
    Применение обработчиков ошибок
    """

    dp.error(F.update.message.as_("message"))(base_error_handler)
    dp.error(ExceptionTypeFilter(BusinessLogicError), F.update.message.as_("message"))(
        business_logic_error_handler
    )
