from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserReadSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    notifiable: bool = Field(False)
    last_activity: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None


class UserUpdateSchema(BaseModel):
    notifiable: bool | None = None
    last_activity: datetime | None = None
