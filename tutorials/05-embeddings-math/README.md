# Tutorial 05 — Math Behind Embeddings

## What you'll build

1. Implement vector math from scratch (dot product, cosine similarity)
2. Build a toy word embedding (skip-gram) using only numpy
3. Use a real embedding model to embed the chunks from Tutorial 03

## Why it matters

Embeddings are the foundation of RAG. If you don't understand what an embedding
*is* — a point in high-dimensional space where nearby points mean similar
things — you can't reason about why retrieval succeeds or fails. Building one
from scratch makes the math concrete.

## Part 1: Math Foundations (`01_math_foundations.py`)

Implement these operations with numpy:
- **Dot product**: geometric meaning and formula
- **Vector magnitude** (L2 norm)
- **Cosine similarity**: `cos(a, b) = dot(a, b) / (|a| * |b|)`
- **Euclidean distance**: `||a - b||`

Then demonstrate:
- Similar sentences should have high cosine similarity
- Unrelated sentences should have low cosine similarity
- Why cosine > Euclidean for comparing text (scale-invariant)

## Part 2: Toy Embedding from Scratch (`02_toy_embedding.py`)

Build a minimal skip-gram word2vec using only numpy:
1. Tokenize a small corpus into a vocabulary
2. Create training pairs: (center_word, context_word) within a window
3. Initialize random weight matrices: W_embed (vocab × dim) and W_context (dim × vocab)
4. Training loop: forward → loss (softmax or negative sampling) → backprop → update
5. After training: the rows of W_embed are your word vectors
6. Test: find nearest neighbors, show that related words cluster

## Part 3: Real Embeddings (`03_real_embeddings.py`)

Use `sentence-transformers` with `all-MiniLM-L6-v2` (384-d, runs on CPU):
1. Load the model
2. Read chunks from Tutorial 03's results
3. Embed each chunk
4. Compute pairwise similarities
5. Show: chunks from the same section are more similar than cross-section chunks
6. Save embeddings as `.npy` files for Tutorial 06

## Your task

Implement the functions marked `# TODO` in each file.

## Run / check your work

```bash
# Part 1:
uv run python tutorials/05-embeddings-math/01_math_foundations.py

# Part 2:
uv run python tutorials/05-embeddings-math/02_toy_embedding.py

# Part 3 (requires Tutorial 03 chunks):
uv run python tutorials/05-embeddings-math/03_real_embeddings.py

# Tests:
uv run pytest tutorials/05-embeddings-math/ -v
```

## Definition of done

- [ ] Part 1: cosine similarity correctly identifies similar/dissimilar pairs
- [ ] Part 2: toy embedding trains and nearest-neighbor lookup works
- [ ] Part 3: real model embeds chunks, saved to `results/`
- [ ] `uv run pytest tutorials/05-embeddings-math/ -v` all green
