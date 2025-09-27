# app/main.py
from fastapi import FastAPI

def create_app():
    app = FastAPI(title="MassageBot API", version="0.1.0")

    @app.middleware("http")
    async def add_charset_header(request, call_next):
        response = await call_next(request)
        ct = response.headers.get("content-type", "")
        if ct.startswith("application/json") and "charset" not in ct.lower():
            response.headers["content-type"] = "application/json; charset=utf-8"
        return response

    # ВАЖНО: подключаем все имеющиеся роутеры
    from app.routers import auth, masseuses, admin, webhooks, users, cities

    for rtr, name in [
        (auth.router, "auth"),
        (masseuses.router, "masseuses"),
        (admin.router, "admin"),
        (webhooks.router, "webhooks"),
        (users.router, "users"),
    ]:
        app.include_router(rtr)
        print(f"➡️  Router '{name}' connected")

        app.include_router(cities.router)
        print("➡️  Router 'cities' connected")

    @app.get("/")
    def root():
        return {"ok": True}

    return app

app = create_app()
