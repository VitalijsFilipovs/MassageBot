# MassageBot

Telegram‑бот и API‑платформа для связи клиентов и массажисток с подпиской €10/мес через PayPal Business.

## Быстрый старт (Docker)
```bash
cp .env.example .env
# заполните токены и ключи
docker-compose up --build
```

- API: http://localhost:8000/docs
- Бот: использует токен TELEGRAM_BOT_TOKEN из `.env`

## Технологии
FastAPI + aiogram 3 + PostgreSQL + SQLAlchemy 2 + Alembic + Docker.

## Структура
- `app/` — FastAPI, модели, роуты, сервисы (PayPal), вебхуки
- `bot/` — Telegram‑бот (aiogram 3)
- `logs/` — логи (папка с .gitkeep)
- `migrations/` — для Alembic
- `docker-compose.yml`, `Dockerfile.api`, `Dockerfile.bot`
- `.env.example` — образец переменных окружения

## Лицензия
MIT
