# pyrefly: ignore [missing-import]
from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/api/health")
def health_check():
    logger.info("Health check called")
    return {"status": "ok", "app_name": settings.app_name}