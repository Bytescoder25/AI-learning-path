"""RAG pipeline — orchestrates retrieve -> assemble context -> generate.

This is the "context assembly" concept from Week 2 in code: take the user query,
pull the most relevant chunks, build a grounded prompt that tells the model to
answer ONLY from those chunks and cite them, then stream the answer.
"""
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from rag_service.config import get_settings
from rag_service.schemas.search import Citation
from rag_service.services.llm import stream_chat
from rag_service.services.retrieval import similarity_search

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers strictly from the provided context. "
    "If the answer is not in the context, say you don't know. "
    "Cite sources inline as [n] using the numbered context blocks."
)


def _build_context_block(citations: list[Citation]) -> str:
    return "\n\n".join(
        f"[{i + 1}] (source: {c.source})\n{c.content}" for i, c in enumerate(citations)
    )


async def answer_question(
    session: AsyncSession, question: str, history: list[dict] | None = None
) -> tuple[AsyncIterator[str], list[Citation]]:
    """Returns (token_stream, citations). Retrieval happens first (so the caller
    can send citations alongside the streamed answer)."""
    settings = get_settings()
    citations = await similarity_search(session, question, top_k=settings.retrieval_top_k)

    context = _build_context_block(citations)
    user_turn = {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    messages = [*(history or []), user_turn]

    return stream_chat(SYSTEM_PROMPT, messages), citations
