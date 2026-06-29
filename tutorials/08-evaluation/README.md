# Tutorial 08 — Retrieval Evaluation & Quality Metrics

## Goal

Measure how good your retrieval pipeline is. Build a gold-standard evaluation
set, compute standard IR metrics, and compare chunking strategies objectively.

## Key Concepts

1. **Precision@k** — Of the k retrieved chunks, how many are relevant?
2. **Recall@k** — Of all relevant chunks, how many did we retrieve in the top k?
3. **MRR (Mean Reciprocal Rank)** — How high is the first relevant result?
4. **NDCG** — Considers graded relevance and position discount.
5. **LLM-as-Judge** — Use an LLM to score answer correctness and faithfulness.

## Pipeline

```
Eval Dataset (questions + gold chunks)
      │
      ├──→ Retrieval Metrics (precision, recall, MRR per strategy)
      │
      └──→ Generation Metrics (answer correctness via LLM judge)
              │
              ▼
       Strategy Comparison Matrix
```

## Files

| File | Purpose |
|------|---------|
| `eval_dataset.json` | 20-30 questions with gold-standard source chunks |
| `build_eval_set.py` | Helper to create/annotate evaluation questions |
| `eval_retrieval.py` | Compute precision@k, recall@k, MRR, NDCG |
| `eval_generation.py` | LLM-as-judge for answer quality scoring |
| `compare_strategies.py` | Run full eval matrix: strategy × PDF → scores |
| `test_tutorial8.py` | Unit tests |

## Setup

Requires Tutorial 06 (vector store populated) and Tutorial 07 (RAG pipeline).

```bash
# Run the evaluation
uv run python tutorials/08-evaluation/eval_retrieval.py

# Compare strategies
uv run python tutorials/08-evaluation/compare_strategies.py

# LLM-based answer evaluation
uv run python tutorials/08-evaluation/eval_generation.py
```

## Tasks

1. Review `eval_dataset.json` — understand the gold-standard format
2. Run `eval_retrieval.py` — observe precision/recall across strategies
3. Run `compare_strategies.py` — find which strategy works best per PDF
4. Run `eval_generation.py` — see how LLM-as-judge scores answers
5. Add 5 more questions to the eval set and re-run

## Check Your Work

- [ ] Can compute precision@5 and recall@5 for each strategy
- [ ] MRR scores show which strategy surfaces relevant chunks fastest
- [ ] Strategy comparison produces a clear winner per PDF type
- [ ] LLM-as-judge provides faithfulness + correctness scores
