from aiogram import Router, types, F
router = Router()

@router.message(F.text.startswith("/profile"))
async def profile(msg: types.Message):
    await msg.answer("Редактирование профиля (заглушка).")

@router.message(F.text.startswith("/subscribe"))
async def subscribe(msg: types.Message):
    # In real code, hit API /api/v1/masseuse/subscribe and return approval link
    await msg.answer("Ссылка на оплату PayPal (заглушка): https://www.sandbox.paypal.com/checkoutnow?token=FAKE")

@router.message(F.text.startswith("/status"))
async def status(msg: types.Message):
    await msg.answer("Статус подписки: active (заглушка).")
