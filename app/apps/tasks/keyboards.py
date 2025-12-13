from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.apps.tasks.schemas.task_type import TaskTypeReadSchema
from app.apps.tasks.constants import Callbacks
from app.apps.tasks.schemas.topic import TopicReadSchema


def topics_selection(topics: list[TopicReadSchema]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for topic in topics:
        kb.button(text=topic.name, callback_data=f"topic-{topic.id}")
    kb.adjust(1)
    return kb.as_markup()


def types_selection(task_types: list[TaskTypeReadSchema]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for task_type in task_types:
        kb.button(text=task_type.name, callback_data=f"task_type-{task_type.id}")
    kb.button(text="Назад", callback_data=Callbacks.back_to_topic_selection)
    kb.adjust(1)
    return kb.as_markup()


def back_to_topics_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="К списку тем", callback_data=Callbacks.back_to_topic_selection)
    kb.adjust(1)
    return kb.as_markup()


def back_to_types_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="К выбору типов", callback_data=Callbacks.back_to_types_selection)
    kb.adjust(1)
    return kb.as_markup()


def regenerate_task_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Сгенерировать другое", callback_data=Callbacks.regenerate_task)
    kb.button(text="назад", callback_data=Callbacks.back_to_types_selection)
    kb.adjust(1)
    return kb.as_markup()


def cancel_task_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Прекратить", callback_data=Callbacks.cancel_task)
    kb.adjust(1)
    return kb.as_markup()
