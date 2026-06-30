"""
Tutorial 08 — LLM Client

Thin wrapper around an OpenAI-compatible LLM API. Supports any endpoint
that implements the chat completions API (OpenAI, Ollama, Together, etc.)

Usage:
    from llm_client import generate
    response = generate([{"role": "user", "content": "Hello"}], model="llama3")

Implement the functions marked # TODO.
"""

from __future__ import annotations

import os
from openai import OpenAI


DEFAULT_MODEL = os.getenv("RAG_MODEL", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", None)


def get_client() -> OpenAI:
    """
    Create an OpenAI client configured from environment variables.

    If OPENAI_BASE_URL is set, use it as the base URL.
    If no OPENAI_API_KEY is set but a base URL exists, use "not-needed" as key.

    Returns:
        Configured OpenAI client instance
    """
    # TODO: Implement client creation.
    #   - Check if BASE_URL is set, pass as base_url kwarg
    #   - If no API key but BASE_URL exists, set api_key="not-needed"
    #   - Return OpenAI(**kwargs)
    raise NotImplementedError("TODO: implement get_client")


def generate(messages: list[dict], model: str = None, stream: bool = False, **kwargs):
    """
    Call the LLM with a list of messages.

    Args:
        messages: [{"role": "system"|"user"|"assistant", "content": "..."}]
        model: model name (defaults to RAG_MODEL env var)
        stream: if True, returns a generator of content deltas
        **kwargs: passed through to API (temperature, max_tokens, etc.)

    Returns:
        If stream=False: the assistant's reply as a string
        If stream=True: a generator yielding content chunks

    Raises:
        ValueError: if no model is configured (env var or parameter)
    """
    # TODO: Implement LLM call.
    #   - Get client via get_client()
    #   - Resolve model (parameter > env var). Raise ValueError if empty.
    #   - Call client.chat.completions.create(model=..., messages=..., stream=...)
    #   - If stream=False: return response.choices[0].message.content
    #   - If stream=True: return a generator that yields delta.content chunks
    raise NotImplementedError("TODO: implement generate")
