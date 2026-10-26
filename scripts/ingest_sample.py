"""Ingest a text file into the RAG store (manual test of the write path).

Run:  python scripts/ingest_sample.py data/samples/sample.txt
"""
import asyncio
import sys

from rag_service.db.session import SessionLocal
from rag_service.services.ingestion import ingest_document


async def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        content = f.read()
    async with SessionLocal() as session:
        doc = await ingest_document(session, source=path, content=content)
        await session.commit()
        print(f"✅ Ingested {doc.source} -> {len(doc.chunks)} chunks (doc id: {doc.id})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python scripts/ingest_sample.py <path-to-text-file>")
        raise SystemExit(1)
    asyncio.run(main(sys.argv[1]))
