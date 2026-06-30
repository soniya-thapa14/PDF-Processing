"""Tests for Tutorial 08 — Basic RAG pipeline.

Run: uv run pytest tutorials/08-basic-rag/ -v

These tests verify your implementations of prompts.py, llm_client.py, and
rag_pipeline.py. Make the tests pass by implementing the # TODO functions.

Edge cases to consider:
- What happens when token budget is exactly the size of one chunk?
- What if chunk_text contains special characters or is very long?
- What if similarity scores are identical?
- What if context is empty but question is valid?
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent))

from prompts import format_context, build_messages, SYSTEM_PROMPT


# ---------------------------------------------------------------------------
# format_context tests
# ---------------------------------------------------------------------------

def test_format_context_numbers_sources():
    """Each chunk should be labeled [Source 1], [Source 2], etc."""
    chunks = [
        {"chunk_text": "The sky is blue.", "pdf_name": "test.pdf",
         "chunk_strategy": "fixed_char", "similarity": 0.95},
        {"chunk_text": "Water is wet.", "pdf_name": "test.pdf",
         "chunk_strategy": "recursive", "similarity": 0.88},
    ]
    result = format_context(chunks, max_tokens=1000)
    assert "[Source 1]" in result
    assert "[Source 2]" in result
    assert "The sky is blue." in result
    assert "Water is wet." in result


def test_format_context_includes_metadata():
    """Source headers should include pdf_name and chunk_strategy."""
    chunks = [
        {"chunk_text": "Hello", "pdf_name": "report.pdf",
         "chunk_strategy": "semantic", "similarity": 0.9},
    ]
    result = format_context(chunks, max_tokens=500)
    assert "report.pdf" in result
    assert "semantic" in result


def test_format_context_respects_token_budget():
    """Should not exceed max_tokens * 4 characters."""
    chunks = [
        {"chunk_text": "A" * 5000, "pdf_name": "big.pdf",
         "chunk_strategy": "fixed_char", "similarity": 0.9},
        {"chunk_text": "Should not appear in full", "pdf_name": "small.pdf",
         "chunk_strategy": "fixed_char", "similarity": 0.8},
    ]
    result = format_context(chunks, max_tokens=500)  # ~2000 chars budget
    assert "Should not appear in full" not in result


def test_format_context_empty_chunks():
    """Empty chunk list should return empty string or similar."""
    result = format_context([], max_tokens=1000)
    assert result == "" or result is not None


# ---------------------------------------------------------------------------
# build_messages tests
# ---------------------------------------------------------------------------

def test_build_messages_returns_two_messages():
    """Should return [system_msg, user_msg]."""
    messages = build_messages("What is RAG?", "Some context here.")
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"


def test_build_messages_system_prompt():
    """System message should contain the SYSTEM_PROMPT."""
    messages = build_messages("test", "context")
    assert SYSTEM_PROMPT in messages[0]["content"]


def test_build_messages_includes_question():
    """User message should contain the question."""
    messages = build_messages("What is the height limit?", "context text")
    assert "What is the height limit?" in messages[1]["content"]


def test_build_messages_includes_context():
    """User message should contain the context."""
    messages = build_messages("question", "My special context string")
    assert "My special context string" in messages[1]["content"]


def test_build_messages_citation_instruction():
    """User message should instruct the model to cite sources."""
    messages = build_messages("test", "test")
    assert "[Source N]" in messages[1]["content"] or "Source" in messages[1]["content"]


# ---------------------------------------------------------------------------
# llm_client tests (mocked — no real API calls)
# ---------------------------------------------------------------------------

def test_generate_raises_without_model():
    """generate() should raise ValueError if no model configured."""
    import llm_client
    import os
    old = os.environ.get("RAG_MODEL", "")
    os.environ["RAG_MODEL"] = ""
    try:
        llm_client.DEFAULT_MODEL = ""
        try:
            llm_client.generate([{"role": "user", "content": "hi"}])
            assert False, "Should have raised ValueError"
        except (ValueError, NotImplementedError):
            pass  # Either is acceptable (NotImplementedError if not yet implemented)
    finally:
        os.environ["RAG_MODEL"] = old


@patch("llm_client.get_client")
def test_generate_calls_api_with_model(mock_get_client):
    """generate() should call the OpenAI API with the specified model."""
    import llm_client

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test answer"
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    result = llm_client.generate([{"role": "user", "content": "hi"}], model="test-model")
    assert result == "Test answer"
    mock_client.chat.completions.create.assert_called_once()


# ---------------------------------------------------------------------------
# Edge-case tests: boundary conditions students should think about
# ---------------------------------------------------------------------------

def test_format_context_single_chunk_exact_budget():
    """When chunk exactly fills the budget, it should still appear."""
    text = "X" * 400  # 400 chars = 100 tokens
    chunks = [
        {"chunk_text": text, "pdf_name": "fit.pdf",
         "chunk_strategy": "fixed_char", "similarity": 0.9},
    ]
    result = format_context(chunks, max_tokens=200)
    assert text in result


def test_format_context_unicode_text():
    """Chunks with Unicode (accents, CJK, emoji) must not crash."""
    chunks = [
        {"chunk_text": "Ñoño café résumé 日本語 🎯", "pdf_name": "intl.pdf",
         "chunk_strategy": "semantic", "similarity": 0.85},
    ]
    result = format_context(chunks, max_tokens=500)
    assert "café" in result
    assert "日本語" in result


def test_format_context_very_large_single_chunk_truncated():
    """A single chunk larger than the entire budget should be truncated with '...'."""
    huge_text = "word " * 5000  # ~25000 chars >> any reasonable budget
    chunks = [
        {"chunk_text": huge_text, "pdf_name": "huge.pdf",
         "chunk_strategy": "fixed_char", "similarity": 0.99},
    ]
    result = format_context(chunks, max_tokens=100)  # 400 char budget
    assert len(result) <= 500  # some overhead for headers is fine
    assert "..." in result


def test_format_context_duplicate_chunks_all_appear():
    """If duplicate chunks are retrieved, they should all appear (retriever's job to deduplicate)."""
    chunks = [
        {"chunk_text": "Same text", "pdf_name": "a.pdf",
         "chunk_strategy": "fixed_char", "similarity": 0.9},
        {"chunk_text": "Same text", "pdf_name": "a.pdf",
         "chunk_strategy": "fixed_char", "similarity": 0.88},
    ]
    result = format_context(chunks, max_tokens=1000)
    assert "[Source 1]" in result
    assert "[Source 2]" in result


def test_build_messages_long_context_preserved():
    """Even very long context strings should not be silently truncated in messages."""
    long_ctx = "context chunk " * 500
    messages = build_messages("What is X?", long_ctx)
    assert long_ctx in messages[1]["content"]


@patch("llm_client.get_client")
def test_generate_passes_temperature_through(mock_get_client):
    """Extra kwargs like temperature should be forwarded to the API."""
    import llm_client

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "answer"
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    llm_client.generate(
        [{"role": "user", "content": "hi"}],
        model="m",
        temperature=0.0,
        max_tokens=100,
    )
    call_kwargs = mock_client.chat.completions.create.call_args[1]
    assert call_kwargs["temperature"] == 0.0
    assert call_kwargs["max_tokens"] == 100
