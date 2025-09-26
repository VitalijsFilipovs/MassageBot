from aiogram import Router, types, F
import httpx
import os

from app.config import get_settings

router = Router()
settings = get_settings()

# Базовый URL API берем из .env (API_BASE_URL) или из настроек
API_BASE = os.getenv("API_BASE_URL", getattr(settings, "api_base_url", "http://localhost:8000"))

@router.message(F.text.startswith("/search"))
async def search(msg: types.Message):
    # Парсим город: "/search Рига" -> "Рига"
    parts = (msg.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        await msg.answer('Укажи город: <code>/search Рига</code>')
        return

    city = parts[1].strip()

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(f"{API_BASE}/api/v1/masseuses", params={"city": city})
            r.raise_for_status()
            data = r.json()
    except httpx.HTTPError as e:
        await msg.answer(f"API недоступно: {e}")
        return

    # Наш API возвращает {"count": N, "items": [...]}
    items = data.get("items", []) if isinstance(data, dict) else data

    if not items:
        await msg.answer(f"В {city} пока никого не нашли.")
        return

    lines = []
    for it in items[:10]:
        name = it.get("name") or "Без имени"
        city_val = it.get("city") or city
        services = ", ".join(it.get("services") or [])
        uid = it.get("id")
        lines.append(
            f"• <b>{name}</b> — {city_val}\n"
            f"  Услуги: {services}\n"
            f"  /view {uid}"
        )

    await msg.answer("Найдено:\n\n" + "\n\n".join(lines))


@router.message(F.text.startswith("/view"))
async def view(msg: types.Message):
    # Пока без отдельного эндпоинта — оставим заглушку поприличнее
    parts = (msg.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await msg.answer("Использование: /view <id>")
        return
    await msg.answer(f"Профиль массажистки (заглушка). ID: {parts[1]}")


@router.message(F.text.startswith("/fav"))
async def fav(msg: types.Message):
    parts = (msg.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await msg.answer("Использование: /fav <id>")
        return
    await msg.answer("Добавлено в избранное (заглушка).")

