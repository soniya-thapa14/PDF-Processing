"""
Tutorial 09 — LLM-as-Judge for answer quality evaluation.

Uses a separate LLM call to score RAG answers on faithfulness and correctness.

Usage:
    uv run python tutorials/09-evaluation/eval_generation.py --max-questions 5

Implement the functions marked # TODO.
"""

from __future__ import annotations

import json
from pathlib import Path


EVAL_DATA = Path(__file__).parent / "eval_dataset.json"

JUDGE_PROMPT = """You are evaluating the quality of a RAG (Retrieval-Augmented Generation) answer.

Given the question and answer, rate the answer on two dimensions:

1. **Faithfulness** (1-5): Does the answer stick to what the context says? (5 = perfectly grounded, 1 = hallucinating)
2. **Correctness** (1-5): Does the answer correctly address the question? (5 = perfect, 1 = completely wrong)

Respond with ONLY a JSON object:
{"faithfulness": <1-5>, "correctness": <1-5>, "reasoning": "<brief explanation>"}
"""


def judge_answer(question: str, answer: str) -> dict:
    """
    Use an LLM to judge answer quality on faithfulness and correctness.

    Sends the JUDGE_PROMPT as system message, and question+answer as user message.
    Parses the JSON response.

    Args:
        question: the original question
        answer: the RAG-generated answer

    Returns:
        dict with keys: faithfulness (1-5), correctness (1-5), reasoning (str)
        On parse failure, return scores of 0 with error in reasoning.
    """
    # TODO: Implement LLM-as-judge.
    #   - Import generate from llm_client (Tutorial 08)
    #   - Build messages: system=JUDGE_PROMPT, user=question+answer
    #   - Call generate with temperature=0.0
    #   - Parse JSON response
    #   - Handle JSONDecodeError gracefully
    raise NotImplementedError("TODO: implement judge_answer")


def evaluate_generation(top_k: int = 5, max_questions: int = None) -> dict:
    """
    Run end-to-end evaluation: generate answers and judge them.

    For each question in eval_dataset.json:
    1. Call the RAG pipeline (Tutorial 08's ask())
    2. Judge the answer with judge_answer()
    3. Collect scores

    Args:
        top_k: chunks to retrieve per question
        max_questions: limit number of questions (for cost control)

    Returns:
        dict with 'per_question' (list) and 'aggregate' (avg scores)
    """
    # TODO: Implement generation evaluation.
    #   - Load eval_dataset.json
    #   - For each question, call ask() then judge_answer()
    #   - Collect per-question results
    #   - Compute aggregate averages
    raise NotImplementedError("TODO: implement evaluate_generation")
