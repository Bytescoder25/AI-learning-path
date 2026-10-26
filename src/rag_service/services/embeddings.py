"""Embeddings — turn text into vectors.

Provider is chosen in config. Retries with backoff wrap the network call so a
transient blip doesn't fail ingestion. Returns one vector per input string.
"""
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from rag_service.config import get_settings

settings = get_settings()
_openai = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None


@retry(stop=stop_after_attempt(settings.max_retries), wait=wait_exponential(min=1, max=10))
async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Batch-embed a list of strings. One API call for the whole batch."""
    if not texts:
        return []
    if settings.embedding_provider == "openai":
        if _openai is None:
            raise RuntimeError("OPENAI_API_KEY not set")
        resp = await _openai.embeddings.create(model=settings.embedding_model, input=texts)
        return [item.embedding for item in resp.data]
    raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")


async def embed_query(text: str) -> list[float]:
    """Convenience: embed a single query string."""
    vectors = await embed_texts([text])
    return vectors[0]
