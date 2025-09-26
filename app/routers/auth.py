from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserMe

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/telegram_login", response_model=UserMe)
def telegram_login(db: Session = Depends(get_db)):
    # Stub: validate Telegram auth data (hash, auth_date, etc.)
    # Create or fetch user; return minimal profile
    user = {"id": 1, "role": "client", "name_display": "Demo User"}
    return user
