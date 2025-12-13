from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession
from app.apps.tasks.repositories.task_type import TaskTypeRepository
from app.apps.tasks.schemas.task_type import TaskTypeReadSchema
from app.exceptions import ModelNotFoundError


class TaskTypeService:
    def __init__(self: Self, session: AsyncSession) -> None:
        self.task_type_repository = TaskTypeRepository(session=session)

    async def get_by_id(self: Self, task_type_id: int) -> TaskTypeReadSchema:
        """
        Получение типа задания по id
        """

        task_type = await self.task_type_repository.get_by(id=task_type_id)
        if not task_type:
            raise ModelNotFoundError(model="Тип задания")
        return task_type

    async def get_all(self: Self) -> list[TaskTypeReadSchema]:
        """
        Получение списка типов задач
        """

        return await self.task_type_repository.get_all()
