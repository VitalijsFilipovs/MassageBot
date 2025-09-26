# app/main.py
from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(title="MassageBot API")

    # ПОДКЛЮЧАЕМ users
    from app.routers import users
    app.include_router(users.router)
    print("➡️  Router 'users' connected")  # диагностика в консоли

    @app.get("/")
    def root():
        return {"ok": True}

    return app

app = create_app()
