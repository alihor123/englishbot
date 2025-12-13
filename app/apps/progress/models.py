from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.apps.tasks.models.topic import Topic
from app.apps.user.models import User
from app.db import Base


class Answer(Base):
    __tablename__ = "answers"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    task: Mapped[str] = mapped_column(Text())
    is_correct: Mapped[bool] = mapped_column(Boolean(), default=False)

    user: Mapped[User] = relationship(lazy="joined")
    topic: Mapped[Topic] = relationship(lazy="joined")
