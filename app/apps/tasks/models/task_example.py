from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.apps.tasks.models.task_type import TaskType
from app.apps.tasks.models.topic import Topic
from app.db import Base


class TaskExample(Base):
    __tablename__ = "task_examples"

    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"))
    task_type_id: Mapped[int] = mapped_column(
        ForeignKey("task_types.id", ondelete="CASCADE")
    )
    text: Mapped[str] = mapped_column(Text())

    topic: Mapped[Topic] = relationship(lazy="joined")
    task_type: Mapped[TaskType] = relationship(lazy="joined")

    __table_args__ = (
        UniqueConstraint(topic_id, task_type_id, name="topic_task_type_idx"),
    )
