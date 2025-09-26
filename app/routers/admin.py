from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db

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
