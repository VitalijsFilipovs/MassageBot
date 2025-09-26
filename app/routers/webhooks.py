from fastapi import APIRouter, Request, HTTPException
import logging
from ..config import get_settings

router = APIRouter(tags=["webhooks"])
log = logging.getLogger(__name__)
settings = get_settings()

@router.post("/webhooks/paypal")
async def paypal_webhook(request: Request):
    # NOTE: In production, verify transmission signature using PAYPAL_WEBHOOK_ID
    payload = await request.json()
    event_type = payload.get("event_type", "")
    log.info({"msg": "paypal_webhook", "event_type": event_type})

    # TODO: update DB: subscription status, last_payment_at, write PaymentLog
    if event_type == "BILLING.SUBSCRIPTION.ACTIVATED":
        pass
    elif event_type == "BILLING.SUBSCRIPTION.CANCELLED":
        pass
    elif event_type == "PAYMENT.SALE.COMPLETED":
        pass

    return {"ok": True}
