from pydantic import BaseModel, ConfigDict, Field


class TopicReadSchema(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class TopicCreateSchema(BaseModel):
    name: str
    description: str


class TopicUpdateSchema(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
