from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, AsyncGenerator, Awaitable, Callable
from sqlalchemy import BigInteger, MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.settings import DatabaseSettings

metadata = MetaData()


def make_engine(dns: str, echo: bool = False) -> AsyncEngine:
    """
    Создание асинхронного движка
    """

    return create_async_engine(url=dns, echo=echo)


def make_async_session_factory(
    dns: str, echo: bool = False
) -> async_sessionmaker[AsyncSession]:
    """
    Создание фабрики асинхронных сессий
    """

    return async_sessionmaker(
        bind=make_engine(dns, echo),
        expire_on_commit=False,
        autoflush=False,
    )  # type: ignore


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Получение транзакции
    """

    async with make_async_session_factory(DatabaseSettings().url, False)() as session:  # type: ignore
        async with session.begin():
            yield session


def transactional(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """
    Декоратор, прокидывающий объект транзакции в функцию
    """

    @wraps(func)
    async def wrapper(*args: tuple[Any, ...], **kwargs: Any) -> Any:
        async with get_session() as session:
            await func(session=session, *args, **kwargs)

    return wrapper


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__: bool = True

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)

    metadata = metadata
