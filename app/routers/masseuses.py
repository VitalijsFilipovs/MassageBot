# app/routers/masseuses.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func

try:
    from app.utils.database import SessionLocal
except ModuleNotFoundError:
    from app.database import SessionLocal

from app.models import Profile, User

router = APIRouter(prefix="/api/v1/masseuses", tags=["masseuses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def search(
    db: Session = Depends(get_db),
    city_id: int | None = Query(None),
    gender: str | None = Query(None),
    q: str | None = Query(None),
    limit: int = 20,
    offset: int = 0,
):
    cond = [Profile.status == "approved", Profile.is_published == True]
    if city_id:
        cond.append(Profile.city_id == city_id)
    if gender:
        cond.append(Profile.gender == gender)
    if q:
        like = f"%{q}%"
        cond.append((Profile.display_name.ilike(like)) | (Profile.about.ilike(like)))

    items = db.execute(
        select(Profile)
        .where(and_(*cond))
        .order_by(Profile.created_at.desc())
        .limit(limit).offset(offset)
    ).scalars().all()

    total = db.execute(
        select(func.count()).select_from(
            select(Profile.id).where(and_(*cond)).subquery()
        )
    ).scalar_one()

    def to_card(p: Profile):
        tg = db.get(User, p.user_id).tg_id if p.user_id else None
        return {
            "id": p.id,
            "display_name": p.display_name,
            "city_id": p.city_id,
            "gender": p.gender,
            "price_from": p.price_from,
            "photos": (p.photos or [])[:3],
            "about": (p.about or "")[:200],
            "phone_public": p.phone_public if p.share_phone_publicly else None,
            "user_tg_id": tg,
            "status": p.status,
        }

    return {"count": total, "items": [to_card(p) for p in items]}
