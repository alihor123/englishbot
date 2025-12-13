from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.progress.constants import Callbacks
from app.apps.progress.keyboards import (
    progress_keyboard,
    to_topics_progress,
    topics_progress_selection,
)
from app.apps.progress.service import ProgressService
from app.apps.tasks.services.topic import TopicService
from app.apps.user.constants import Commands as UserCommands
from app.apps.user.service import UserService
from app.db import transactional


router = Router()


@router.message(F.text == UserCommands.to_progress)
@transactional
async def handle_to_progress_command(message: Message, session: AsyncSession) -> None:
    """
    Вывод прогресса пользователя
    """

    if message.from_user is None:
        await message.answer("Не удалось определить кто вы")
        return

    user_service = UserService(session=session)
    progress_service = ProgressService(session=session)
    user = await user_service.get_by_id(message.from_user.id)
    progress = await progress_service.get_all(user.id)

    answer = (
        f"<b>{message.from_user.first_name}</b>\n"
        f"Ваш прогресс\n\n"
        f"<b>Общее количество данных ответов</b>: {progress.total_answers}\n\n"
        f"<b>Количество правильных ответов</b>: {progress.total_correct_answers}\n\n"
        f"<b>Количество неверных ответов</b>: {progress.total_incorrect_answers}\n\n"
    )

    await message.answer(answer, reply_markup=progress_keyboard(user.notifiable))


@router.callback_query(F.data == Callbacks.topic_progress)
@transactional
async def handle_topics_progress_callback(
    cb: CallbackQuery, session: AsyncSession
) -> None:
    """
    Вывод списка топиков, по которым можно узнать прогресс
    """

    if not cb.message:
        await cb.answer("Что то пошло не так")
        return

    cb.answer()
    topic_service = TopicService(session=session)
    topics = await topic_service.get_all()
    await cb.message.edit_text(  # type: ignore
        "Выберите тему, по которой хотите узнать свой прогресс",
        reply_markup=topics_progress_selection(topics),
    )


@router.callback_query(F.data.startswith(f"{Callbacks.topic_progress}-"))
@transactional
async def handle_topic_progress_callback(
    cb: CallbackQuery, session: AsyncSession
) -> None:
    """
    Вывод прогресса по выбраному топику
    """

    if not cb.message or not cb.data:
        await cb.answer("Что то пошло не так")
        return

    cb.answer()

    topic_id = int(cb.data.split("-")[1])
    if not topic_id:
        await cb.answer("Произошла ошибка при выборе темы, попробуй еще раз")

    progress_service = ProgressService(session=session)
    topic_serviec = TopicService(session=session)
    topic = await topic_serviec.get_by_id(topic_id)
    topic_progress = await progress_service.get_by_topic(cb.from_user.id, topic.id)

    answer = (
        (
            f"<b>Прогресс по теме</b> <i>{topic.name}</i>\n"
            f"{topic.description}\n\n"
            f"<b>Общее количество данных ответов</b>: {topic_progress.total_answers}\n\n"
            f"<b>Количество правильных ответов</b>: {topic_progress.total_correct_answers}\n\n"
            f"<b>Количество неверных ответов</b>: {topic_progress.total_incorrect_answers}\n\n"
        )
        if topic_progress
        else "<i>Вы еще не решали задачи по этой теме</i>"
    )

    await cb.message.edit_text(answer, reply_markup=to_topics_progress())  # type: ignore


@router.callback_query(F.data == Callbacks.to_progress)
@transactional
async def handle_back_to_progress_callback(
    cb: CallbackQuery, session: AsyncSession
) -> None:
    """
    Возвращение к прогрессу пользователя
    """

    cb.answer()

    if cb.message is None:
        await cb.answer("Что то пошло не так")
        return

    user_service = UserService(session=session)
    progress_service = ProgressService(session=session)
    user = await user_service.get_by_id(cb.from_user.id)
    progress = await progress_service.get_all(user.id)

    answer = (
        f"<b>{cb.from_user.first_name}</b>\n"
        f"Ваш прогресс\n\n"
        f"<b>Общее количество данных ответов</b>: {progress.total_answers}\n\n"
        f"<b>Количество правильных ответов</b>: {progress.total_correct_answers}\n\n"
        f"<b>Количество неверных ответов</b>: {progress.total_incorrect_answers}\n\n"
    )

    await cb.message.edit_text(answer, reply_markup=progress_keyboard(user.notifiable))  # type: ignore
