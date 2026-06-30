"""Benchmark: compare retrieval with and without reranking."""

import json
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "08-basic-rag"))
sys.path.insert(0, str(Path(__file__).parent.parent / "09-evaluation"))
sys.path.insert(0, str(Path(__file__).parent.parent / "10-hybrid-search"))
sys.path.insert(0, str(Path(__file__).parent))

from hybrid_search import hybrid_search
from reranker import rerank
from eval_retrieval import precision_at_k, recall_at_k, mrr


EVAL_DATA = Path(__file__).parent.parent / "09-evaluation" / "eval_dataset.json"


def benchmark(k: int = 5, retrieve_k: int = 50):
    """Compare hybrid-only vs hybrid+rerank on the eval set."""
    with open(EVAL_DATA) as f:
        questions = json.load(f)

    results = {"no_rerank": [], "with_rerank": []}
    timings = {"no_rerank": [], "with_rerank": []}

    for q in questions:
        t0 = time.time()
        candidates = hybrid_search(
            query=q["question"], top_k=retrieve_k, pdf_name=q.get("pdf_name")
        )
        t_hybrid = time.time() - t0

        no_rerank_indices = [c["chunk_index"] for c in candidates[:k]]
        results["no_rerank"].append(no_rerank_indices)
        timings["no_rerank"].append(t_hybrid * 1000)

        t1 = time.time()
        reranked = rerank(q["question"], candidates, top_k=k)
        t_rerank = time.time() - t1

        rerank_indices = [c["chunk_index"] for c in reranked]
        results["with_rerank"].append(rerank_indices)
        timings["with_rerank"].append((t_hybrid + t_rerank) * 1000)

    metrics = {}
    for method in ["no_rerank", "with_rerank"]:
        total_p, total_r, total_mrr = 0.0, 0.0, 0.0
        for i, q in enumerate(questions):
            gold = q["gold_chunk_indices"]
            retrieved = results[method][i]
            total_p += precision_at_k(retrieved, gold, k)
            total_r += recall_at_k(retrieved, gold, k)
            total_mrr += mrr(retrieved, gold)
        n = len(questions)
        avg_time = sum(timings[method]) / n
        metrics[method] = {
            "precision": total_p / n,
            "recall": total_r / n,
            "mrr": total_mrr / n,
            "avg_latency_ms": avg_time,
        }

    return metrics


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

    delta_p = metrics["with_rerank"]["precision"] - metrics["no_rerank"]["precision"]
    delta_mrr = metrics["with_rerank"]["mrr"] - metrics["no_rerank"]["mrr"]
    delta_t = metrics["with_rerank"]["avg_latency_ms"] - metrics["no_rerank"]["avg_latency_ms"]
    print(f"\nReranking impact: precision {delta_p:+.3f}, MRR {delta_mrr:+.3f}, "
          f"latency {delta_t:+.0f}ms")


if __name__ == "__main__":
    main()
