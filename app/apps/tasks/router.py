from typing import Any
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.tasks.keyboards import (
    back_to_types_button,
    cancel_task_button,
    regenerate_task_button,
    topics_selection,
    types_selection,
)
from app.apps.tasks.schemas.task import TaskCreateSchema, TaskReadSchema
from app.apps.tasks.services.task import TaskService
from app.apps.tasks.services.task_type import TaskTypeService
from app.apps.tasks.services.topic import TopicService
from app.apps.tasks.state import TaskState
from app.apps.tasks.constants import Callbacks
from app.apps.user.constants import Commands as UserCommands
from app.db import transactional


router = Router()


@router.message(F.text == UserCommands.to_tasks)
@transactional
async def handle_to_task_command(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обработка команды перехода к упражнениям
    """

    topic_service = TopicService(session=session)
    topics = await topic_service.get_all()
    await state.set_state(TaskState.topic_selection)
    await message.answer(
        text="Список доступных тем", reply_markup=topics_selection(topics)
    )


@router.callback_query(F.data.startswith("topic-"), TaskState.topic_selection)
@transactional
async def handle_topic_selection_callback(
    cb: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обработка выбора топика
    """

    await cb.answer()
    if cb.data is None or not cb.message:
        await cb.answer("Что то пошло не так")
        await state.clear()
        return

    topic_id = int(cb.data.split("-")[1])
    if not topic_id:
        await cb.answer("Что то пошло не так при выборе топика")
        await state.clear()
        return

    await state.update_data(topic_id=topic_id)
    await state.set_state(TaskState.type_selection)

    task_type_service = TaskTypeService(session=session)
    task_types = await task_type_service.get_all()
    await cb.message.edit_text(  # type: ignore
        text="\n\n Выбретие тип задания", reply_markup=types_selection(task_types)
    )


@router.callback_query(F.data.startswith("task_type-"), TaskState.type_selection)
@transactional
async def handle_task_type_selection_callback(
    cb: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обработка выбора типа задания
    """

    await cb.answer()
    if cb.data is None or not cb.message:
        await cb.answer("Что то пошло не так")
        await state.clear()
        return

    task_type_id = int(cb.data.split("-")[1])
    if not task_type_id:
        await cb.answer("Что то пошло не так при выборе типа задания")
        await state.clear()
        return

    await state.update_data(task_type_id=task_type_id)

    topic_id = await state.get_value("topic_id")
    if not topic_id:
        await cb.answer("Что то пошло не так при попытке сгенерировать задание")
        await state.clear()
        return

    task_service = TaskService(session=session)
    topic_service = TopicService(session=session)
    task_type_service = TaskTypeService(session=session)

    topic = await topic_service.get_by_id(topic_id)
    task_type = await task_type_service.get_by_id(task_type_id)

    task = await task_service.get(TaskCreateSchema(topic=topic, task_type=task_type))
    await state.set_state(TaskState.verify)
    await state.update_data(task=task.model_dump())
    await cb.message.edit_text(text=task.task, reply_markup=regenerate_task_button())  # type: ignore


@router.message(TaskState.verify)
@transactional
async def handle_user_answer_message(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обработка ответа пользвателя на задание
    """

    if message.from_user is None:
        await message.answer("Что то пошло не так")
        await state.clear()
        return

    data: dict[str, Any] | None = await state.get_value("task")
    if not data:
        await message.answer("Что то пошло не так при проверке ответа")
        await state.clear()
        return

    task = TaskReadSchema(**data)
    task_service = TaskService(session=session)
    answer = await task_service.check(
        message.from_user.id,
        message.text or "",
        task,
    )

    if answer.is_correct:
        await state.set_state(TaskState.topic_selection)
        await message.answer(
            "Правильно, вы молодец!", reply_markup=back_to_types_button()
        )
        return

    await message.answer(
        "Неверное, можете попробовать еще раз или в следующий раз",
        reply_markup=cancel_task_button(),
    )


@router.callback_query(F.data == Callbacks.back_to_types_selection)
@transactional
async def handle_back_to_types_selection_callback(
    cb: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обработка возвращения к выбору типа задания
    """

    if cb.message is None:
        await cb.answer("Что то пошло не так")
        await state.clear()
        return

    task_type_service = TaskTypeService(session=session)
    task_types = await task_type_service.get_all()
    await state.set_state(TaskState.type_selection)
    await cb.message.edit_text(  # type: ignore
        text="Выберите тему", reply_markup=types_selection(task_types)
    )


@router.callback_query(F.data == Callbacks.back_to_topic_selection)
@transactional
async def handle_back_to_topic_selection_callback(
    cb: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обработка возвращения к выбору топика
    """

    if cb.message is None:
        await cb.answer("Что то пошло не так")
        await state.clear()
        return

    topic_service = TopicService(session=session)
    topic = await topic_service.get_all()
    await state.set_state(TaskState.topic_selection)
    await cb.message.edit_text(  # type: ignore
        text="Выберите тему", reply_markup=topics_selection(topic)
    )


@router.callback_query(F.data == Callbacks.regenerate_task)
@transactional
async def handle_regenerate_task_callback(
    cb: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Обрабокта вызова ре генереации задания
    """

    await cb.answer()
    data: dict[str, Any] | None = await state.get_value("task")
    if not data:
        await cb.answer("Что то пошло не так при попытке ре-генерации задания")
        await state.clear()
        return

    task = TaskReadSchema(**data)
    task_service = TaskService(session=session)

    task = await task_service.get(
        TaskCreateSchema(topic=task.topic, task_type=task.task_type)
    )
    await state.set_state(TaskState.verify)
    await state.update_data(task=task.model_dump())
    await cb.message.edit_text(text=task.task, reply_markup=regenerate_task_button())  # type: ignore


@router.callback_query(F.data == Callbacks.cancel_task, TaskState.verify)
async def handel_cancel_task_callback(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка вызова отмены выполнения задания
    """

    await cb.answer(text="Переход к выбору топика")
    await handle_back_to_topic_selection_callback(cb, state)
