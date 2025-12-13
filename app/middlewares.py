from typing import Any, Awaitable, Callable

from aiogram import Dispatcher
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.user.service import UserService
from app.db import transactional


@transactional
async def activity_recorder_middleware(
    handler: Callable[[Update, dict[str, Any]], Awaitable[None]],
    event: Update,
    data: dict[str, Any],
    session: AsyncSession,
) -> None:
    if event.message is not None and event.message.from_user:
        user_id = event.message.from_user.id
    else:
        return await handler(event, data)

    user_service = UserService(session=session)
    await user_service.update_activity(user_id)

    return await handler(event, data)


def use_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(activity_recorder_middleware)
