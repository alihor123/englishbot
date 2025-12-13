from app.apps.tasks.models.task_type import TaskType
from app.apps.tasks.schemas.task_type import (
    TaskTypeCreateSchema,
    TaskTypeReadSchema,
    TaskTypeUpdateSchema,
)
from app.repositories.db import DbCrudRepository


class TaskTypeRepository(
    DbCrudRepository[
        TaskType, TaskTypeReadSchema, TaskTypeCreateSchema, TaskTypeUpdateSchema
    ]
):
    model_type = TaskType
    model_schema = TaskTypeReadSchema
