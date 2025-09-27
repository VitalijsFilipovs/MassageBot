# bot/api.py
import os
from typing import Any, Dict, Optional
import httpx

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

async def get_or_create_user(tg_id: int, locale: str) -> Dict[str, Any]:
    async with httpx.AsyncClient(base_url=API_BASE, timeout=10) as client:
        r = await client.post("/users/get_or_create", json={"tg_id": tg_id, "locale": locale})
        r.raise_for_status()
        return r.json()

async def update_user(tg_id: int, **fields) -> Dict[str, Any]:
    async with httpx.AsyncClient(base_url=API_BASE, timeout=10) as client:
        r = await client.patch(f"/users/{tg_id}", json=fields)
        r.raise_for_status()
        return r.json()

async def provider_exists(tg_id: int) -> bool:
    async with httpx.AsyncClient(base_url=API_BASE, timeout=10) as client:
        r = await client.get(f"/profiles/by_user/{tg_id}")
        if r.status_code == 404:
            return False
        r.raise_for_status()
        data = r.json()
        return bool(data and data.get("is_published") is not None)

async def list_cities() -> list[dict]:
    async with httpx.AsyncClient(base_url=API_BASE, timeout=10) as client:
        r = await client.get("/cities")
        r.raise_for_status()
        return r.json()

async def search_profiles(city_slug: str, gender: Optional[str], locale: str) -> list[dict]:
    params = {"city": city_slug}
    if gender:
        params["gender"] = gender
    params["locale"] = locale
    async with httpx.AsyncClient(base_url=API_BASE, timeout=15) as client:
        r = await client.get("/profiles", params=params)
        r.raise_for_status()
        return r.json()

async def get_profile(profile_id: int) -> dict:
    async with httpx.AsyncClient(base_url=API_BASE, timeout=10) as client:
        r = await client.get(f"/profiles/{profile_id}")
        r.raise_for_status()
        return r.json()

async def save_profile(tg_id: int, payload: dict):
    async with httpx.AsyncClient(base_url=API_BASE, timeout=20) as client:
        r = await client.post("/api/v1/profiles/upsert", json={"tg_id": tg_id, **payload})
        r.raise_for_status()
        return r.json()