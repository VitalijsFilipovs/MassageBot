# bot/routers/provider_menu.py (фрагмент)
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()
ADMIN_ID = int(os.getenv("SUPERADMIN_TELEGRAM_ID", "0"))

@router.message(Command("write_admin"))
async def write_admin(m: Message):
    await m.answer("Напиши сообщение для админа. Я перешлю.")

@router.message(F.text & ~Command("admin"))
async def forward_to_admin(m: Message):
    # простой вариант: если это не админ и команда не служебная — форвардим админу
    if m.from_user.id != ADMIN_ID and m.text:
        await m.bot.send_message(ADMIN_ID, f"✉️ Сообщение от {m.from_user.id} (@{m.from_user.username or 'no-username'}):\n\n{m.text}")
