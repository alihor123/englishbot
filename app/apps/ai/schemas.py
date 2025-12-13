from pydantic import BaseModel


class BaseMessageSchema(BaseModel):
    content: str


class SystemMessageSchema(BaseMessageSchema): ...


class HumanMessageSchema(BaseMessageSchema): ...


class AiResponseSchema(BaseModel):
    content: str
