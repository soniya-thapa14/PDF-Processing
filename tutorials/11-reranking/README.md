# Tutorial 11 — Reranking with Cross-Encoders

## Goal

Add a reranking step between retrieval and generation to improve precision.
Retrieve broadly (top-50 via hybrid search), rerank to top-5 with a
cross-encoder, then pass only the best chunks to the LLM.

By the end of this tutorial you will understand:
- The difference between bi-encoders and cross-encoders
- Why two-stage retrieval is the industry standard
- How to use a cross-encoder model for reranking
- The latency/quality tradeoff and how to tune it

---

## The Problem: Retrieval Is Good but Not Perfect

After Tutorial 10, hybrid search gives us solid recall — the relevant chunks
are *somewhere* in the top-50. But the ordering isn't perfect. Chunk #15 might
be more relevant than chunk #3, because vector similarity is an approximation.

If we pass the wrong top-5 to the LLM, we get worse answers. The solution:
use a more powerful (but slower) model to re-order the candidates.

---

## Bi-Encoders vs Cross-Encoders

### Bi-Encoder (what we've been using)

```
Query  →  [Encoder]  →  query_embedding
                                          → cosine_similarity(q, d)
Doc    →  [Encoder]  →  doc_embedding
```

- Encodes query and document **independently**
- Document embeddings computed offline (fast at query time)
- Scalable to millions of documents
- But: can't capture query-document **interactions**

### Cross-Encoder (what we add now)

```
(Query, Doc)  →  [Encoder]  →  relevance_score
```

- Processes query and document **together** in a single forward pass
- Captures rich interactions (word overlap, semantic alignment, context)
- Much more accurate than bi-encoder similarity
- But: must run once per (query, document) pair — O(n) at query time

### The Tradeoff

| Aspect | Bi-Encoder | Cross-Encoder |
|--------|-----------|---------------|
| Speed | O(1) per doc (pre-computed) | O(n) per doc (at query time) |
| Accuracy | Good | Excellent |
| Scale | Millions of docs | Dozens of candidates |
| Use case | First-stage recall | Second-stage precision |

---

## Two-Stage Architecture

The industry standard combines both:

```
Stage 1: RECALL (fast, broad)
├── Hybrid search (vector + BM25)
├── Retrieve top-50 candidates
└── Takes ~20ms

Stage 2: RERANK (slow, precise)
├── Cross-encoder scores each (query, chunk) pair
├── Re-sort by relevance score
├── Return top-5 with highest confidence
└── Takes ~200ms for 50 candidates

Stage 3: GENERATE (LLM)
├── Only sees the best 5 chunks
├── Higher context quality → better answers
└── Takes ~1-3s
```

**Why not just use the cross-encoder directly?**
Scoring 10,000 chunks with a cross-encoder would take ~40 seconds.
But scoring 50 chunks takes ~200ms. The first stage narrows the field cheaply.

---

## The Cross-Encoder Model

We use `cross-encoder/ms-marco-MiniLM-L-6-v2`:
- Trained on MS MARCO passage ranking dataset
- 22M parameters (runs on CPU in ~200ms for 50 pairs)
- Input: (query, passage) pair
- Output: relevance score (higher = more relevant)
- No normalization needed — scores are comparable within a query

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
scores = model.predict([
    ("What is attention?", "The attention mechanism computes..."),
    ("What is attention?", "The weather today is sunny..."),
])
# → [8.2, -4.1]  (first is highly relevant, second is not)
```

---

## Score Thresholding

After reranking, you can filter out low-confidence chunks:

```python
reranked = rerank(query, candidates, top_k=5, threshold=0.0)
```

- Scores > 5: Very high confidence (almost certainly relevant)
- Scores 0-5: Moderate confidence (probably relevant)
- Scores < 0: Low confidence (probably not relevant)

Thresholding prevents low-quality chunks from polluting the context,
even if they're in the "top-5" by default.

---

## Files

| File | Purpose | Key Functions |
|------|---------|---------------|
| `reranker.py` | Load cross-encoder, score (query, chunk) pairs | `get_model()`, `rerank()` |
| `two_stage_pipeline.py` | Full pipeline: retrieve → rerank → generate | `ask_with_reranking()` |
| `benchmark.py` | Compare with/without reranking on eval set | `benchmark()` |
| `test_tutorial10.py` | Unit tests (mocked cross-encoder) | 4 tests |

---

## Setup

```bash
# sentence-transformers is already installed (from Tutorial 05/06)
# The cross-encoder model downloads automatically on first use (~25MB)

# Run the two-stage pipeline
uv run python tutorials/11-reranking/two_stage_pipeline.py \
    --query "What is the scaled dot-product attention formula?"

