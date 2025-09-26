# app/routers/users.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

# Гибкие импорты под обе структуры проекта
try:
    from app.utils.database import SessionLocal
    from app.utils.models import User
except ModuleNotFoundError:
    from app.database import SessionLocal
    from app.models import User

router = APIRouter(prefix="/api/v1/users", tags=["users"])


class UserCreateOrGet(BaseModel):
    tg_id: int
    locale: str


@router.post("/get_or_create")
def get_or_create_user(payload: UserCreateOrGet):
    db = SessionLocal()
    try:
        user = db.execute(select(User).where(User.tg_id == payload.tg_id)).scalar_one_or_none()
        if not user:
            user = User(
                tg_id=payload.tg_id,
                locale=payload.locale or "ru",
                role="client",
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return {
            "id": user.id,
            "tg_id": user.tg_id,
            "role": user.role,
            "gender": getattr(user, "gender", None),
            "locale": user.locale,
            "phone": getattr(user, "phone", None),
            "share_phone_publicly": getattr(user, "share_phone_publicly", False),
        }
    finally:
        db.close()


class UserPatch(BaseModel):
    role: str | None = None          # client | provider | admin
    gender: str | None = None        # female | male | other
    phone: str | None = None
    share_phone_publicly: bool | None = None
    locale: str | None = None


@router.patch("/{tg_id}")
def patch_user(tg_id: int, payload: UserPatch):
    db = SessionLocal()
    try:
        user = db.execute(select(User).where(User.tg_id == tg_id)).scalar_one_or_none()
        if not user:
            raise HTTPException(404, "User not found")
        for k, v in payload.model_dump(exclude_none=True).items():
            setattr(user, k, v)
        db.commit()
        db.refresh(user)
        return {
            "id": user.id,
            "tg_id": user.tg_id,
            "role": user.role,
            "gender": getattr(user, "gender", None),
            "locale": user.locale,
            "phone": getattr(user, "phone", None),
            "share_phone_publicly": getattr(user, "share_phone_publicly", False),
        }
    finally:
        db.close()
