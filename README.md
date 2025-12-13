# 📚 EnglishExerciseBot

Telegram-бот для практики английского языка с поддержкой AI.

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://gitlab.com/wannasleep66/telegram_english_bot.git
cd telegram_english_bot
```

### 2. Настройка переменных окружения

```bash
cp .env.example .env
nano .env
```

**Обязательно заполни:**

```env
# База данных
POSTGRES_HOST=database
POSTGRES_PORT=5432
POSTGRES_USER=english_bot_user
POSTGRES_PASSWORD=Test123!Local          # Для тестов, на проде сделать сложнее
POSTGRES_DB=english_bot_db

# Telegram бот (получить у @BotFather)
TELEGRAM_TOKEN=ВАШ_ТОКЕН_ТЕЛЕГРАМ

# GigaChat API (получить на developers.sber.ru)
AI_TOKEN=ВАШ_AI_ТОКЕН
```

---

## 3. Запуск приложения

### 3.1 Через Docker Compose (рекомендуется)

```bash
docker compose up --build -d
docker compose logs -f application
```

Ожидаемые строки в логах:

```text
✅ Database is ready!
Applying migrations...
Applying seeds...
🚀 Starting bot...
```

После этого:
- Найди бота в Telegram по его username
- Отправь `/start`
- Бот должен ответить

---

## 4. Управление контейнерами

```bash
# Статус контейнеров
docker compose ps

# Остановить бота
docker compose stop

# Запустить снова
docker compose start

# Перезапустить
docker compose restart

# Логи бота
docker compose logs -f application

# Остановить и удалить контейнеры
docker compose down

# Полная очистка (с удалением данных БД)
docker compose down -v
```

---

## 5. Структура проекта

```text
telegram_english_bot/
├── app/                   # Код бота
│   ├── bootstrap.py       # Точка входа
│   ├── handlers/          # Обработчики команд
│   ├── models/            # Модели БД
│   └── cli/               # CLI утилиты (seed и пр.)
├── migrations/            # Миграции Alembic
├── seeds/                 # Начальные данные
├── docker-compose.yml     # Оркестрация контейнеров
├── Dockerfile             # Описание образа приложения
├── entrypoint.sh          # Скрипт, который ждёт БД, крутит миграции и запускает бота
├── pyproject.toml         # Зависимости Poetry
├── .env.example           # Пример настроек окружения
└── README.md              # Этот файл
```
