"""Shared pytest fixtures.

Integration tests that need a live pgvector DB should be marked and skipped in CI
until a test database is wired up. Unit tests (like chunking) need nothing here.
"""
import pytest


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
