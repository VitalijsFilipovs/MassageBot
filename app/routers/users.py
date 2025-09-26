# app/routers/users.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from app.database import SessionLocal
from app.models import User

router = APIRouter(prefix="/users", tags=["users"])

class UserCreateOrGet(BaseModel):
    tg_id: int
    locale: str

@router.post("/get_or_create")
def get_or_create_user(payload: UserCreateOrGet):
    db = SessionLocal()
    try:
        u = db.execute(select(User).where(User.tg_id == payload.tg_id)).scalar_one_or_none()
        if not u:
            u = User(tg_id=payload.tg_id, locale=payload.locale, role="client", is_active=True)
            db.add(u)
            db.commit()
            db.refresh(u)
        return {"id": u.id, "tg_id": u.tg_id, "role": u.role, "locale": u.locale}
    finally:
        db.close()

class UserPatch(BaseModel):
    role: str | None = None
    gender: str | None = None
    phone: str | None = None
    share_phone_publicly: bool | None = None
    locale: str | None = None

@router.patch("/{tg_id}")
def patch_user(tg_id: int, payload: UserPatch):
    db = SessionLocal()
    try:
        u = db.execute(select(User).where(User.tg_id == tg_id)).scalar_one_or_none()
        if not u:
            raise HTTPException(404, "User not found")
        for k, v in payload.model_dump(exclude_none=True).items():
            setattr(u, k, v)
        db.commit()
        db.refresh(u)
        return {"id": u.id, "tg_id": u.tg_id, "role": u.role, "gender": u.gender, "phone": u.phone, "share_phone_publicly": u.share_phone_publicly, "locale": u.locale}
    finally:
        db.close()
