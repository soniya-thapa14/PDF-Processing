"""Compare retrieval quality across chunking strategies."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from eval_retrieval import evaluate_retrieval


STRATEGIES = [
    "chunk_fixed_char",
    "chunk_fixed_token",
    "chunk_recursive",
    "chunk_by_headers",
    "chunk_semantic",
    "chunk_table_aware",
    "chunk_sliding_window",
]


def compare_all(k: int = 5):
    """Run evaluation for each strategy and produce comparison matrix."""
    results = {}

    for strategy in STRATEGIES:
        print(f"  Evaluating strategy: {strategy}...")
        try:
            eval_result = evaluate_retrieval(k=k, strategy=strategy)
            results[strategy] = eval_result["aggregate"]
        except Exception as e:
            print(f"    Skipped (error: {e})")
            results[strategy] = {
                "avg_precision": 0, "avg_recall": 0,
                "avg_mrr": 0, "avg_ndcg": 0,
            }

    return results


def print_comparison(results: dict):
    """Print a formatted comparison table."""
    print(f"\n{'Strategy':<25} {'Precision@k':>12} {'Recall@k':>10} {'MRR':>8} {'NDCG':>8}")
    print("=" * 65)

    sorted_results = sorted(results.items(), key=lambda x: x[1]["avg_precision"], reverse=True)
    for strategy, scores in sorted_results:
        print(f"{strategy:<25} {scores['avg_precision']:>12.3f} {scores['avg_recall']:>10.3f} "
              f"{scores['avg_mrr']:>8.3f} {scores['avg_ndcg']:>8.3f}")

    print("=" * 65)
    best = sorted_results[0]
    print(f"\nBest strategy: {best[0]} (precision={best[1]['avg_precision']:.3f})")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compare chunking strategies")
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    print(f"Comparing strategies (k={args.k})...\n")
    results = compare_all(k=args.k)
    print_comparison(results)


if __name__ == "__main__":
    main()
