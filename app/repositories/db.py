from typing import Generic, Self, TypeVar, Any

from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base

IdType = int | str


Model = TypeVar("Model", bound=Base)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class DbCrudRepository(Generic[Model, ReadSchema, CreateSchema, UpdateSchema]):
    model_type: type[Model]
    model_schema: type[ReadSchema]

    def __init__(self: Self, session: AsyncSession) -> None:
        self.session = session

    async def create(self: Self, create_schema: CreateSchema) -> ReadSchema:
        """
        Создание записи
        """

        statement = (
            insert(self.model_type)
            .values(create_schema.model_dump())
            .returning(self.model_type)
        )
        instance = await self.session.scalar(statement)
        if not instance:
            raise Exception()
        return self.model_schema.model_validate(instance)

    async def get_by(self: Self, **filters: Any) -> ReadSchema | None:
        """
        Получение записи по фильтрам
        """

        statement = select(self.model_type).filter_by(**filters)
        instance = await self.session.scalar(statement)
        return self.model_schema.model_validate(instance) if instance else None

    async def get_all_by(self: Self, **filters: Any) -> list[ReadSchema]:
        """
        Получение списка записей по фильтрам
        """

        statement = select(self.model_type).filter_by(**filters)
        instances = await self.session.scalars(statement)
        return [self.model_schema.model_validate(instance) for instance in instances]

    async def get_all(self: Self) -> list[ReadSchema]:
        """
        Получение списка записей
        """

        statement = select(self.model_type)
        instances = await self.session.scalars(statement)
        return [self.model_schema.model_validate(instance) for instance in instances]

    async def exists_by(self: Self, **filters: Any) -> bool:
        """
        Проверка на существование записи по фильтрам
        """

        instance = await self.get_by(**filters)
        return instance is not None

    async def update(
        self: Self, id_: IdType, update_schema: UpdateSchema
    ) -> ReadSchema:
        """
        Обновление записи
        """

        statement = (
            update(self.model_type)
            .filter_by(id=id_)
            .values(update_schema.model_dump(exclude_none=True))
            .returning(self.model_type)
        )
        instance = await self.session.scalar(statement)
        if not instance:
            raise Exception()
        return self.model_schema.model_validate(instance)

    async def delete(self: Self, id_: IdType) -> int | str | None:
        """
        Удаление записи
        """

        statement = (
            delete(self.model_type).filter_by(id=id_).returning(self.model_type.id)  # type: ignore
        )
        deleted_id = await self.session.scalar(statement)
        return deleted_id
