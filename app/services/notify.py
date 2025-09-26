# app/services/notify.py
import os, httpx
from app.config import get_settings

def _send_text(chat_id: int, text: str):
    s = get_settings()
    token = os.getenv("TELEGRAM_BOT_TOKEN") or s.TELEGRAM_BOT_TOKEN
    if not token: return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        httpx.post(url, json={"chat_id": chat_id, "text": text})
    except Exception:
        pass

def notify_admin(text: str):
    s = get_settings()
    if s.superadmin_telegram_id:
        _send_text(s.superadmin_telegram_id, text)

def notify_user(tg_id: int, text: str):
    _send_text(tg_id, text)
