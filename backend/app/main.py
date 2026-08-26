from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app_name": settings.app_name}