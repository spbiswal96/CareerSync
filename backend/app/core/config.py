from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "CareerSync API"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma4:e2b"
    max_upload_size_mb: int = 10
    database_url: str = "sqlite:///./careersync.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()