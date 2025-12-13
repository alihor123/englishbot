# Базовый образ Python 3.12
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка менеджер зависимостей
RUN pip install poetry --no-cache-dir

# Копирование файлов зависимостей
COPY ./pyproject.toml ./poetry.lock /app/

# Настройка Poetry и установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копирование всего остального кода
COPY . .

# Права на выполнение entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Переменная окружения для Python
ENV PYTHONPATH="/app"

# Точка входа (стартовый скрипт)
ENTRYPOINT ["./entrypoint.sh"]

# Команда по умолчанию (запуск бота)
CMD ["poetry", "run", "python", "./app/bootstrap.py"]