# Benchmark with vs without reranking
uv run python tutorials/11-reranking/benchmark.py --k 5 --retrieve-k 50
```

---

## Usage Examples

```bash
# Basic query with reranking
uv run python tutorials/11-reranking/two_stage_pipeline.py \
    --query "What are the parking requirements for commercial zones?"

# Wider recall (more candidates to rerank)
uv run python tutorials/11-reranking/two_stage_pipeline.py \
    --query "Explain RLHF" --retrieve-k 100 --rerank-k 5

# With score threshold (only high-confidence chunks)
uv run python tutorials/11-reranking/two_stage_pipeline.py \
    --query "GloVe objective function" --threshold 2.0

# Filter by PDF
uv run python tutorials/11-reranking/two_stage_pipeline.py \
    --query "Revenue growth Q4" --pdf financial_report
```

---

## Tasks

### Task 1: Understand the Cross-Encoder
Read `reranker.py`. Notice:
- The model loads once and is cached (`_model` global)
- `rerank()` creates (query, text) pairs and batch-scores them
- Results are re-sorted by cross-encoder score, not vector similarity

### Task 2: Run a Query and Inspect Reranking
```bash
uv run python tutorials/11-reranking/two_stage_pipeline.py \
    --query "What is attention?" --retrieve-k 20 --rerank-k 5
```
Compare the reranked order to what vector search alone would return.
Are the top chunks different? Better?

### Task 3: Run the Benchmark
```bash
uv run python tutorials/11-reranking/benchmark.py
```
Look at the precision/recall/MRR improvement and the latency cost.
Is the quality gain worth the extra time?

### Task 4: Experiment with retrieve_k
Try different first-stage sizes:
```bash
uv run python tutorials/11-reranking/benchmark.py --retrieve-k 20
uv run python tutorials/11-reranking/benchmark.py --retrieve-k 50
uv run python tutorials/11-reranking/benchmark.py --retrieve-k 100
```
More candidates = better reranking quality, but higher latency.
Where is the sweet spot?

### Task 5: Experiment with Thresholding
Add `--threshold 0.0` to filter out negative-score chunks.
Does this improve answer quality for questions with sparse relevant content?

### Task 6: Understand the Full Pipeline
Trace the complete path from question to answer:
1. Hybrid search (T10) retrieves 50 candidates
2. Cross-encoder reranks to top-5
3. `format_context()` (T07) fits them into the prompt
4. LLM generates the answer with citations

---

## Expected Benchmark Results

Typical improvement from reranking:

```
Method              Precision    Recall      MRR    Latency
=======================================================
Hybrid only             0.420     0.480    0.600      25ms
Hybrid + Rerank         0.560     0.510    0.720     230ms
=======================================================

