from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Topic(Base):
    __tablename__ = "topics"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(Text())
