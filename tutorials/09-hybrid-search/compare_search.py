"""Compare vector, keyword, and hybrid search on the eval dataset."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "07-basic-rag"))
sys.path.insert(0, str(Path(__file__).parent.parent / "08-evaluation"))
sys.path.insert(0, str(Path(__file__).parent))

from rag_pipeline import retrieve as vector_search
from keyword_search import keyword_search
from hybrid_search import hybrid_search
from eval_retrieval import precision_at_k, recall_at_k, mrr


EVAL_DATA = Path(__file__).parent.parent / "08-evaluation" / "eval_dataset.json"


def evaluate_search_method(search_fn, questions, k=5, **kwargs):
    """Evaluate a search function across all questions."""
    total_p, total_r, total_mrr = 0.0, 0.0, 0.0

    for q in questions:
        results = search_fn(query=q["question"], top_k=k, pdf_name=q.get("pdf_name"), **kwargs)
        retrieved_indices = [r["chunk_index"] for r in results]
        gold = q["gold_chunk_indices"]

        total_p += precision_at_k(retrieved_indices, gold, k)
        total_r += recall_at_k(retrieved_indices, gold, k)
        total_mrr += mrr(retrieved_indices, gold)

    n = len(questions)
    return {
        "precision": total_p / n,
        "recall": total_r / n,
        "mrr": total_mrr / n,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compare search methods")
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    with open(EVAL_DATA) as f:
        questions = json.load(f)

    print(f"Comparing search methods (k={args.k}, {len(questions)} questions)...\n")

    methods = {
        "Vector Only": lambda **kw: vector_search(**kw),
        "Keyword Only": lambda **kw: keyword_search(**kw),
        "Hybrid (RRF)": lambda **kw: hybrid_search(**kw),
    }

    print(f"{'Method':<20} {'Precision@k':>12} {'Recall@k':>10} {'MRR':>8}")
    print("=" * 52)

    for name, search_fn in methods.items():
        try:
            scores = evaluate_search_method(search_fn, questions, k=args.k)
            print(f"{name:<20} {scores['precision']:>12.3f} {scores['recall']:>10.3f} "
                  f"{scores['mrr']:>8.3f}")
        except Exception as e:
            print(f"{name:<20} {'ERROR':>12} — {str(e)[:30]}")

    print("=" * 52)


if __name__ == "__main__":
    main()
