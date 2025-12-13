import asyncio
import json
from pathlib import Path
from typing import Any

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.tasks.models.task_example import TaskExample
from app.apps.tasks.models.task_type import TaskType
from app.apps.tasks.models.topic import Topic
from app.db import get_session


SEEDS_DIR: Path = Path(__file__).parent.parent.parent / "seeds"


def load_json(filename: str) -> list[dict[str, Any]]:
    path = SEEDS_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


async def upsert_task_types(session: AsyncSession) -> None:
    data = load_json("task_types.json")

    inserted, updated = 0, 0
    for row in data:
        result = await session.execute(
            select(TaskType).where(TaskType.name == row["name"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            for k, v in row.items():
                setattr(existing, k, v)
            updated += 1
        else:
            session.add(TaskType(**row))
            inserted += 1

    try:
        await session.flush()
        logger.info(f"✅ TaskTypes upserted: inserted={inserted}, updated={updated}")
    except SQLAlchemyError as e:
        logger.error(f"❌ Error upserting task_types: {e}")


async def upsert_topics(session: AsyncSession) -> None:
    data = load_json("topics.json")

    inserted, updated = 0, 0
    for row in data:
        result = await session.execute(select(Topic).where(Topic.name == row["name"]))
        existing = result.scalar_one_or_none()

        if existing:
            for k, v in row.items():
                setattr(existing, k, v)
            updated += 1
        else:
            session.add(Topic(**row))
            inserted += 1

    try:
        await session.flush()
        logger.info(f"✅ Topics upserted: inserted={inserted}, updated={updated}")
    except SQLAlchemyError as e:
        logger.error(f"❌ Error upserting topics: {e}")


async def upsert_task_examples(session: AsyncSession) -> None:
    data = load_json("task_examples.json")

    topic_result = await session.execute(select(Topic.name, Topic.id))
    topics: dict[str, int] = {name: id_ for name, id_ in topic_result.all()}

    task_type_result = await session.execute(select(TaskType.name, TaskType.id))
    task_types: dict[str, int] = {name: id_ for name, id_ in task_type_result.all()}

    inserted, updated, skipped = 0, 0, 0
    for row in data:
        topic_name = row["topic"]
        task_type_name = row["task_type"]

        topic_id = topics.get(topic_name)
        task_type_id = task_types.get(task_type_name)

        if topic_id is None or task_type_id is None:
            logger.warning(
                f"⚠️ Пропущен task_example (topic={topic_name}, task_type={task_type_name})"
            )
            skipped += 1
            continue

        result = await session.execute(
            select(TaskExample).where(
                TaskExample.topic_id == topic_id,
                TaskExample.task_type_id == task_type_id,
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.text = row["text"]
            updated += 1
        else:
            session.add(
                TaskExample(
                    topic_id=topic_id,
                    task_type_id=task_type_id,
                    text=row["text"],
                )
            )
            inserted += 1

    try:
        await session.flush()
        logger.info(
            f"✅ TaskExamples upserted: inserted={inserted}, updated={updated}, skipped={skipped}"
        )
    except SQLAlchemyError as e:
        logger.error(f"❌ Error upserting task_examples: {e}")


async def main() -> None:
    async with get_session() as session:
        await upsert_task_types(session)
        await upsert_topics(session)
        await upsert_task_examples(session)
        await session.commit()  # сохраняем изменения


if __name__ == "__main__":
    asyncio.run(main())
