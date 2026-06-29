# Tutorial 10 — Reranking with Cross-Encoders

## Goal

Add a reranking step between retrieval and generation to improve precision.
Retrieve broadly (top-50 via hybrid search), rerank to top-5 with a
cross-encoder, then pass to the LLM.

## Key Concepts

1. **Bi-encoder vs Cross-encoder** — Bi-encoders embed query and doc separately
   (fast, O(1) per doc at query time); cross-encoders process (query, doc)
   together (slow, O(n), but much more accurate).
2. **Two-stage retrieval** — Use fast retrieval for recall, then precise
   reranking for precision.
3. **Cross-encoder model** — `cross-encoder/ms-marco-MiniLM-L-6-v2` scores
   (query, passage) pairs with a relevance score.
4. **Score thresholding** — Filter out low-confidence chunks after reranking.
5. **Latency/quality tradeoff** — More candidates = better quality but slower.

## Two-Stage Architecture

```
Query
  │
  ▼
┌──────────────────┐
│  Stage 1: Recall │  ← hybrid search (T09), retrieve top-50
│  (fast, broad)   │
└────────┬─────────┘
         │  50 candidates
         ▼
┌──────────────────┐
│  Stage 2: Rerank │  ← cross-encoder scores each (query, chunk) pair
│  (slow, precise) │
└────────┬─────────┘
         │  top-5 (high confidence)
         ▼
┌──────────────────┐
│  Generate Answer │  ← LLM with only the best chunks
└──────────────────┘
```

## Files

| File | Purpose |
|------|---------|
| `reranker.py` | Load cross-encoder, score (query, chunk) pairs |
| `two_stage_pipeline.py` | Full pipeline: retrieve → rerank → generate |
| `benchmark.py` | Compare no-rerank vs rerank (latency + quality) |
| `test_tutorial10.py` | Unit tests |

## Setup

```bash
# sentence-transformers already installed (provides CrossEncoder)
# No additional dependencies needed

# Run the two-stage pipeline
uv run python tutorials/10-reranking/two_stage_pipeline.py --query "What is attention?"

# Benchmark
uv run python tutorials/10-reranking/benchmark.py
```

## Tasks

1. Read `reranker.py` — understand bi-encoder vs cross-encoder tradeoff
2. Run `two_stage_pipeline.py` with a query and observe the reranking
3. Run `benchmark.py` — compare quality metrics with and without reranking
4. Experiment: change `retrieve_k` (50, 100, 200) and observe latency/quality
5. Experiment: add a score threshold to filter low-confidence chunks

## Check Your Work

- [ ] Cross-encoder produces different ordering than vector similarity
- [ ] Reranked results are more relevant (visually inspect)
- [ ] Benchmark shows reranking improves precision/MRR on eval set
- [ ] Can explain the latency tradeoff (reranking adds ~200ms for 50 candidates)
