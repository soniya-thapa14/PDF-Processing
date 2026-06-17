"""
Tutorial 05, Part 2 — Build a Toy Word Embedding from Scratch

Implement a minimal skip-gram word2vec using only numpy.
No PyTorch, no TensorFlow — just linear algebra and gradient descent.

The goal is to understand what happens inside an embedding model:
    1. Words → one-hot vectors → dense vectors via a learned projection
    2. Training: predict context words from center words
    3. Result: similar words end up with similar vectors

Usage:
    uv run python tutorials/05-embeddings-math/02_toy_embedding.py
"""

import numpy as np
from collections import Counter


# ---------------------------------------------------------------------------
# Step 1: Build vocabulary from corpus
# ---------------------------------------------------------------------------

CORPUS = [
    "the king rules the kingdom with wisdom",
    "the queen rules the kingdom with grace",
    "the prince is the son of the king",
    "the princess is the daughter of the queen",
    "a man works in the field",
    "a woman works in the market",
    "the boy plays in the field",
    "the girl plays in the market",
    "the king and queen rule together",
    "the prince and princess are royalty",
    "the man and woman are workers",
    "the boy and girl are children",
    "wisdom and grace are virtues",
    "the kingdom is ruled by royalty",
    "workers labor in the field and market",
    "children play while adults work",
    "the king has a crown of gold",
    "the queen wears a crown of silver",
    "royalty lives in the castle",
    "workers live in the village",
]


def build_vocabulary(corpus: list[str], min_count: int = 1) -> tuple[dict, dict]:
    """
    Build word-to-index and index-to-word mappings from the corpus.

    Returns:
        word2idx: dict mapping word -> integer index
        idx2word: dict mapping integer index -> word
    """
    # TODO: Tokenize all sentences (split by space, lowercase)
    #   Count word frequencies, keep words with count >= min_count
    #   Assign each word a unique integer index
    #   Return both mappings
    raise NotImplementedError("TODO: build vocabulary")


# ---------------------------------------------------------------------------
# Step 2: Generate training pairs
# ---------------------------------------------------------------------------

def generate_training_pairs(
    corpus: list[str],
    word2idx: dict,
    window_size: int = 2,
) -> list[tuple[int, int]]:
    """
    Generate (center_word_idx, context_word_idx) pairs using a sliding window.

    For each word in each sentence, the context words are those within
    `window_size` positions to the left and right.

    Example: "the king rules" with window=1 produces:
        (king, the), (king, rules), (the, king), (rules, king), etc.
    """
    # TODO: For each sentence, for each word position:
    #   - Get center word index
    #   - For each position within ±window_size (not the center itself):
    #     - If valid position, add (center_idx, context_idx) pair
    #   Return list of all pairs
    raise NotImplementedError("TODO: generate training pairs")


# ---------------------------------------------------------------------------
# Step 3: Initialize model
# ---------------------------------------------------------------------------

def initialize_model(vocab_size: int, embedding_dim: int = 20) -> tuple[np.ndarray, np.ndarray]:
    """
    Initialize the two weight matrices:
        W_embed:  (vocab_size, embedding_dim) — input → hidden
        W_context: (embedding_dim, vocab_size) — hidden → output

    Use small random values (Xavier initialization: scale by 1/sqrt(dim)).
    """
    # TODO: Initialize W_embed and W_context with random values
    #   Scale: np.random.randn(...) * (1.0 / np.sqrt(embedding_dim))
    raise NotImplementedError("TODO: initialize model weights")


# ---------------------------------------------------------------------------
# Step 4: Training loop (forward + backward + update)
# ---------------------------------------------------------------------------

def softmax(x: np.ndarray) -> np.ndarray:
    """Numerically stable softmax."""
    # TODO: Implement softmax with the exp-shift trick for numerical stability
    #   shifted = x - max(x)
    #   exp_x = exp(shifted)
    #   return exp_x / sum(exp_x)
    raise NotImplementedError("TODO: implement softmax")


def train_skipgram(
    pairs: list[tuple[int, int]],
    vocab_size: int,
    embedding_dim: int = 20,
    epochs: int = 50,
    learning_rate: float = 0.01,
) -> np.ndarray:
    """
    Train skip-gram model and return the learned embedding matrix.

    For each (center, context) pair:
        1. Forward: hidden = W_embed[center]  (lookup row)
                    scores = W_context.T @ hidden  (dot with all context vectors)
                    probs = softmax(scores)
        2. Loss: cross-entropy = -log(probs[context])
        3. Backward: compute gradients for W_embed and W_context
        4. Update: SGD step

    Returns W_embed after training (each row is a word's embedding).
    """
    # TODO: Implement the training loop.
    #   - Initialize W_embed, W_context
    #   - Shuffle pairs each epoch
    #   - For each pair: forward pass → loss → backward → update
    #   - Print loss every 10 epochs
    #   - Return W_embed
    raise NotImplementedError("TODO: implement skip-gram training")


# ---------------------------------------------------------------------------
# Step 5: Use the trained embeddings
# ---------------------------------------------------------------------------

def find_nearest(word: str, word2idx: dict, idx2word: dict, embeddings: np.ndarray, top_k: int = 5) -> list[tuple[str, float]]:
    """
    Find the top_k most similar words to `word` using cosine similarity.

    Returns list of (word, similarity) tuples, sorted by similarity descending.
    """
    # TODO: Get the embedding for `word`
    #   Compute cosine similarity with all other words
    #   Return top_k most similar (excluding the word itself)
    raise NotImplementedError("TODO: implement nearest neighbor search")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("TOY WORD2VEC (Skip-gram with Softmax)")
    print("=" * 60)

    print("\n1. Building vocabulary...")
    word2idx, idx2word = build_vocabulary(CORPUS)
    print(f"   Vocabulary size: {len(word2idx)} words")

    print("\n2. Generating training pairs...")
    pairs = generate_training_pairs(CORPUS, word2idx, window_size=2)
    print(f"   Training pairs: {len(pairs)}")

    print("\n3. Training skip-gram model...")
    embeddings = train_skipgram(
        pairs, vocab_size=len(word2idx), embedding_dim=20, epochs=100, learning_rate=0.05
    )
    print(f"   Embedding matrix shape: {embeddings.shape}")

    print("\n4. Finding nearest neighbors...")
    test_words = ["king", "queen", "man", "woman", "kingdom"]
    for word in test_words:
        if word in word2idx:
            neighbors = find_nearest(word, word2idx, idx2word, embeddings, top_k=4)
            neighbor_str = ", ".join(f"{w} ({s:.3f})" for w, s in neighbors)
            print(f"   {word:>10} → {neighbor_str}")

    print("\n5. Analogy test: king - man + woman ≈ ?")
    if all(w in word2idx for w in ["king", "man", "woman"]):
        vec = embeddings[word2idx["king"]] - embeddings[word2idx["man"]] + embeddings[word2idx["woman"]]
        from numpy.linalg import norm
        sims = embeddings @ vec / (norm(embeddings, axis=1) * norm(vec) + 1e-8)
        exclude = {word2idx["king"], word2idx["man"], word2idx["woman"]}
        top_idx = [i for i in np.argsort(sims)[::-1] if i not in exclude][:3]
        print(f"   Result: {', '.join(idx2word[i] for i in top_idx)}")
        print(f"   (hoping for 'queen' — on toy data, results vary)")


if __name__ == "__main__":
    main()