Reranking impact: precision +0.140, MRR +0.120, latency +205ms
```

The ~200ms latency cost is negligible compared to the 1-3s LLM generation
time, but the quality improvement is significant.

---

## When Reranking Helps Most

| Scenario | Improvement |
|----------|------------|
| Ambiguous queries | High — cross-encoder resolves ambiguity |
| Long documents (many chunks) | High — more noise to filter |
| Exact-match queries | Low — keyword search already finds the right chunk |
| Simple factual queries | Low — vector search is already accurate |
| Multi-hop questions | High — cross-encoder better at relevance nuance |

---

## Common Issues

| Problem | Solution |
|---------|----------|
| First run is slow (~30s) | Model is downloading; subsequent runs use cache |
| Out of memory | Reduce `retrieve_k` or run on a machine with more RAM |
| Reranking doesn't help | Check if your queries are too simple (exact keyword matches) |
| Scores all negative | The chunks may genuinely be irrelevant — check retrieval quality |

---

## Theory & References

### The Foundational Paper on Neural Reranking

**"Passage Re-ranking with BERT"**
Nogueira & Cho, 2019 (NYU)
[arXiv:1901.04085](https://arxiv.org/abs/1901.04085)

The paper that demonstrated BERT-based cross-encoders dramatically outperform
traditional reranking approaches. Key insight: by encoding the query and
passage together, the model can capture fine-grained relevance signals
(word overlap, semantic alignment, negation) that bi-encoders miss.

> "Simply fine-tuning BERT for passage re-ranking achieves state-of-the-art
> results on the MS MARCO passage ranking task."

Results: +12% MRR improvement over the best non-neural approaches.

### Bi-Encoders vs Cross-Encoders

**"Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"**
Reimers & Gurevych, 2019 (UKP Lab, TU Darmstadt)
[arXiv:1908.10084](https://arxiv.org/abs/1908.10084)

The paper that made bi-encoder embeddings practical for retrieval. Before
Sentence-BERT, using BERT for similarity required O(n²) cross-encoder calls.
Sentence-BERT trains a Siamese network to produce fixed-size sentence embeddings
that can be compared with cosine similarity in O(1).

The tradeoff they identify is exactly what motivates two-stage retrieval:
- Bi-encoder: fast (O(1) comparison) but less accurate
- Cross-encoder: accurate but slow (O(n) at query time)
- Solution: use bi-encoder for recall, cross-encoder for precision

### MS MARCO — The Training Dataset

**"MS MARCO: A Human Generated MAchine Reading COmprehension Dataset"**
Bajaj et al., 2016 (Microsoft)
[arXiv:1611.09268](https://arxiv.org/abs/1611.09268)

Our cross-encoder model (`ms-marco-MiniLM-L-6-v2`) is fine-tuned on MS MARCO,
which contains 8.8M passages from web documents and 1M+ real Bing queries with
human-labeled relevant passages. This training data is what teaches the model
to distinguish relevant from irrelevant (query, passage) pairs.

### Two-Stage Retrieval in Production

**"Efficient Passage Retrieval with Hashing for Open-domain Question Answering"**
Yamada et al., 2021
[arXiv:2106.00882](https://arxiv.org/abs/2106.00882)

Demonstrates the two-stage pattern at scale: a hash-based first stage retrieves
thousands of candidates in microseconds, then a cross-encoder reranks the top-k.
The same architecture we implement (vector retrieval → cross-encoder) is used
by Google, Bing, and every major search engine.

**"ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT"**
Khattab & Zaharia, 2020 (Stanford)
[arXiv:2004.12832](https://arxiv.org/abs/2004.12832)

ColBERT proposes a middle ground: token-level interactions that are faster
than full cross-encoding but more accurate than simple dot-product similarity.
A potential future upgrade to our pipeline that preserves the two-stage
architecture while improving both stages.

### Anthropic & OpenAI on Retrieval Quality

**Anthropic — "Give Claude access to information from outside sources"** (2024)
[docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation](https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation)

Anthropic's RAG guide recommends:
- Retrieve more candidates than you ultimately use (our retrieve-50, use-5 pattern)
- Rerank by relevance before stuffing into context
- Quality of retrieval matters more than quantity of context
- "A few highly relevant passages outperform many marginally relevant ones"

**OpenAI — "Optimizing RAG"** (2024)
[cookbook.openai.com/examples/rag_with_reranking](https://cookbook.openai.com/examples/rag_with_reranking)

OpenAI's RAG optimization cookbook directly implements the pattern in this tutorial:
1. Retrieve broadly (embeddings + keyword)
2. Rerank with a cross-encoder
3. Pass only top-k reranked results to the LLM

They report 10-20% improvement in answer accuracy from adding reranking.

### Model Distillation — Why Small Rerankers Work

**"MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers"**
Wang et al., 2020 (Microsoft)
[arXiv:2002.10957](https://arxiv.org/abs/2002.10957)

Our reranker (`MiniLM-L-6-v2`) is a distilled model — a smaller model trained
to replicate a larger teacher model's behavior. With only 22M parameters
(vs BERT's 110M), it runs on CPU in ~4ms per (query, passage) pair while
retaining ~95% of the teacher's accuracy. This makes reranking 50 candidates
practical even without a GPU (~200ms total).

---

## Check Your Work

- [ ] Cross-encoder produces different ordering than vector similarity
- [ ] Reranked results are more relevant (visually inspect top-5)
- [ ] Benchmark shows reranking improves precision and MRR
- [ ] Can explain the latency tradeoff (~200ms for 50 candidates)
- [ ] Understand why two-stage is better than cross-encoder alone
- [ ] Can articulate when reranking helps most vs least

---

## Congratulations!

You've built a complete, production-grade RAG pipeline:

```
PDF → Markdown → Chunks → Embeddings → Vector Store
                                              │
                    ┌───────────────────────────┘
                    ▼
              Hybrid Search (Vector + BM25)
                    │
                    ▼
              Cross-Encoder Reranking
                    │
                    ▼
              LLM Generation with Citations
                    │
                    ▼
              Evaluated with Gold-Standard Metrics
```

This is the same architecture used by production RAG systems at scale.
The main differences in production are:
- More sophisticated chunking (overlapping, document-structure-aware)
- Query understanding/rewriting before retrieval
- Caching layers for repeated queries
- Guardrails and content filtering
- A/B testing different configurations

You now have the foundation to build any of these extensions.
