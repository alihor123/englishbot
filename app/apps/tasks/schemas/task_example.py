from typing import Self
from pydantic import BaseModel, ConfigDict

from app.apps.tasks.models.task_example import TaskExample
from app.apps.tasks.schemas.topic import TopicReadSchema
from app.apps.tasks.schemas.task_type import TaskTypeReadSchema


class TaskExampleReadSchema(BaseModel):
    id: int
    task_type: TaskTypeReadSchema
    topic: TopicReadSchema
    text: str

    @classmethod
    def model_validate(
        cls,
        obj: TaskExample,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: object | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self:
        _ = strict
        _ = from_attributes
        _ = context
        _ = by_alias
        _ = by_name
        return cls(
            id=obj.id,
            task_type=TaskTypeReadSchema.model_validate(obj.task_type),
            topic=TopicReadSchema.model_validate(obj.topic),
            text=obj.text,
        )

    model_config = ConfigDict(from_attributes=True)


class TaskExampleCreateSchema(BaseModel):
    task_type_id: int
    topic_id: int
    text: str


class TaskExampleUpdateSchema(BaseModel):
    text: str | None = None
