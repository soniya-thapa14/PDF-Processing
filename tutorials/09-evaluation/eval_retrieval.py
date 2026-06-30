"""Retrieval evaluation metrics: Precision@k, Recall@k, MRR, NDCG."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "08-basic-rag"))
sys.path.insert(0, str(Path(__file__).parent.parent / "06-vector-store"))

from rag_pipeline import retrieve


EVAL_DATA = Path(__file__).parent / "eval_dataset.json"


def precision_at_k(retrieved_indices: list[int], gold_indices: list[int], k: int) -> float:
    """Fraction of top-k retrieved chunks that are relevant."""
    top_k = retrieved_indices[:k]
    relevant = sum(1 for idx in top_k if idx in gold_indices)
    return relevant / k if k > 0 else 0.0


def recall_at_k(retrieved_indices: list[int], gold_indices: list[int], k: int) -> float:
    """Fraction of relevant chunks that appear in top-k."""
    if not gold_indices:
        return 0.0
    top_k = retrieved_indices[:k]
    found = sum(1 for idx in gold_indices if idx in top_k)
    return found / len(gold_indices)


def mrr(retrieved_indices: list[int], gold_indices: list[int]) -> float:
    """Mean Reciprocal Rank: 1/position of first relevant result."""
    for i, idx in enumerate(retrieved_indices, 1):
        if idx in gold_indices:
            return 1.0 / i
    return 0.0


def ndcg_at_k(retrieved_indices: list[int], gold_indices: list[int], k: int) -> float:
    """Normalized Discounted Cumulative Gain at k."""
    import math

    def dcg(indices, golds, k):
        score = 0.0
        for i, idx in enumerate(indices[:k], 1):
            rel = 1.0 if idx in golds else 0.0
            score += rel / math.log2(i + 1)
        return score

    actual_dcg = dcg(retrieved_indices, gold_indices, k)
    ideal_order = gold_indices[:k] + [i for i in retrieved_indices if i not in gold_indices]
    ideal_dcg = dcg(ideal_order, gold_indices, k)
    return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0


def evaluate_retrieval(k: int = 5, strategy: str = None):
    """Run retrieval evaluation across the eval dataset.

    Returns per-question metrics and aggregate scores.
    """
    with open(EVAL_DATA) as f:
        questions = json.load(f)

    results = []
    total_precision = 0.0
    total_recall = 0.0
    total_mrr = 0.0
    total_ndcg = 0.0

    for q in questions:
        chunks = retrieve(
            query=q["question"],
            top_k=k,
            pdf_name=q.get("pdf_name"),
            strategy=strategy,
        )

        retrieved_indices = [c["chunk_index"] for c in chunks]
        gold = q["gold_chunk_indices"]

        p = precision_at_k(retrieved_indices, gold, k)
        r = recall_at_k(retrieved_indices, gold, k)
        m = mrr(retrieved_indices, gold)
        n = ndcg_at_k(retrieved_indices, gold, k)

        results.append({
            "id": q["id"],
            "question": q["question"],
            "precision": p,
            "recall": r,
            "mrr": m,
            "ndcg": n,
            "retrieved": retrieved_indices,
            "gold": gold,
        })

        total_precision += p
        total_recall += r
        total_mrr += m
        total_ndcg += n

    n_questions = len(questions)
    aggregate = {
        "avg_precision": total_precision / n_questions,
        "avg_recall": total_recall / n_questions,
        "avg_mrr": total_mrr / n_questions,
        "avg_ndcg": total_ndcg / n_questions,
    }

    return {"per_question": results, "aggregate": aggregate}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate retrieval quality")
    parser.add_argument("--k", type=int, default=5, help="Top-k for retrieval")
    parser.add_argument("--strategy", help="Filter by chunking strategy")
    args = parser.parse_args()

    print(f"Evaluating retrieval (k={args.k}, strategy={args.strategy or 'all'})...\n")
    results = evaluate_retrieval(k=args.k, strategy=args.strategy)

    print(f"{'ID':<6} {'Precision':>10} {'Recall':>8} {'MRR':>6} {'NDCG':>6}")
    print("-" * 40)
    for r in results["per_question"]:
        print(f"{r['id']:<6} {r['precision']:>10.3f} {r['recall']:>8.3f} {r['mrr']:>6.3f} {r['ndcg']:>6.3f}")

    print("-" * 40)
    agg = results["aggregate"]
    print(f"{'AVG':<6} {agg['avg_precision']:>10.3f} {agg['avg_recall']:>8.3f} "
          f"{agg['avg_mrr']:>6.3f} {agg['avg_ndcg']:>6.3f}")


if __name__ == "__main__":
    main()
