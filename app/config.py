from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Core
    PROJECT_NAME: str = "MassageBot"
    ENV: str = "dev"

    # Локальная дефолтная инфа (не критично, т.к. используем DATABASE_URL из .env)
    POSTGRES_PORT: int = 5433  # твой порт по умолчанию

    # DB (берём из .env → DATABASE_URL)
    database_url: str = Field(env="DATABASE_URL")

    # Telegram
    TELEGRAM_BOT_TOKEN: str = Field(env="TELEGRAM_BOT_TOKEN")

    # PayPal (явные имена переменных окружения)
    paypal_client_id: str | None = Field(default=None, env="PAYPAL_CLIENT_ID")
    paypal_client_secret: str | None = Field(default=None, env="PAYPAL_CLIENT_SECRET")
    paypal_webhook_id: str | None = Field(default=None, env="PAYPAL_WEBHOOK_ID")
    paypal_base_url: str | None = Field(default="https://api-m.sandbox.paypal.com", env="PAYPAL_BASE_URL")

    # Admin
    superadmin_telegram_id: int | None = Field(default=None, env="SUPERADMIN_TELEGRAM_ID")

    # pydantic v2 config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=False,
        populate_by_name=True,
        extra="ignore",
    )

    # Чтобы существующий код, который обращается к settings.DATABASE_URL, продолжал работать:
    @property
    def DATABASE_URL(self) -> str:
        return self.database_url


@lru_cache
def get_settings() -> Settings:
    return Settings()
