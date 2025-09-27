from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.database import get_db     # или SessionLocal, если нужно
from app.utils.schemas import UserMe

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/telegram_login", response_model=UserMe)
def telegram_login(db: Session = Depends(get_db)):
    return {"id": 1, "role": "client", "name_display": "Demo User"}
