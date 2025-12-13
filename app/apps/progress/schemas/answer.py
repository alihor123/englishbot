from pydantic import BaseModel, ConfigDict


class AnswerReadSchema(BaseModel):
    id: int
    user_id: int
    topic_id: int
    task: str
    is_correct: bool

    model_config = ConfigDict(from_attributes=True)


class AnswerCreateSchema(BaseModel):
    user_id: int
    topic_id: int
    task: str
    is_correct: bool


class AnswerUpdateSchema(BaseModel):
    is_correct: bool
