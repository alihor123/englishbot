from pathlib import Path
from typing import Self
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__name__).parent.parent / ".env"


class AiSettings(BaseSettings):
    """
    Настройки llm модели
    """

    token: str
    secure: bool = Field(False)
    model: str = Field("GigaChat-Max")

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_prefix="AI_", extra="ignore"
    )


class CacheSettings(BaseSettings):
    """
    Настройки кеша
    """

    host: str = Field("cache")
    port: str = Field("6370")
    db: str = Field("0")

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_prefix="REDIS_", extra="ignore"
    )


class DatabaseSettings(BaseSettings):
    """
    Настройки базы данных
    """

    user: str = Field(...)
    password: str = Field(...)
    db: str = Field(...)
    port: str = Field("5432")
    host: str = Field("database")

    @property
    def url(self: Self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_prefix="POSTGRES_", extra="ignore"
    )


class TelegramSettings(BaseSettings):
    """
    Настройки телеграм бота
    """

    token: str = Field(...)

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_prefix="TELEGRAM_", extra="ignore"
    )


class AppSettings(BaseSettings):
    """
    Настройки приложения
    """

    database: DatabaseSettings = DatabaseSettings()  # type: ignore
    # cache: CacheSettings() = CacheSettings() #type: ignore
    telegram: TelegramSettings = TelegramSettings()  # type: ignore
