from datetime import datetime
from typing import Self

from sqlalchemy import select
from app.apps.user.models import User
from app.apps.user.schemas import UserCreateSchema, UserReadSchema, UserUpdateSchema
from app.repositories.db import DbCrudRepository


class UserRepository(
    DbCrudRepository[User, UserReadSchema, UserCreateSchema, UserUpdateSchema]
):
    model_type = User
    model_schema = UserReadSchema

    async def get_inactive(self: Self, period: datetime) -> list[UserReadSchema]:
        statement = select(User).filter(User.last_activity < period, User.notifiable)
        instances = await self.session.scalars(statement)
        return [UserReadSchema.model_validate(instance) for instance in instances]
