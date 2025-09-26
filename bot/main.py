# bot/main.py
import os, asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.aiohttp import AiohttpSession

from bot.routers import onboarding  # твой новый роутер
# при необходимости: from bot.routers import admin_panel, admin_reply, provider_menu, billing

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def on_startup_set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать / Choose language"),
        BotCommand(command="profile", description="Профиль мастера"),
        BotCommand(command="search", description="Поиск мастеров"),
        BotCommand(command="subscribe", description="Подписка €10/мес"),
        BotCommand(command="admin", description="Админ-панель (только для владельца)"),
    ]
    await bot.set_my_commands(commands)

async def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is empty")
    bot = Bot(token=TOKEN, session=AiohttpSession())
    dp = Dispatcher()

    # ВАЖНО: первым — онбординг с /start
    dp.include_router(onboarding.router)
    # затем остальные роутеры:
    # dp.include_router(provider_menu.router)
    # dp.include_router(admin_panel.router)
    # dp.include_router(admin_reply.router)
    # dp.include_router(billing.router)

    await on_startup_set_commands(bot)
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
