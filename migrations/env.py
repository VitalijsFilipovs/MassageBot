# migrations/env.py
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine, pool

# --- PYTHONPATH: migrations/.. -> корень проекта
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- 1) Грузим .env вручную (без зависимостей)
env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    with env_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            # убираем кавычки вокруг значения, если есть
            if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
                v = v[1:-1]
            os.environ.setdefault(k, v)

# --- 2) Берём URL из окружения (или .env, подгруженного выше)
DATABASE_URL = os.getenv("DATABASE_URL")

# на Windows иногда помогает 127.0.0.1 вместо localhost — но у тебя уже ок
# если нужно, можно форснуть замену:
# if DATABASE_URL and "localhost:" in DATABASE_URL:
#     DATABASE_URL = DATABASE_URL.replace("localhost:", "127.0.0.1:")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is empty — Alembic не знает, куда подключаться. Проверь .env")

# Для отладки — увидим, что URL реально подхватился
print("ALEMBIC DATABASE_URL =", DATABASE_URL)

# --- 3) Модели и metadata
from app.models import Base  # noqa: E402  (после исправления sys.path)
from app import models       # noqa: F401  (чтобы Alembic увидел все модели)

target_metadata = Base.metadata


def run_migrations_offline():
    """Генерация SQL без подключения."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Обычный режим — с подключением к БД."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool, future=True)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
