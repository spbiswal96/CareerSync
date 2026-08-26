from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ollama_service import get_ollama_service

router = APIRouter(prefix="/api/ollama", tags=["ollama"])


class TestPromptRequest(BaseModel):
    prompt: str


@router.post("/test")
async def test_ollama(request: TestPromptRequest):
    service = get_ollama_service()
    result = await service.generate(request.prompt)
    return {"response": result}