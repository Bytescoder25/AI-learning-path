"""Unit tests for chunking — pure logic, no DB or network needed."""
from rag_service.services.chunking import chunk_text


def test_chunk_respects_size_and_overlap():
    text = "abcdefghij" * 20  # 200 chars
    chunks = chunk_text(text, chunk_size=50, overlap=10)
    assert all(len(c) <= 50 for c in chunks)
    assert len(chunks) > 1


def test_empty_text_returns_no_chunks():
    assert chunk_text("   ") == []


def test_overlap_must_be_smaller_than_size():
    import pytest

    with pytest.raises(ValueError):
        chunk_text("hello world", chunk_size=10, overlap=10)
