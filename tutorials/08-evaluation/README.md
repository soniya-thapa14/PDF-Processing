# Tutorial 08 — Retrieval Evaluation & Quality Metrics

## Goal

Measure how good your retrieval pipeline is. Right now you can ask questions
and get answers — but are the *right* chunks being retrieved? This tutorial
builds a gold-standard evaluation set and computes standard Information
Retrieval (IR) metrics to objectively compare chunking strategies.

By the end of this tutorial you will know:
- How to construct gold-standard evaluation datasets
- How to compute Precision@k, Recall@k, MRR, and NDCG
- How to use an LLM as an automated answer-quality judge
- Which chunking strategy works best for which PDF structure

---

## Why Evaluate Retrieval Separately?

In a RAG system, bad retrieval = bad answers. No matter how powerful your LLM
is, if the retrieved chunks don't contain the answer, the model can't help.

```
                  Retrieval Quality
                  ┌─────────────────────┐
Good retrieval  → │ ✓ Right chunks      │ → Good answer
                  └─────────────────────┘
                  ┌─────────────────────┐
Bad retrieval   → │ ✗ Irrelevant chunks │ → Hallucination or "I don't know"
                  └─────────────────────┘
```

By measuring retrieval quality independently, you can:
1. Diagnose whether problems are in retrieval or generation
2. Compare strategies without expensive LLM calls
3. Iterate quickly on the retrieval side (embeddings, chunking, search)

---

## Evaluation Metrics Explained

### Precision@k

> "Of the k chunks I retrieved, how many are actually relevant?"

```
Precision@5 = (# relevant in top-5) / 5
```

**Example:** You retrieve 5 chunks. 3 are relevant → Precision@5 = 0.6

**When it matters:** High precision means you're not wasting context window
space on irrelevant chunks.

### Recall@k

> "Of all the relevant chunks that exist, how many did I find in the top-k?"

```
Recall@5 = (# relevant found in top-5) / (total # relevant chunks)
```

**Example:** There are 4 relevant chunks total. You find 2 in top-5 → Recall@5 = 0.5

**When it matters:** High recall means you're not missing important information.

### MRR (Mean Reciprocal Rank)

> "How high is the first relevant result?"

```
MRR = 1 / (position of first relevant result)
```

**Example:** First relevant chunk is at position 3 → RR = 1/3 ≈ 0.33

**When it matters:** If only the top-1 or top-2 chunks fit in your prompt,
you need relevant results ranked as high as possible.

### NDCG (Normalized Discounted Cumulative Gain)

> "Are relevant results concentrated at the top of the list?"

NDCG accounts for the *position* of relevant results — finding a relevant
chunk at position 1 is worth more than finding it at position 5.

```
DCG@k = Σ (relevance_i) / log2(i + 1)
NDCG@k = DCG@k / ideal_DCG@k
```

**When it matters:** When you have graded relevance (some chunks are more
relevant than others) or when position strongly affects downstream quality.

---

## The Evaluation Dataset

The file `eval_dataset.json` contains 20 questions, each with:

```json
{
  "id": "q04",
  "question": "What is the scaled dot-product attention formula?",
  "pdf_name": "research_textbook",
  "expected_keywords": ["attention", "softmax", "Q", "K", "V", "sqrt"],
  "gold_chunk_indices": [30, 31],
  "difficulty": "easy"
}
```

| Field | Purpose |
|-------|---------|
| `question` | The natural language question to ask |
| `pdf_name` | Which PDF contains the answer |
| `expected_keywords` | Terms that should appear in retrieved chunks |
| `gold_chunk_indices` | Which chunk indices are considered "relevant" |
| `difficulty` | easy / medium / hard (for stratified analysis) |

The gold-standard chunk indices were determined by manually examining which
chunks from the vector store contain the information needed to answer each
question correctly.

---

## Pipeline

```
Eval Dataset (questions + gold chunks)
      │
      ├──→ eval_retrieval.py
      │      • Retrieve top-k for each question
      │      • Compare retrieved indices to gold indices
      │      • Compute precision, recall, MRR, NDCG
      │
      ├──→ eval_generation.py
      │      • Run full RAG pipeline for each question
      │      • LLM judge scores: faithfulness + correctness
      │
      └──→ compare_strategies.py
             • Run eval_retrieval for each chunking strategy
             • Produce comparison matrix
             • Identify best strategy per PDF type
```

---

## LLM-as-Judge Evaluation

For end-to-end evaluation, we use a second LLM call to judge answer quality:

