# bot/routers/admin_reply.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandObject, Command
import os

router = Router()
ADMIN_ID = int(os.getenv("SUPERADMIN_TELEGRAM_ID", "0"))

@router.message(Command("reply"))
async def reply_cmd(m: Message, command: CommandObject):
    if m.from_user.id != ADMIN_ID:
        return
    # формат: /reply <tg_id> <текст>
    if not command.args:
        return await m.answer("Формат: /reply <tg_id> <текст>")
    try:
        parts = command.args.split(maxsplit=1)
        tg_id = int(parts[0])
        text = parts[1] if len(parts) > 1 else ""
    except Exception:
        return await m.answer("Формат: /reply <tg_id> <текст>")
    if not text:
        return await m.answer("Нет текста сообщения.")
    await m.bot.send_message(tg_id, f"Ответ администратора:\n\n{text}")
    await m.answer("Отправлено.")
