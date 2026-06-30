"""Helper to build and annotate evaluation questions.

This script helps create questions for the eval dataset by:
1. Sampling random chunks from the vector store
2. Generating questions about those chunks using an LLM
3. Recording the gold-standard chunk indices
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "06-vector-store"))
sys.path.insert(0, str(Path(__file__).parent.parent / "08-basic-rag"))

EVAL_DATA = Path(__file__).parent / "eval_dataset.json"


def load_eval_set() -> list[dict]:
    """Load the existing evaluation dataset."""
    if EVAL_DATA.exists():
        with open(EVAL_DATA) as f:
            return json.load(f)
    return []


def save_eval_set(questions: list[dict]):
    """Save the evaluation dataset."""
    with open(EVAL_DATA, "w") as f:
        json.dump(questions, f, indent=2)
    print(f"Saved {len(questions)} questions to {EVAL_DATA}")


def add_question(
    question: str,
    pdf_name: str,
    gold_chunk_indices: list[int],
    expected_keywords: list[str] = None,
    difficulty: str = "medium",
):
    """Add a new question to the evaluation set.

    Args:
        question: the evaluation question
        pdf_name: which PDF the answer comes from
        gold_chunk_indices: indices of relevant chunks
        expected_keywords: keywords expected in correct retrieval
        difficulty: easy/medium/hard
    """
    questions = load_eval_set()
    next_id = f"q{len(questions) + 1:02d}"

    entry = {
        "id": next_id,
        "question": question,
        "pdf_name": pdf_name,
        "expected_keywords": expected_keywords or [],
        "gold_chunk_indices": gold_chunk_indices,
        "difficulty": difficulty,
    }
    questions.append(entry)
    save_eval_set(questions)
    print(f"Added question {next_id}: {question[:60]}...")


def sample_chunks_for_annotation(pdf_name: str = None, n: int = 5):
    """Sample random chunks from the vector store for manual annotation."""
    from store_embeddings import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            where = ""
            params = {"n": n}
            if pdf_name:
                where = "WHERE pdf_name = %(pdf)s"
                params["pdf"] = pdf_name

            cur.execute(f"""
                SELECT chunk_index, pdf_name, chunk_strategy, chunk_text
                FROM pdf_chunks
                {where}
                ORDER BY RANDOM()
                LIMIT %(n)s
            """, params)
            rows = cur.fetchall()

        print(f"\nSampled {len(rows)} chunks for annotation:\n")
        for row in rows:
            print(f"  [{row[0]}] pdf={row[1]}, strategy={row[2]}")
            print(f"       {row[3][:150]}...")
            print()
    finally:
        conn.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build evaluation dataset")
    parser.add_argument("--add", action="store_true", help="Add a question interactively")
    parser.add_argument("--sample", action="store_true", help="Sample chunks for annotation")
    parser.add_argument("--pdf", help="Filter by PDF name")
    parser.add_argument("--stats", action="store_true", help="Show dataset statistics")
    args = parser.parse_args()

    if args.stats:
        questions = load_eval_set()
        print(f"Total questions: {len(questions)}")
        by_pdf = {}
        by_diff = {}
        for q in questions:
            by_pdf[q["pdf_name"]] = by_pdf.get(q["pdf_name"], 0) + 1
            by_diff[q["difficulty"]] = by_diff.get(q["difficulty"], 0) + 1
        print("By PDF:", by_pdf)
        print("By difficulty:", by_diff)
        return

    if args.sample:
        sample_chunks_for_annotation(pdf_name=args.pdf)
        return

    if args.add:
        question = input("Question: ").strip()
        pdf_name = input("PDF name: ").strip()
        indices = input("Gold chunk indices (comma-separated): ").strip()
        gold = [int(x.strip()) for x in indices.split(",")]
        keywords = input("Expected keywords (comma-separated): ").strip()
        kw_list = [k.strip() for k in keywords.split(",")] if keywords else []
        difficulty = input("Difficulty (easy/medium/hard): ").strip() or "medium"
        add_question(question, pdf_name, gold, kw_list, difficulty)
        return

    print("Use --add, --sample, or --stats. See --help for details.")


if __name__ == "__main__":
    main()
