from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.apps.user.constants import Commands


def menu_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=Commands.to_tasks)
    kb.button(text=Commands.to_progress)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