**Faithfulness (1-5):** Does the answer stick to what the context says?
- 5 = perfectly grounded, every claim traceable to a source
- 1 = hallucinating facts not in the context

**Correctness (1-5):** Does the answer correctly address the question?
- 5 = complete, accurate answer
- 1 = completely wrong or irrelevant

The judge LLM sees only the question and answer (not the context), so it
evaluates whether the answer is independently sensible and accurate.

---

## Files

| File | Purpose | Key Functions |
|------|---------|---------------|
| `eval_dataset.json` | 20 questions with gold-standard sources | — |
| `build_eval_set.py` | Create/annotate evaluation questions | `add_question()`, `sample_chunks_for_annotation()` |
| `eval_retrieval.py` | Retrieval metrics computation | `precision_at_k()`, `recall_at_k()`, `mrr()`, `ndcg_at_k()` |
| `eval_generation.py` | LLM-as-judge scoring | `judge_answer()`, `evaluate_generation()` |
| `compare_strategies.py` | Strategy comparison matrix | `compare_all()`, `print_comparison()` |
| `test_tutorial8.py` | Unit tests for metrics | 9 tests |

---

## Setup

Requires Tutorial 06 (vector store populated) and Tutorial 07 (RAG pipeline).

```bash
# Run retrieval evaluation (no LLM calls needed)
uv run python tutorials/08-evaluation/eval_retrieval.py

# Compare strategies across the eval set
uv run python tutorials/08-evaluation/compare_strategies.py

# LLM-based answer evaluation (requires API key, costs a few cents)
uv run python tutorials/08-evaluation/eval_generation.py --max-questions 5

# Inspect the eval dataset
uv run python tutorials/08-evaluation/build_eval_set.py --stats
```

---

## Tasks

### Task 1: Understand the Eval Dataset
Read `eval_dataset.json`. For each question, mentally check:
- Could this be answered from the named PDF?
- Are the gold chunk indices plausible?

### Task 2: Run Retrieval Evaluation
```bash
uv run python tutorials/08-evaluation/eval_retrieval.py --k 5
```
Look at per-question scores. Which questions have 0 precision? Why?

### Task 3: Compare Chunking Strategies
```bash
uv run python tutorials/08-evaluation/compare_strategies.py --k 5
```
Which strategy wins overall? Does the winner change for different PDF types?

### Task 4: Run LLM-as-Judge
```bash
uv run python tutorials/08-evaluation/eval_generation.py --max-questions 5
```
Compare faithfulness vs correctness scores. Are they correlated?

### Task 5: Expand the Eval Set
Use `build_eval_set.py --add` to add 5 new questions. Re-run evaluation.
Does your new questions change which strategy wins?

### Task 6: Analyze Failure Modes
For questions with precision=0:
- Is the question poorly phrased?
- Is the gold standard wrong?
- Does the embedding model fail on this type of query?

---

## Interpreting Results

| Metric Value | Interpretation |
|-------------|----------------|
| Precision@5 > 0.6 | Good — most retrieved chunks are relevant |
| Precision@5 < 0.2 | Bad — mostly irrelevant chunks in context |
| Recall@5 > 0.8 | Great — finding almost all relevant information |
| Recall@5 < 0.3 | Bad — missing critical chunks |
| MRR > 0.5 | Good — relevant chunk usually in top 2 positions |
| MRR < 0.2 | Bad — relevant chunks buried deep in results |

---

## Common Issues

| Problem | Solution |
|---------|----------|
| All metrics are 0 | Gold chunk indices may not match actual stored chunks — re-examine |
| Strategy comparison all zeros | Chunks stored without strategy labels — check `chunk_strategy` column |
| LLM judge gives all 5s | The judge model may be too lenient — try a more critical prompt |
| Evaluation is slow | Reduce `--max-questions` for generation eval; retrieval eval is fast |

---

## Check Your Work

- [ ] Can compute precision@5 and recall@5 for each strategy
- [ ] MRR scores show which strategy surfaces relevant chunks fastest
- [ ] Strategy comparison produces a clear winner per PDF type
- [ ] LLM-as-judge provides faithfulness + correctness scores
- [ ] Can explain why precision and recall sometimes conflict
- [ ] Have added at least 5 custom questions to the eval set

---

## What's Next

In **Tutorial 09**, we'll address a fundamental weakness of pure vector search:
it fails on exact matches (codes, numbers, specific names). By adding
keyword-based BM25 search and fusing it with vector search, we get the best
of both worlds — and the evaluation set from this tutorial will prove it.
