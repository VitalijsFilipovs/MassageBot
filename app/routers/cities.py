# app/routers/cities.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

# гибкий импорт get_db под обе раскладки
try:
    from app.utils.database import get_db
except ModuleNotFoundError:
    from app.database import get_db

from app.models import City  # см. модель ниже

router = APIRouter(prefix="/api/v1", tags=["cities"])

@router.get("/cities")
def list_cities(db: Session = Depends(get_db)):
    rows = db.execute(select(City).order_by(City.id)).scalars().all()
    return [
        {
            "id": c.id,
            "slug": c.slug,
            "name_ru": c.name_ru,
            "name_lv": c.name_lv,
            "name_en": c.name_en,
        }
        for c in rows
    ]
