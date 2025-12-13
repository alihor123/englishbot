from pydantic import BaseModel, ConfigDict, Field


class TaskTypeReadSchema(BaseModel):
    id: int
    name: str
    description: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class TaskTypeCreateSchema(BaseModel):
    name: str
    description: str | None = Field(None)


class TaskTypeUpdateSchema(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
