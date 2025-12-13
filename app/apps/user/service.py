from datetime import datetime, timedelta
from typing import Self
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.user.repository import UserRepository
from app.apps.user.schemas import UserCreateSchema, UserReadSchema, UserUpdateSchema
from app.exceptions import ModelNotFoundError


class UserService:
    user_repository: UserRepository

    def __init__(self, session: AsyncSession) -> None:
        self.user_repository = UserRepository(session=session)

    async def authenticate(
        self: Self, create_schema: UserCreateSchema
    ) -> UserReadSchema:
        """
        Аутентификация пользователя
        """

        user = await self.user_repository.get_by(id=create_schema.id)
        if not user:
            user = await self.user_repository.create(create_schema)
            logger.info(f"Created user {user.id}")

        return user

    async def get_by_id(self: Self, user_id: int) -> UserReadSchema:
        """
        Получение пользователя по id
        """

        user = await self.user_repository.get_by(id=user_id)
        if not user:
            raise ModelNotFoundError(model="Пользователь")

        return user

    async def update_activity(self: Self, user_id: int) -> None:
        """
        Обновление времени последней активности у пользователя
        """

        user = await self.user_repository.get_by(id=user_id)
        if not user:
            return

        await self.user_repository.update(
            user.id, UserUpdateSchema(last_activity=datetime.now())
        )
        logger.debug("Updated activity for user {user.id}")

    async def list_inactive(self: Self) -> list[UserReadSchema]:
        """
        Получение списка неактивных пользвателей
        """

        return await self.user_repository.get_inactive(
            period=datetime.now() - timedelta(hours=3)
        )

    async def switch_notifications(self: Self, telegram_id: int) -> UserReadSchema:
        """
        Переключение вкл/выкл уведомлений
        """

        user = await self.user_repository.get_by(id=telegram_id)
        if not user:
            raise ModelNotFoundError(model="Пользователь")
        notifiable = not user.notifiable
        updated_user = await self.user_repository.update(
            id_=user.id, update_schema=UserUpdateSchema(notifiable=notifiable)
        )
        logger.info(f"Updated user {updated_user.id}")
        return updated_user
