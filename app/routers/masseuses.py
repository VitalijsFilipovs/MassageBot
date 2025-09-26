from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models

router = APIRouter(prefix="/api/v1", tags=["masseuses"])

@router.get("/masseuses")
def list_masseuses(
    city: str | None = Query(default=None, description="Город (например: Рига)"),
    service: str | None = Query(default=None, description="Код услуги (classic/thai/relax/...)"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(models.Masseuse).filter(models.Masseuse.subscription_status == "active")

    if city:
        q = q.filter(func.lower(models.Masseuse.city) == city.lower())

    if service:
        # services — JSON-массив; contains по списку ищет в массиве
        q = q.filter(models.Masseuse.services.contains([service]))

    q = q.offset(offset).limit(limit)

    items = []
    for m in q.all():
        user = db.query(models.User).get(m.user_id)
        items.append({
            "id": m.user_id,
            "name": user.name_display if user else None,
            "city": m.city,
            "description": m.description,
            "services": m.services,
            "subscription_status": m.subscription_status,
        })
    return {"count": len(items), "items": items}
