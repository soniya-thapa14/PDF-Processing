"""
Tutorial 08 — Interactive RAG Demo

CLI interface to ask questions about your PDFs.

Usage:
    uv run python tutorials/08-basic-rag/demo.py
    uv run python tutorials/08-basic-rag/demo.py --query "What is attention?"

Implement the functions marked # TODO.
"""

from __future__ import annotations

import argparse


def run_interactive():
    """
    Run an interactive question-answering loop.

    - Prompt the user for a question
    - Call ask() from rag_pipeline
    - Print the answer and source citations
    - Loop until user types 'quit' or 'exit'
    """
    # TODO: Implement interactive loop.
    #   - Print a welcome banner
    #   - Loop: input("Question: ")
    #   - Break on 'quit', 'exit', 'q', empty, EOF, KeyboardInterrupt
    #   - Call ask(question, stream=True)
    #   - If streaming, iterate and print chunks
    #   - Print source citations: pdf_name, strategy, chunk_index, similarity
    raise NotImplementedError("TODO: implement run_interactive")


def run_single(query: str, pdf_name: str = None, top_k: int = 5):
    """
    Answer a single question and exit.

    Print the question, answer, and source list.
    """
    # TODO: Implement single-query mode.
    #   - Call ask(query, top_k=top_k, pdf_name=pdf_name)
    #   - Print question, answer, and sources
    raise NotImplementedError("TODO: implement run_single")


def main():
    parser = argparse.ArgumentParser(description="RAG Demo — Ask questions about your PDFs")
    parser.add_argument("--query", "-q", help="Single question (non-interactive mode)")
    parser.add_argument("--pdf", help="Filter by PDF name")
    parser.add_argument("--top-k", type=int, default=5, help="Number of chunks to retrieve")
    args = parser.parse_args()

    if args.query:
        run_single(args.query, pdf_name=args.pdf, top_k=args.top_k)
    else:
        run_interactive()


if __name__ == "__main__":
    main()
