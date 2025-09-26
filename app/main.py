from aiogram import Bot, Dispatcher
import asyncio, os

from bot.routers import onboarding  # импортируй router
# dp.include_router(onboarding.router)
from fastapi import FastAPI

async def main():
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(onboarding.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

def create_app() -> FastAPI:
    application = FastAPI(title="MassageBot API")
    # Подключение роутеров (раскомментируй по мере наличия файлов)
    # from app.routers import users, admin, billing, profiles, cities, favorites
    # application.include_router(users.router)
    # application.include_router(admin.router)
    # application.include_router(billing.router)
    # application.include_router(profiles.router)
    # application.include_router(cities.router)
    # application.include_router(favorites.router)

    @application.get("/health")
    def health():
        return {"status": "ok"}

    return application

# ВАЖНО: экспорт переменной с именем app
app = create_app()