from dataclasses import dataclass
from typing import Self

from redis.asyncio import Redis


@dataclass
class RedisCacheRepository:
    redis: Redis

    async def set(
        self: Self, key: str, value: str, expire: int | None = None, nx: bool = False
    ) -> None:
        """
        Установка значения по ключу
        """

        await self.redis.set(key, value, ex=expire, nx=nx)

    async def get(self: Self, key: str) -> str | None:
        """
        Получение значения по ключу
        """

        value = await self.redis.get(key)
        return str(value) if value else None

    async def clear(self: Self, key: str) -> None:
        """
        Удаление значения по ключу
        """

        await self.redis.delete(key)
