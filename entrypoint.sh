#!/bin/bash
set -e

echo "=== Starting English Bot ==="


# Ждём готовности базы данных
echo "Waiting for database to be ready..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  echo "Database is unavailable - waiting..."
  sleep 2
done

echo "✅ Database is ready!"


# Применяем миграции
echo "Applying migrations..."
poetry run alembic upgrade head

# Загружаем начальные данные
echo "Applying seeds..."
poetry run python ./app/cli/seed.py

# Запускаем бота
echo "🚀 Starting bot..."
exec "$@"
