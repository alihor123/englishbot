from app.apps.tasks.models.topic import Topic
from app.apps.tasks.schemas.topic import (
    TopicCreateSchema,
    TopicReadSchema,
    TopicUpdateSchema,
)
from app.repositories.db import DbCrudRepository


class TopicRepository(
    DbCrudRepository[Topic, TopicReadSchema, TopicCreateSchema, TopicUpdateSchema]
):
    model_type = Topic
    model_schema = TopicReadSchema
