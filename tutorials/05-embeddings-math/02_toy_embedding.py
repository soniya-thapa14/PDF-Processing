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
    word_count = {}
    for sent in corpus:
        for word in sent.lower().split(" "):
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

    word2idx = {}
    idx2word = {}
    counter = 0
    for word in word_count:
        if word_count[word] >= min_count:
            word2idx[word] = counter
            idx2word[counter] = word
            counter += 1

    return word2idx, idx2word


# ---------------------------------------------------------------------------
# Step 2: Generate training pairs
# ---------------------------------------------------------------------------

def generate_training_pairs(
    corpus: list[str],
    word2idx: dict,
    window_size: int = 2,
) -> list[tuple[int, int]]:
    pairs = []
    for sent in corpus:
        words = sent.lower().split(" ")
        for i in range(len(words)):
            center_word = words[i]
            center_idx = word2idx[center_word]
            for j in range(i - window_size, i + window_size + 1):
                if  i == j or j < 0 or j >= len(words):
                    continue
                context_word = words[j]
                context_idx = word2idx[context_word]
                pairs.append((center_idx, context_idx))
    return pairs


# ---------------------------------------------------------------------------
# Step 3: Initialize model
# ---------------------------------------------------------------------------

def initialize_model(vocab_size: int, embedding_dim: int = 20) -> tuple[np.ndarray, np.ndarray]:
    w_embed = np.random.randn(vocab_size, embedding_dim) * (1.0 / np.sqrt(embedding_dim))
    w_context = np.random.randn(embedding_dim, vocab_size) * (1.0 / np.sqrt(embedding_dim))
    return w_embed, w_context


# ---------------------------------------------------------------------------
# Step 4: Training loop (forward + backward + update)
# ---------------------------------------------------------------------------

def softmax(x: np.ndarray) -> np.ndarray:
    shifted = x - max(x)
    exp_x = np.exp(shifted)
    return exp_x / sum(exp_x)


def train_skipgram(
    pairs: list[tuple[int, int]],
    vocab_size: int,
    embedding_dim: int = 20,
    epochs: int = 50,
    learning_rate: float = 0.01,
) -> np.ndarray:
    w_embed, w_context = initialize_model(vocab_size, embedding_dim)
    losses = []
    for epoch in range(epochs):
        losses = []
        for center, context in pairs:
            hidden = w_embed[center]
            scores = w_context.T @ hidden
            probs = softmax(scores)
            loss = -np.log(probs[context])

            d_scores = probs.copy()
            d_scores[context] -= 1
            d_w_context = np.outer(hidden, d_scores)
            d_w_embed = w_context @ d_scores
            w_embed[center] = w_embed[center] - learning_rate * d_w_embed
            w_context = w_context - learning_rate * d_w_context
            losses.append(loss)
        if epoch % 10 == 0:
            print(f"Epoch {epoch}, loss: {np.mean(losses)}")
    return w_embed



# ---------------------------------------------------------------------------
# Step 5: Use the trained embeddings
# ---------------------------------------------------------------------------

def find_nearest(word: str, word2idx: dict, idx2word: dict, embeddings: np.ndarray, top_k: int = 5) -> list[tuple[str, float]]:
    idx = word2idx[word]
    word_vec = embeddings[idx]
    similarities = []
    for w, i in word2idx.items():
        if w == word:
            continue
        word_embed = embeddings[i]
        sim = np.dot(word_vec, word_embed) / (np.linalg.norm(word_vec) * np.linalg.norm(word_embed))
        similarities.append((w, sim))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]

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
