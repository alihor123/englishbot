from pydantic import BaseModel

from app.apps.tasks.schemas.task_type import TaskTypeReadSchema
from app.apps.tasks.schemas.topic import TopicReadSchema


class TaskReadSchema(BaseModel):
    topic: TopicReadSchema
    task_type: TaskTypeReadSchema
    task: str


class TaskCreateSchema(BaseModel):
    topic: TopicReadSchema
    task_type: TaskTypeReadSchema
