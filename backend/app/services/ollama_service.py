import httpx

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class OllamaService:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model

    async def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": False}

        async with httpx.AsyncClient(timeout=60.0) as client:
            logger.info("Sending request to Ollama model=%s", self.model)
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["response"]


def get_ollama_service() -> OllamaService:
    return OllamaService()