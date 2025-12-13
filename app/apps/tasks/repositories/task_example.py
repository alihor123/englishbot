from app.apps.tasks.models.task_example import TaskExample
from app.apps.tasks.schemas.task_example import (
    TaskExampleReadSchema,
    TaskExampleUpdateSchema,
)
from app.apps.tasks.schemas.task_type import TaskTypeCreateSchema
from app.repositories.db import DbCrudRepository


class TaskExampleRepository(
    DbCrudRepository[
        TaskExample,
        TaskExampleReadSchema,
        TaskTypeCreateSchema,
        TaskExampleUpdateSchema,
    ]
):
    model_type = TaskExample
    model_schema = TaskExampleReadSchema
