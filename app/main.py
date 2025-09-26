from fastapi import FastAPI
from .utils.logging import configure_logging
from .database import Base, engine
from .routers import auth, masseuses, admin, webhooks

configure_logging()

app = FastAPI(title="MassageBot API")

# Create tables (for PoC; prefer Alembic for prod)
# Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(masseuses.router)
app.include_router(admin.router)
app.include_router(webhooks.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "MassageBot API"}
