from typing import Self
from sqlalchemy import case, func, select
from app.apps.progress.schemas.progress import ProgressSchema
from app.apps.tasks.models.topic import Topic
from app.apps.user.models import User
from app.repositories.db import DbCrudRepository
from app.apps.progress.models import Answer
from app.apps.progress.schemas.answer import (
    AnswerCreateSchema,
    AnswerReadSchema,
    AnswerUpdateSchema,
)


class AnswerRepository(
    DbCrudRepository[Answer, AnswerReadSchema, AnswerCreateSchema, AnswerUpdateSchema]
):
    model_type = Answer
    model_schema = AnswerReadSchema

    async def get_progress(self: Self, user_id: int) -> ProgressSchema:
        topic_progress_statement = (
            select(
                Answer.user_id,
                Topic.name,
                func.sum(case((Answer.is_correct, 1), else_=0)).label(
                    "correct_answers"
                ),
                func.sum(case((~Answer.is_correct, 1), else_=0)).label(
                    "incorrect_answers"
                ),
                func.count().label("total_answers"),
            )
            .join(Topic, Answer.topic_id == Topic.id)
            .group_by(Answer.user_id, Topic.name)
            .alias("topic_progress")
        )

        statement = (
            select(
                func.coalesce(
                    func.sum(topic_progress_statement.c.total_answers), 0
                ).label("total_answers"),
                func.coalesce(
                    func.sum(topic_progress_statement.c.correct_answers), 0
                ).label("total_correct_answers"),
                func.coalesce(
                    func.sum(topic_progress_statement.c.incorrect_answers), 0
                ).label("total_incorrect_answers"),
            )
            .select_from(User)
            .outerjoin(
                topic_progress_statement, User.id == topic_progress_statement.c.user_id
            )
            .filter(User.id == user_id)
            .group_by(User.id)
        )

        result = await self.session.execute(statement)
        row = result.mappings().first()
        return ProgressSchema.model_validate(row)

    async def get_progress_by_topic(
        self: Self, user_id: int, topic_id: int
    ) -> ProgressSchema | None:
        statement = (
            select(
                Answer.user_id,
                Topic.name,
                func.sum(case((Answer.is_correct, 1), else_=0)).label(
                    "total_correct_answers"
                ),
                func.sum(case((~Answer.is_correct, 1), else_=0)).label(
                    "total_incorrect_answers"
                ),
                func.count().label("total_answers"),
            )
            .join(Topic, Answer.topic_id == Topic.id)
            .where(Answer.user_id == user_id, Answer.topic_id == topic_id)
            .group_by(Answer.user_id, Topic.name)
        )

        result = await self.session.execute(statement)
        row = result.mappings().first()
        return ProgressSchema.model_validate(row) if row else None
