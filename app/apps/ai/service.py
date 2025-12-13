from typing import Self

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_gigachat import GigaChat
from loguru import logger

from app.apps.ai.schemas import (
    AiResponseSchema,
    BaseMessageSchema,
    HumanMessageSchema,
    SystemMessageSchema,
)
from app.settings import AiSettings


class AiService:
    def __init__(self: Self) -> None:
        settings = AiSettings()  # type: ignore
        self.model = GigaChat(
            credentials=settings.token,
            model=settings.model,
            verify_ssl_certs=settings.secure,
        )

    async def promt(self: Self, messages: list[BaseMessageSchema]) -> AiResponseSchema:
        model_input: list[BaseMessage] = []
        for message in messages:
            if isinstance(message, HumanMessageSchema):
                model_input.append(HumanMessage(content=message.content))
            elif isinstance(message, SystemMessageSchema):
                model_input.append(SystemMessage(content=message.content))
            else:
                logger.warning("Unknown ai message type")

        response = await self.model.ainvoke(model_input)
        return AiResponseSchema(content=response.content)  # type: ignore
