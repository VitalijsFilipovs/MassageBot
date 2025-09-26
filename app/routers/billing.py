# app/routers/billing.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Profile, User
from app.config import get_settings
from app.services.paypal import create_subscription
from app.services.notify import notify_admin, notify_user

router = APIRouter(prefix="/billing", tags=["billing"])

class CreateSub(BaseModel):
    tg_id: int
    plan_id: str  # положим в .env PAYPAL_PLAN_ID="..."

@router.post("/create-subscription")
async def create_sub(payload: CreateSub):
    # упростим: одна анкета на пользователя
    db = SessionLocal()
    try:
        u = db.execute(select(User).where(User.tg_id==payload.tg_id)).scalar_one_or_none()
        if not u: raise HTTPException(404, "User not found")
        p = db.execute(select(Profile).where(Profile.user_id==u.id)).scalar_one_or_none()
        if not p: raise HTTPException(404, "Profile not found")

        data = await create_subscription(payload.plan_id, subscriber_tg_id=payload.tg_id)
        # сохраним preliminary subscription_id
        p.subscription_id = data["subscription_id"]
        p.plan_id = payload.plan_id
        db.commit()
        return data
    finally:
        db.close()

# Webhook от PayPal
@router.post("/webhook")
async def paypal_webhook(req: Request):
    # TO DO: verify signature with PAYPAL_WEBHOOK_ID (сделаем позже)
    body = await req.json()
    event_type = body.get("event_type")
    resource = body.get("resource", {})

    # вытащим tg_id
    custom_id = resource.get("custom_id")
    tg_id = int(custom_id) if custom_id and custom_id.isdigit() else None

    db = SessionLocal()
    try:
        if event_type in ("BILLING.SUBSCRIPTION.ACTIVATED", "PAYMENT.SALE.COMPLETED"):
            if tg_id:
                u = db.execute(select(User).where(User.tg_id==tg_id)).scalar_one_or_none()
                if u:
                    p = db.execute(select(Profile).where(Profile.user_id==u.id)).scalar_one_or_none()
                    if p:
                        p.subscription_status = "active"
                        p.is_published = (p.status=="approved")
                        db.commit()
                        notify_user(tg_id, "💚 Подписка активирована. Профиль опубликован!" if p.is_published else "💚 Подписка активна. Ожидает модерации.")
                        notify_admin(f"💶 Оплата/Подписка активна: {p.display_name} (tg_id={tg_id})")

        elif event_type in ("BILLING.SUBSCRIPTION.SUSPENDED","BILLING.SUBSCRIPTION.CANCELLED"):
            if tg_id:
                u = db.execute(select(User).where(User.tg_id==tg_id)).scalar_one_or_none()
                if u:
                    p = db.execute(select(Profile).where(Profile.user_id==u.id)).scalar_one_or_none()
                    if p:
                        p.subscription_status = "suspended" if "SUSPENDED" in event_type else "cancelled"
                        p.is_published = False
                        db.commit()
                        notify_user(tg_id, "⚠️ Подписка приостановлена/отменена. Профиль скрыт.")
                        notify_admin(f"⚠️ Подписка {p.subscription_status}: {p.display_name} (tg_id={tg_id})")

    finally:
        db.close()

    return {"ok": True}
