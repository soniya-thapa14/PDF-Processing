"""Tests for Tutorial 07 — Basic RAG pipeline."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent))

from prompts import format_context, build_messages, SYSTEM_PROMPT


def test_format_context_basic():
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
    assert "test.pdf" in result


def test_format_context_respects_token_budget():
    chunks = [
        {"chunk_text": "A" * 5000, "pdf_name": "big.pdf",
         "chunk_strategy": "fixed_char", "similarity": 0.9},
        {"chunk_text": "Should not appear", "pdf_name": "small.pdf",
         "chunk_strategy": "fixed_char", "similarity": 0.8},
    ]
    result = format_context(chunks, max_tokens=500)
    assert "Should not appear" not in result


def test_build_messages_structure():
    messages = build_messages("What is RAG?", "Some context here.")
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "What is RAG?" in messages[1]["content"]
    assert "Some context here." in messages[1]["content"]
    assert SYSTEM_PROMPT in messages[0]["content"]


def test_build_messages_includes_citation_instruction():
    messages = build_messages("test question", "test context")
    assert "[Source N]" in messages[1]["content"]


@patch("llm_client.get_client")
def test_generate_calls_api(mock_get_client):
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
