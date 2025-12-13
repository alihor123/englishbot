from pydantic import BaseModel, ConfigDict


class ProgressSchema(BaseModel):
    total_answers: int
    total_correct_answers: int
    total_incorrect_answers: int

    model_config = ConfigDict(from_attributes=True)
