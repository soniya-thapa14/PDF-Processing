"""
Tutorial 11 — Benchmark: compare retrieval with and without reranking.

Measures quality (precision, recall, MRR) and latency for both approaches.

Usage:
    uv run python tutorials/11-reranking/benchmark.py --k 5 --retrieve-k 50

Implement the functions marked # TODO.
"""

from __future__ import annotations

import json
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "08-basic-rag"))
sys.path.insert(0, str(Path(__file__).parent.parent / "09-evaluation"))
sys.path.insert(0, str(Path(__file__).parent.parent / "10-hybrid-search"))
sys.path.insert(0, str(Path(__file__).parent))


EVAL_DATA = Path(__file__).parent.parent / "09-evaluation" / "eval_dataset.json"


def benchmark(k: int = 5, retrieve_k: int = 50) -> dict:
    """
    Compare hybrid-only vs hybrid+rerank on the eval set.

    For each question:
    1. Run hybrid search (time it)
    2. Take top-k without reranking → compute metrics
    3. Rerank the candidates → take top-k → compute metrics (time it)

    Args:
        k: final top-k for both methods
        retrieve_k: first-stage candidate count

    Returns:
        dict mapping method ("no_rerank", "with_rerank") → metrics dict
        with keys: precision, recall, mrr, avg_latency_ms
    """
    # TODO: Implement benchmark.
    #   - Load eval_dataset.json
    #   - Import hybrid_search, rerank, precision_at_k, recall_at_k, mrr
    #   - For each question:
    #     - Time hybrid_search → extract top-k indices → compute metrics
    #     - Time rerank → extract top-k indices → compute metrics
    #   - Average metrics and timings
    #   - Return comparison dict
    raise NotImplementedError("TODO: implement benchmark")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Benchmark reranking")
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--retrieve-k", type=int, default=50)
    args = parser.parse_args()

    print(f"Benchmarking (final k={args.k}, retrieve_k={args.retrieve_k})...\n")
    metrics = benchmark(k=args.k, retrieve_k=args.retrieve_k)

    print(f"{'Method':<18} {'Precision':>10} {'Recall':>8} {'MRR':>6} {'Latency':>10}")
    print("=" * 55)
    for method, m in metrics.items():
        label = "Hybrid only" if method == "no_rerank" else "Hybrid + Rerank"
        print(f"{label:<18} {m['precision']:>10.3f} {m['recall']:>8.3f} "
              f"{m['mrr']:>6.3f} {m['avg_latency_ms']:>8.0f}ms")
    print("=" * 55)


if __name__ == "__main__":
    main()
