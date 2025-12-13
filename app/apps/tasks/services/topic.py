from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.tasks.repositories.topic import TopicRepository
from app.apps.tasks.schemas.topic import TopicReadSchema
from app.exceptions import ModelNotFoundError


class TopicService:
    def __init__(self: Self, session: AsyncSession) -> None:
        self.topic_repository = TopicRepository(session=session)

    async def get_by_id(self: Self, topic_id: int) -> TopicReadSchema:
        """
        Получение топика по id
        """

        topic = await self.topic_repository.get_by(id=topic_id)
        if not topic:
            raise ModelNotFoundError(model="Топик")

        return topic

    async def get_all(self: Self) -> list[TopicReadSchema]:
        """
        Получение списка всех топиков
        """

        return await self.topic_repository.get_all_by()
