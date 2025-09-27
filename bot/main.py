# bot/main.py
import os, asyncio, logging, importlib
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

logging.basicConfig(level=logging.INFO)

async def set_cmds(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start",     description="Начать / Choose language"),
        BotCommand(command="profile",   description="Профиль мастера"),
        BotCommand(command="search",    description="Поиск мастеров"),
        BotCommand(command="subscribe", description="Подписка €10/мес"),
        BotCommand(command="admin",     description="Админ-панель"),
    ])

async def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is empty")

    bot = Bot(token=token, session=AiohttpSession(),
              default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # онбординг — первым
    from bot.routers import onboarding
    from bot.routers import provider_reg

    dp.include_router(onboarding.router)
    dp.include_router(provider_reg.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_cmds(bot)

    me = await bot.get_me()
    print(f"Bot started: @{me.username} (id={me.id})")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
