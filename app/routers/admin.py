from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Profile
from app.config import get_settings
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    # Stub: return list of users
    return [{"id": 1, "role": "admin"}, {"id": 2, "role": "masseuse"}]

@router.get("/payments")
def payments_report(db: Session = Depends(get_db)):
    # Stub: return summary
    return {"total": 0, "currency": "EUR", "items": []}

@router.post("/masseuse/{user_id}/suspend")
def suspend(user_id: int, db: Session = Depends(get_db)):
    # Stub: flag user as suspended
    return {"user_id": user_id, "suspended": True}

router = APIRouter(prefix="/admin", tags=["admin"])

def ensure_admin(tg_id: int):
    from app.config import get_settings
    if tg_id != get_settings().superadmin_telegram_id:
        raise HTTPException(403, "Forbidden")

@router.get("/providers/pending")
def list_pending(admin_tg_id: int = Query(..., alias="admin_tg_id")):
    ensure_admin(admin_tg_id)
    db = SessionLocal()
    try:
        rows = db.execute(select(Profile).where(Profile.status=="pending")).scalars().all()
        return [dict(id=p.id, display_name=p.display_name, city_id=p.city_id, user_id=p.user_id) for p in rows]
    finally:
        db.close()

class ModerationAction(BaseModel):
    admin_tg_id: int

@router.patch("/providers/{profile_id}/approve")
def approve_profile(profile_id: int, payload: ModerationAction):
    ensure_admin(payload.admin_tg_id)
    db = SessionLocal()
    try:
        p = db.get(Profile, profile_id)
        if not p: raise HTTPException(404, "Profile not found")
        p.status = "approved"
        p.is_published = True if p.subscription_status=="active" else False
        db.commit()
        # уведомим
        from app.services.notify import notify_user
        notify_user(p.user.tg_id, f"✅ Профиль одобрен. Статус подписки: {p.subscription_status}.")
        return {"ok": True}
    finally:
        db.close()

@router.patch("/providers/{profile_id}/reject")
def reject_profile(profile_id: int, payload: ModerationAction):
    ensure_admin(payload.admin_tg_id)
    db = SessionLocal()
    try:
        p = db.get(Profile, profile_id)
        if not p: raise HTTPException(404, "Profile not found")
        p.status = "rejected"
        p.is_published = False
        db.commit()
        from app.services.notify import notify_user
        notify_user(p.user.tg_id, "❌ Профиль отклонён. Проверьте данные и отправьте заново.")
        return {"ok": True}
    finally:
        db.close()

@router.patch("/providers/{profile_id}/freeze")
def freeze_profile(profile_id: int, payload: ModerationAction):
    ensure_admin(payload.admin_tg_id)
    db = SessionLocal()
    try:
        p = db.get(Profile, profile_id)
        if not p: raise HTTPException(404, "Profile not found")
        p.status = "frozen"
        p.is_published = False
        db.commit()
        from app.services.notify import notify_user
        notify_user(p.user.tg_id, "🧊 Профиль заморожен администратором.")
        return {"ok": True}
    finally:
        db.close()

@router.patch("/providers/{profile_id}/unfreeze")
def unfreeze_profile(profile_id: int, payload: ModerationAction):
    ensure_admin(payload.admin_tg_id)
    db = SessionLocal()
    try:
        p = db.get(Profile, profile_id)
        if not p: raise HTTPException(404, "Profile not found")
        p.status = "approved"
        # публикуем только если подписка активна
        p.is_published = True if p.subscription_status=="active" else False
        db.commit()
        from app.services.notify import notify_user
        notify_user(p.user.tg_id, "✅ Профиль разморожен.")
        return {"ok": True}
    finally:
        db.close()