"""Bootstrap the database: enable pgvector + create tables.

Dev convenience. For production/schema changes, switch to Alembic migrations.

Run:  python scripts/init_db.py
"""
import asyncio

from sqlalchemy import text

from rag_service.db.models import Base
from rag_service.db.session import engine


async def main() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    print("✅ pgvector enabled and tables created.")


if __name__ == "__main__":
    asyncio.run(main())
