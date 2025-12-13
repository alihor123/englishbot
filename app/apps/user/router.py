from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.progress.keyboards import progress_keyboard
from app.apps.user.keyboards import menu_keyboard
from app.apps.user.schemas import UserCreateSchema
from app.apps.user.service import UserService
from app.apps.user.constants import Callbacks
from app.db import transactional


router = Router()


@router.message(Command("start"))
@transactional
async def handle_start_comand(message: Message, session: AsyncSession) -> None:
    """
    Обработка команды старт
    """
    if message.from_user is None:
        await message.answer("Не удалось определить кто вы")
        return

    user_service = UserService(session=session)

    user = await user_service.authenticate(
        UserCreateSchema(
            id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        ),
    )
    await message.answer(f"Привет {user.first_name}", reply_markup=menu_keyboard())


@router.callback_query(F.data == Callbacks.switch_notifications)
@transactional
async def handle_switch_notifications_callback(
    cb: CallbackQuery,
    session: AsyncSession
) -> None:
    """
    Обработка нажатия на кнопку вкл/выкл уведомления
    """

    user_service = UserService(session=session)
    updated_user = await user_service.switch_notifications(cb.from_user.id)

    await cb.answer(
        text="Уведомления включены"
        if updated_user.notifiable
        else "Уведомления выключены"
    )

    await cb.message.edit_reply_markup(  # type: ignore
        reply_markup=progress_keyboard(notifiable=updated_user.notifiable)
    )
