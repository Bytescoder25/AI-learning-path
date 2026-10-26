"""LLM client — the generation call, with streaming support.

Provider chosen in config. `stream_chat` yields text deltas so the API can
forward them as Server-Sent Events (better perceived latency).
"""
from collections.abc import AsyncIterator

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from rag_service.config import get_settings

settings = get_settings()
_openai = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
_anthropic = (
    AsyncAnthropic(api_key=settings.anthropic_api_key) if settings.anthropic_api_key else None
)


async def stream_chat(system: str, messages: list[dict]) -> AsyncIterator[str]:
    """Stream the model's answer as text chunks.

    `messages` is a list of {"role": "user"|"assistant", "content": str}.
    """
    if settings.llm_provider == "openai":
        if _openai is None:
            raise RuntimeError("OPENAI_API_KEY not set")
        stream = await _openai.chat.completions.create(
            model=settings.chat_model,
            messages=[{"role": "system", "content": system}, *messages],
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    elif settings.llm_provider == "anthropic":
        if _anthropic is None:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        async with _anthropic.messages.stream(
            model=settings.chat_model,
            max_tokens=1024,
            system=system,
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text
    else:
        raise ValueError(f"Unsupported llm provider: {settings.llm_provider}")
