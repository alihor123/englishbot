from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.ai.schemas import HumanMessageSchema, SystemMessageSchema
from app.apps.ai.service import AiService
from app.apps.progress.schemas.answer import AnswerReadSchema, AnswerCreateSchema
from app.apps.progress.service import ProgressService
from app.apps.tasks.schemas.task import TaskCreateSchema, TaskReadSchema
from app.exceptions import ModelNotFoundError
from app.apps.tasks.repositories.task_example import TaskExampleRepository


class TaskService:
    def __init__(self: Self, session: AsyncSession) -> None:
        self.ai_service = AiService()
        self.progress_service = ProgressService(session=session)
        self.task_example_repository = TaskExampleRepository(session=session)

    async def get(self: Self, task_create_schema: TaskCreateSchema) -> TaskReadSchema:
        """
        Получение упражнения
        """

        task_example = await self.task_example_repository.get_by(
            topic_id=task_create_schema.topic.id,
            task_type_id=task_create_schema.task_type.id,
        )
        if not task_example:
            raise ModelNotFoundError(model="Пример задачи")

        task = await self.ai_service.promt(
            [
                SystemMessageSchema(
                    content="Ты учитель английского языка, который создает упражнения"
                ),
                HumanMessageSchema(
                    content=(
                        f"Сгенерируй упражнение по английскому языку на тему: {task_example.topic.name}"
                        f"Тип задания: {task_example.task_type.name}"
                        f"Пример задания: {task_example.text}"
                        f"Задание должно отличаться от примера"
                        f"Очень важно: не присылай ответ на это упражнение - это запрещено"
                    )
                ),
            ]
        )

        return TaskReadSchema(
            topic=task_example.topic,
            task_type=task_example.task_type,
            task=task.content,
        )

    async def check(
        self: Self, user_id: int, answer: str, task: TaskReadSchema
    ) -> AnswerReadSchema:
        response = await self.ai_service.promt(
            [
                SystemMessageSchema(
                    content="Ты эксперт по проверке заданий на английском языке."
                ),
                HumanMessageSchema(
                    content=(
                        f"Текст задания: {task.task}. "
                        f"Ответ студента: {answer}. "
                        "Если ответ правильный — напиши ровно одно слово 'Да'. "
                        "Если ответ неправильный — напиши ровно одно слово 'Нет'. "
                        "Ничего больше не добавляй."
                    )
                ),
            ]
        )

        normalized = response.content.strip().lower()
        is_correct = normalized == "да"

        return await self.progress_service.save(
            AnswerCreateSchema(
                user_id=user_id,
                topic_id=task.topic.id,
                task=task.task,
                is_correct=is_correct,
            )
        )
