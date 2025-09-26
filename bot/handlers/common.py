from aiogram import Router, types
from aiogram.filters import CommandStart, Command

router = Router()

@router.message(CommandStart())
async def cmd_start(msg: types.Message):
    text = (
        "Привет! Это MassageBot. Выберите роль:\n"
        "1) Я массажистка — /profile\n"
        "2) Я клиент — /search &lt;город&gt;\n"   # <город> -> &lt;город&gt;
        "Подписка массажистки: €10/мес — /subscribe"
    )
    await msg.answer(text)

@router.message(Command("help"))
async def cmd_help(msg: types.Message):
    await msg.answer(
        "Команды:\n"
        "/profile — профиль\n"
        "/subscribe — подписка\n"
        "/status — статус подписки\n"
        "/search <город> — поиск\n"
        "/fav <id> — избранное"
    )
