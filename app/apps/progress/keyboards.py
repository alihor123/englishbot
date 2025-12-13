from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.apps.progress.constants import Callbacks
from app.apps.tasks.schemas.topic import TopicReadSchema
from app.apps.user.constants import Callbacks as UserCallbacks


def progress_keyboard(notifiable: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Подробнее", callback_data=Callbacks.topic_progress)
    kb.button(
        text=("Выключить" if notifiable else "Включить") + " уведомления",
        callback_data=UserCallbacks.switch_notifications,
    )
    kb.adjust(2)
    return kb.as_markup()


def to_topics_progress() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data=Callbacks.topic_progress)
    kb.adjust(1)
    return kb.as_markup()


def topics_progress_selection(topics: list[TopicReadSchema]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for topic in topics:
        kb.button(
            text=topic.name, callback_data=f"{Callbacks.topic_progress}-{topic.id}"
        )
    kb.button(text="Назад", callback_data=Callbacks.to_progress)
    kb.adjust(1)
    return kb.as_markup()
