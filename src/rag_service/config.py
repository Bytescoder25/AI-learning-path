"""Application settings — loaded from environment / .env (12-factor style).

Everything configurable lives here so nothing is hardcoded. This is the Python
equivalent of a central `config.js` in your Express apps.
"""
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- App ---
    app_name: str = "rag-service"
    environment: Literal["local", "staging", "production"] = "local"
    log_level: str = "INFO"

    # --- Database (pgvector) ---
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/rag",
        description="Async SQLAlchemy DSN for Postgres with the vector extension.",
    )

    # --- Auth ---
    jwt_secret: str = "change-me-in-prod"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # --- LLM / embeddings provider ---
    # Pick your provider once here; services read these, not env directly.
    llm_provider: Literal["openai", "anthropic"] = "openai"
    embedding_provider: Literal["openai"] = "openai"
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    chat_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536  # text-embedding-3-small = 1536

    # --- RAG knobs ---
    chunk_size: int = 800          # characters (start simple)
    chunk_overlap: int = 100
    retrieval_top_k: int = 5

    # --- Reliability ---
    request_timeout_s: float = 30.0
    max_retries: int = 3


@lru_cache
def get_settings() -> Settings:
    """Cached singleton so we parse env once per process."""
    return Settings()
