from aiogram import Router, types, F
router = Router()

@router.message(F.text.startswith("/admin"))
async def admin_root(msg: types.Message):
    await msg.answer("Админ‑раздел (заглушка). Доступ ограничен.")
