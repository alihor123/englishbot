from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.ai.schemas import HumanMessageSchema, SystemMessageSchema
from app.apps.ai.service import AiService
from app.apps.progress.schemas.answer import AnswerReadSchema, AnswerCreateSchema
from app.apps.progress.service import ProgressService
from app.apps.tasks.schemas.task import TaskCreateSchema, TaskReadSchema
from app.exceptions import ModelNotFoundError
from app.apps.tasks.repositories.task_example import TaskExampleRepository


class TaskService:
    def __init__(self: Self, session: AsyncSession) -> None:
        self.ai_service = AiService()
        self.progress_service = ProgressService(session=session)
        self.task_example_repository = TaskExampleRepository(session=session)

    async def get(self: Self, task_create_schema: TaskCreateSchema) -> TaskReadSchema:
        """
        Получение упражнения
        """
        task_example = await self.task_example_repository.get_by(
            topic_id=task_create_schema.topic.id,
            task_type_id=task_create_schema.task_type.id,
        )

        if not task_example:
            raise ModelNotFoundError(model="Пример задачи")

        task = await self.ai_service.promt(
            messages=[
                SystemMessageSchema(
                    content="""Ты учитель английского языка A1-A2. Создаешь грамматически ИДЕАЛЬНЫЕ упражнения.

🔴 ГЛАВНОЕ ПРАВИЛО - СОГЛАСОВАНИЕ ПОДЛЕЖАЩЕГО И ГЛАГОЛА:

I/You/We/They → базовая форма глагола (БЕЗ -s)
- I play, You watch, We have, They do

He/She/It → форма с окончанием -s/-es
- He plays, She watches, It has, He does

🔴 ОКОНЧАНИЯ ГЛАГОЛОВ (для He/She/It):
- Обычные: play → plays, work → works
- После -s, -sh, -ch, -x, -o: watch → watches, go → goes, do → does
- Согласная + y: study → studies

🔴 ФОРМЫ TO BE:
- I am
- He/She/It is
- You/We/They are

🔴 ФОРМЫ TO HAVE:
- I/You/We/They have
- He/She/It has

🔴 ПРИ СОЗДАНИИ ВАРИАНТОВ ОТВЕТА:
1. Смотри на подлежащее в КАЖДОМ предложении
2. Подбирай форму глагола под КОНКРЕТНОЕ подлежащее
3. Если подлежащие разные (I, She, They) → формы глаголов тоже РАЗНЫЕ

❌ ПЛОХОЙ пример (ОШИБКА):
You ___ TV. Варианты: a) watches b) plays
Ошибка: "You" требует форму БЕЗ -s, а даны формы С -s

✅ ХОРОШИЙ пример:
You ___ TV. Варианты: a) watch b) play c) watches

ТРЕБОВАНИЯ:
- Задание на русском языке
- Все варианты грамматически корректные
- Только один правильный ответ по смыслу
- Ты создаешь НОВОЕ задание, отличающееся от примера (другие предложения, другие слова)
- Постоянно меняй порядок вариантов ответа, чтобы не получилось так, что немерация предложений соотвествует порядку нумерации правильных ответов
- НЕ присылай правильный ответ"""

                ),
                HumanMessageSchema(
                    content=(
                        f"Создай упражнение:\n\n"
                        f"Тема: {task_example.topic.name}\n"
                        f"Тип задания: {task_example.task_type.name}\n"
                        f"Пример для образца структуры:\n{task_example.text}\n\n"
                        f"ПРОВЕРЬ ПЕРЕД ОТПРАВКОЙ:\n"
                        f"- Все подлежащие (I/You/He/She/It/We/They) имеют ПРАВИЛЬНЫЕ формы глаголов\n"
                        f"- Если He/She/It → обязательно -s/-es на глаголе\n"
                        f"- Если I/You/We/They → БЕЗ -s на глаголе"
                    )
                ),
            ]
        )

        return TaskReadSchema(
            topic=task_example.topic,
            task_type=task_example.task_type,
            task=task.content,
        )

    async def check(
        self: Self, user_id: int, answer: str, task: TaskReadSchema
    ) -> AnswerReadSchema:
        response = await self.ai_service.promt(
            messages=[
                SystemMessageSchema(
                    content="""Ты эксперт по английской грамматике. Проверяешь ответы учеников уровня A1-A2.

🔴 ГРАММАТИЧЕСКИЕ ПРАВИЛА (проверяй СТРОГО):

СОГЛАСОВАНИЕ подлежащего и глагола:
- I/You/We/They + глагол БЕЗ -s (play, have, watch)
- He/She/It + глагол С -s/-es (plays, has, watches)

ОКОНЧАНИЯ:
- -s: plays, works, reads
- -es: watches, goes, does, washes
- -ies: studies (если согласная + y)

ФОРМЫ TO BE:
- I am / He is / You are / We are / They are

ФОРМЫ TO HAVE:
- I have / He has / They have

АРТИКЛИ:
- a (перед согласной): a book, a cat
- an (перед гласной): an apple, an orange

ПРЕДЛОГИ ВРЕМЕНИ:
- in (год, месяц, время суток): in 2020, in May, in the morning
- on (день недели, дата): on Monday, on 5th May
- at (точное время): at 5 o'clock, at noon

🔴 ФОРМАТЫ ОТВЕТА СТУДЕНТА:
Студент может написать:
- Букву: "a", "b", "c"
- Букву со скобкой: "a)", "b)"
- Последовательность: "1a 2b 3c" или "a, b, c"
- Само слово/фразу: "plays", "is watching"
- Любой другой формат, который имеет смысл, и ответ является правильным

🔴 ПРАВИЛА ПРОВЕРКИ:
- Если все верно → "Да"
- Если ЛЮБАЯ ошибка → "Нет"
- Регистр букв не важен

ФОРМАТ ОТВЕТА:
Если ответ правильный — напиши ровно одно слово 'Да'.
Если ответ неправильный — напиши ровно одно слово 'Нет'.
Ничего больше не добавляй."""
                ),
                HumanMessageSchema(
                    content=(
                        f"Задание: {task.task}\n\n"
                        f"Ответ студента: {answer}\n\n"
                        f"Правильный ответ?"
                    )
                ),
            ]
        )

        normalized = response.content.strip().lower()
        is_correct = normalized == "да"

        return await self.progress_service.save(
            AnswerCreateSchema(
                user_id=user_id,
                topic_id=task.topic.id,
                task=task.task,
                is_correct=is_correct,
            )
        )
