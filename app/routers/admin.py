# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.utils.database import get_db
from app.models import User, Profile

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

# ---- helpers ---------------------------------------------------------------

def ensure_admin(db: Session, tg_id: int) -> User:
    admin = db.execute(select(User).where(User.tg_id == tg_id)).scalar_one_or_none()
    if not admin or admin.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return admin

# ---- simple stubs (как были) ----------------------------------------------

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    rows = db.execute(select(User)).scalars().all()
    return [{"id": u.id, "tg_id": u.tg_id, "role": u.role} for u in rows]

@router.get("/payments")
def payments_report(db: Session = Depends(get_db)):
    return {"total": 0, "currency": "EUR", "items": []}

@router.post("/masseuse/{user_id}/suspend")
def suspend(user_id: int, db: Session = Depends(get_db)):
    # Заглушка
    return {"user_id": user_id, "suspended": True}

# ---- moderation ------------------------------------------------------------

@router.get("/providers/pending")
def list_pending(admin_tg_id: int = Query(...), db: Session = Depends(get_db)):
    ensure_admin(db, admin_tg_id)
    items = (
        db.execute(select(Profile).where(Profile.status == "pending"))
        .scalars()
        .all()
    )
    return [
        {
            "id": p.id,
            "display_name": p.display_name,
            "city_id": p.city_id,
            "user_id": p.user_id,
            "status": p.status,
        }
        for p in items
    ]

class ModerationAction(BaseModel):
    admin_tg_id: int

@router.patch("/providers/{profile_id}/approve")
def approve_profile(
    profile_id: int,
    payload: ModerationAction,
    db: Session = Depends(get_db),
):
    ensure_admin(db, payload.admin_tg_id)
    p = db.get(Profile, profile_id)
    if not p:
        raise HTTPException(404, "Profile not found")
    p.status = "approved"
    p.is_published = True if p.subscription_status == "active" else False
    db.commit()
    return {"ok": True, "profile_id": p.id, "status": p.status}

@router.patch("/providers/{profile_id}/reject")
def reject_profile(
    profile_id: int,
    payload: ModerationAction,
    db: Session = Depends(get_db),
):
    ensure_admin(db, payload.admin_tg_id)
    p = db.get(Profile, profile_id)
    if not p:
        raise HTTPException(404, "Profile not found")
    p.status = "rejected"
    p.is_published = False
    db.commit()
    return {"ok": True, "profile_id": p.id, "status": p.status}

@router.patch("/providers/{profile_id}/freeze")
def freeze_profile(
    profile_id: int,
    payload: ModerationAction,
    db: Session = Depends(get_db),
):
    ensure_admin(db, payload.admin_tg_id)
    p = db.get(Profile, profile_id)
    if not p:
        raise HTTPException(404, "Profile not found")
    p.status = "frozen"
    p.is_published = False
    db.commit()
    return {"ok": True, "profile_id": p.id, "status": p.status}

@router.patch("/providers/{profile_id}/unfreeze")
def unfreeze_profile(
    profile_id: int,
    payload: ModerationAction,
    db: Session = Depends(get_db),
):
    ensure_admin(db, payload.admin_tg_id)
    p = db.get(Profile, profile_id)
    if not p:
        raise HTTPException(404, "Profile not found")
    p.status = "approved"
    p.is_published = True if p.subscription_status == "active" else False
    db.commit()
    return {"ok": True, "profile_id": p.id, "status": p.status}
