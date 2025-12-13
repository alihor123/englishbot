from typing import Self

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.progress.repository import AnswerRepository
from app.apps.progress.schemas.answer import AnswerCreateSchema, AnswerReadSchema
from app.apps.progress.schemas.progress import ProgressSchema


class ProgressService:
    def __init__(self: Self, session: AsyncSession) -> None:
        self.answer_repository = AnswerRepository(session=session)

    async def save(
        self: Self, answer_create_schema: AnswerCreateSchema
    ) -> AnswerReadSchema:
        """
        Сохранeние ответа
        """

        answer = await self.answer_repository.create(answer_create_schema)
        logger.info("Created answer %d", answer.id)
        return answer

    async def get_all(self: Self, user_id: int) -> ProgressSchema:
        """
        Получение общего прогресса
        """

        return await self.answer_repository.get_progress(user_id)

    async def get_by_topic(
        self: Self, user_id: int, topic_id: int
    ) -> ProgressSchema | None:
        """
        Получение прогресса по топику
        """

        return await self.answer_repository.get_progress_by_topic(user_id, topic_id)
