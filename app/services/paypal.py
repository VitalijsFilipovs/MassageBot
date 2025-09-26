import httpx
import base64
import logging
from typing import Any, Dict
from ..config import get_settings

log = logging.getLogger(__name__)
settings = get_settings()

class PayPalClient:
    def __init__(self):
        self.base = settings.PAYPAL_BASE_URL
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET

    async def _get_access_token(self) -> str:
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        async with httpx.AsyncClient(base_url=self.base, timeout=20) as client:
            resp = await client.post(
                "/v1/oauth2/token",
                headers={"Authorization": f"Basic {auth}"},
                data={"grant_type": "client_credentials"},
            )
            resp.raise_for_status()
            data = resp.json()
            return data["access_token"]

    async def create_product_and_plan(self) -> Dict[str, Any]:
        # Minimal stub; usually create Product then Plan (€10/month)
        token = await self._get_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # Create product (idempotency outside scope)
        async with httpx.AsyncClient(base_url=self.base, timeout=20, headers=headers) as client:
            prod = await client.post("/v1/catalogs/products", json={
                "name": "MassageBot Subscription",
                "type": "SERVICE",
                "category": "SOFTWARE"
            })
            prod.raise_for_status()
            product_id = prod.json().get("id")

            plan = await client.post("/v1/billing/plans", json={
                "product_id": product_id,
                "name": "Monthly €10",
                "billing_cycles": [{
                    "frequency": {"interval_unit": "MONTH", "interval_count": 1},
                    "tenure_type": "REGULAR",
                    "sequence": 1,
                    "total_cycles": 0,
                    "pricing_scheme": {"fixed_price": {"value": "10", "currency_code": "EUR"}}
                }],
                "payment_preferences": {"auto_bill_outstanding": True}
            })
            plan.raise_for_status()
            return plan.json()

    async def create_subscription(self, plan_id: str, subscriber_email: str | None = None) -> Dict[str, Any]:
        token = await self._get_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload: Dict[str, Any] = {"plan_id": plan_id}
        if subscriber_email:
            payload["subscriber"] = {"email_address": subscriber_email}
        async with httpx.AsyncClient(base_url=self.base, timeout=20, headers=headers) as client:
            resp = await client.post("/v1/billing/subscriptions", json=payload)
            resp.raise_for_status()
            return resp.json()

def _auth_header():
    s = get_settings()
    creds = f"{s.paypal_client_id}:{s.paypal_client_secret}".encode()
    return {"Authorization": "Basic " + base64.b64encode(creds).decode()}

async def create_subscription(plan_id: str, subscriber_tg_id: int):
    s = get_settings()
    body = {
        "plan_id": plan_id,
        "custom_id": str(subscriber_tg_id),  # чтобы поймать в webhook
        "application_context": {
            "brand_name": "MassageBot",
            "locale": "en-US",
            "return_url": s.API_BASE_URL + "/billing/return",
            "cancel_url": s.API_BASE_URL + "/billing/cancel"
        }
    }
    async with httpx.AsyncClient(base_url=s.paypal_base_url, timeout=20) as client:
        r = await client.post("/v1/billing/subscriptions", json=body, headers=_auth_header())
        r.raise_for_status()
        data = r.json()
        approve = next((l["href"] for l in data["links"] if l["rel"]=="approve"), None)
        return {"subscription_id": data["id"], "approve_url": approve}