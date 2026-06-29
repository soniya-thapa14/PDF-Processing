"""Interactive CLI demo for the RAG pipeline."""

import argparse
import sys

from rag_pipeline import ask


def run_interactive():
    """Run an interactive question-answering loop."""
    print("=" * 60)
    print("  RAG Demo — Ask questions about your PDFs")
    print("  Type 'quit' or 'exit' to stop")
    print("=" * 60)
    print()

    while True:
        try:
            question = input("Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question or question.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        result = ask(question, stream=True)

        if isinstance(result["answer"], str):
            print(f"\nAnswer: {result['answer']}\n")
        else:
            print("\nAnswer: ", end="", flush=True)
            for chunk in result["answer"]:
                print(chunk, end="", flush=True)
            print("\n")

        if result["sources"]:
            print(f"  [{result['context_used']} chunks used]")
            for i, src in enumerate(result["sources"], 1):
                print(f"  Source {i}: {src['pdf_name']} / {src['chunk_strategy']} "
                      f"(chunk {src['chunk_index']}, similarity={src['similarity']:.3f})")
            print()


def run_single(query: str, pdf_name: str = None, top_k: int = 5):
    """Answer a single question and exit."""
    result = ask(query, top_k=top_k, pdf_name=pdf_name)

    print(f"Question: {query}\n")
    print(f"Answer: {result['answer']}\n")

    if result["sources"]:
        print("Sources:")
        for i, src in enumerate(result["sources"], 1):
            print(f"  [{i}] {src['pdf_name']} / {src['chunk_strategy']} "
                  f"(chunk {src['chunk_index']}, sim={src['similarity']:.3f})")
            print(f"      {src['chunk_text'][:100]}...")


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
