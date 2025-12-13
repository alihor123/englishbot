from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class TaskType(Base):
    __tablename__ = "task_types"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
