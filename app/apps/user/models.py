from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(), nullable=True)
    username: Mapped[str | None] = mapped_column(String(), nullable=True)
    notifiable: Mapped[bool] = mapped_column(default=False)
    last_activity: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.now, server_default=func.now()
    )
