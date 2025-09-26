# bot/routers/admin_panel.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import os, httpx

router = Router()
SUPERADMIN = int(os.getenv("SUPERADMIN_TELEGRAM_ID", "0"))
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

def is_admin(message: Message) -> bool:
    return message.from_user and message.from_user.id == SUPERADMIN

@router.message(Command("admin"))
async def admin_menu(m: Message, state: FSMContext):
    if not is_admin(m):
        return
    kb = [
        [("⏳ На модерации", "adm:pending")],
        [("✅ Активные", "adm:active"), ("🧊 Замороженные", "adm:frozen")],
    ]
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t, callback_data=d)] for t, d in kb
    ])
    await m.answer("Админ-панель:", reply_markup=markup)

@router.callback_query(F.data=="adm:pending")
async def adm_pending(c: CallbackQuery):
    if c.from_user.id != SUPERADMIN:
        return await c.answer("Нет доступа", show_alert=True)
    async with httpx.AsyncClient(base_url=API_BASE, timeout=15) as client:
        r = await client.get("/admin/providers/pending", params={"admin_tg_id": SUPERADMIN})
        r.raise_for_status()
        items = r.json()
    if not items:
        await c.message.answer("Нет анкет на модерации.")
        return await c.answer()
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    for it in items[:10]:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"adm:approve:{it['id']}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"adm:reject:{it['id']}"),
            InlineKeyboardButton(text="👁 Профиль", callback_data=f"adm:view:{it['id']}"),
        ]])
        await c.message.answer(f"#{it['id']} {it['display_name']}", reply_markup=kb)
    await c.answer()

@router.callback_query(F.data.startswith("adm:approve:"))
async def adm_approve(c: CallbackQuery):
    if c.from_user.id != SUPERADMIN:
        return await c.answer("Нет доступа", show_alert=True)
    pid = int(c.data.split(":")[2])
    async with httpx.AsyncClient(base_url=API_BASE, timeout=10) as client:
        r = await client.patch(f"/admin/providers/{pid}/approve", json={"admin_tg_id": SUPERADMIN})
        r.raise_for_status()
    await c.message.edit_text(f"✅ Одобрено #{pid}")
    await c.answer()

@router.callback_query(F.data.startswith("adm:reject:"))
async def adm_reject(c: CallbackQuery):
    if c.from_user.id != SUPERADMIN:
        return await c.answer("Нет доступа", show_alert=True)
    pid = int(c.data.split(":")[2])
    async with httpx.AsyncClient(base_url=API_BASE, timeout=10) as client:
        r = await client.patch(f"/admin/providers/{pid}/reject", json={"admin_tg_id": SUPERADMIN})
        r.raise_for_status()
    await c.message.edit_text(f"❌ Отклонено #{pid}")
    await c.answer()
