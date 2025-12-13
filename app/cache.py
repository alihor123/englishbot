from functools import wraps
from typing import Any, Awaitable, Callable
from redis.asyncio import Redis

from app.settings import CacheSettings
from app.repositories.cache import RedisCacheRepository


def get_redis_client() -> Redis:
    settings = CacheSettings()  # type: ignore
    return Redis(host=settings.host, port=int(settings.port), db=settings.db)


def cacheable(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """
    Декоратор, прокидывающий объект репозитория редиса в функцию
    """

    @wraps(func)
    async def wrapper(*args: tuple[Any, ...], **kwargs: Any) -> Any:
        cache = get_redis_client()
        return await func(cache=RedisCacheRepository(redis=cache), *args, **kwargs)

    return wrapper
