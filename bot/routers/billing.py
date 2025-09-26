# bot/routers/billing.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
import os, httpx

router = Router()
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
PLAN_ID = os.getenv("PAYPAL_PLAN_ID", "YOUR_PLAN_ID")  # задай в .env

@router.message(F.text.lower().in_({"оплата","оплатить","subscribe","подписка"}))
async def pay_menu(m: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить €10/мес", callback_data="pay:start")]
    ])
    await m.answer("Подписка публикует анкету и держит её активной. Цена: €10/мес.", reply_markup=kb)

@router.callback_query(F.data=="pay:start")
async def pay_start(c: CallbackQuery):
    async with httpx.AsyncClient(base_url=API_BASE, timeout=20) as client:
        r = await client.post("/billing/create-subscription", json={"tg_id": c.from_user.id, "plan_id": PLAN_ID})
        r.raise_for_status()
        data = r.json()
    url = data["approve_url"]
    await c.message.answer(f"Перейдите по ссылке для оплаты:\n{url}")
    await c.answer()
