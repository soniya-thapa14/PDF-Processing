# Tutorial 07 — Running LLMs Locally

## Goal

Understand what a Large Language Model (LLM) is, how it works under the hood,
and how to run one locally on your own machine — no API keys, no cloud
dependency, complete privacy.

This tutorial is a prerequisite for Tutorials 08-11 (RAG pipeline). You'll
set up a local LLM that the RAG pipeline uses for generation and evaluation.

---

## What Is a Large Language Model?

An LLM is a neural network trained to predict the next token in a sequence.
Given "The cat sat on the", it predicts "mat" (or "roof", "table", etc.)
with associated probabilities.

What makes them "large":
- **Parameters**: 1B to 400B+ learned weights (numbers)
- **Training data**: Trillions of tokens from books, web, code, papers
- **Compute**: Thousands of GPUs for weeks/months

Despite the simplicity of "predict the next word", this objective at scale
produces systems that can reason, summarize, translate, write code, and
answer questions.

---

## Architecture: The Transformer

Nearly all modern LLMs use the **Transformer** architecture (Vaswani et al., 2017).

### Core Components

```
Input tokens → Embedding → [Transformer Blocks × N] → Output Probabilities

Each Transformer Block:
┌──────────────────────────────────────────────────┐
│  1. Multi-Head Self-Attention                    │
│     • Each token attends to all previous tokens  │
│     • Learns which tokens are relevant to which  │
│                                                  │
│  2. Feed-Forward Network (FFN)                   │
│     • Two linear layers with activation          │
│     • Processes each token independently         │
│                                                  │
│  3. Layer Normalization + Residual Connections   │
│     • Stabilizes training                        │
│     • Allows gradient flow through deep networks │
└──────────────────────────────────────────────────┘
```

### Self-Attention (The Key Innovation)

Self-attention lets each token "look at" every other token to determine context:

```
Attention(Q, K, V) = softmax(QKᵀ / √d_k) × V

where:
  Q = queries (what am I looking for?)
  K = keys (what do I contain?)
  V = values (what information do I provide?)
  d_k = dimension of keys (scaling factor)
```

**Example:** In "The bank by the river was flooded", the word "bank" attends
strongly to "river" and "flooded" to resolve its meaning (riverbank, not
financial bank).

### Autoregressive Generation

LLMs generate text one token at a time:

```
Input:  "What is the capital of France?"
Step 1: predict → "The"
Step 2: predict → "capital"
Step 3: predict → "of"
Step 4: predict → "France"
Step 5: predict → "is"
Step 6: predict → "Paris"
Step 7: predict → "."
Step 8: predict → <end>
```

Each prediction uses ALL previous tokens as context. This is why "context
window" matters — it's how many tokens the model can see at once.

### Key Parameters

| Parameter | Meaning | Typical Range |
|-----------|---------|---------------|
| Parameters (B) | Total learned weights | 1B – 400B |
| Context window | Max tokens in/out | 4K – 128K |
| Layers | Transformer blocks | 24 – 128 |
| Hidden dim | Internal representation size | 2048 – 12288 |
| Attention heads | Parallel attention patterns | 16 – 128 |

---

## Model Families (Overview)

| Family | Creator | Key Models | Open Weight? |
|--------|---------|------------|:------------:|
| GPT | OpenAI | GPT-4o, GPT-4o-mini | No (API only) |
| Claude | Anthropic | Claude 3.5 Sonnet, Claude 3 Haiku | No (API only) |
| Llama | Meta | Llama 3 (8B, 70B, 405B) | Yes |
| Mistral | Mistral AI | Mistral 7B, Mixtral 8x7B | Yes |
| Phi | Microsoft | Phi-3 Mini (3.8B), Phi-3 Medium | Yes |
| Gemma | Google | Gemma 2 (2B, 9B, 27B) | Yes |
| Qwen | Alibaba | Qwen 2.5 (7B, 14B, 72B) | Yes |

**For local use:** Open-weight models (Llama, Mistral, Phi, Gemma, Qwen) can
run on your own hardware. Closed models (GPT, Claude) require API access.

---

## How to Run LLMs Locally

### Option 1: Ollama (Recommended for Beginners)

[Ollama](https://ollama.ai) is the easiest way to run open-weight models locally.
It handles downloading, quantization, and serving with a single command.

#### Install

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai/download
```

#### Pull and Run a Model

```bash
# Download a model (one-time, ~4GB for 7B models)
ollama pull llama3
ollama pull mistral
ollama pull phi3

# Chat interactively
ollama run llama3

# Start the API server (runs in background)
ollama serve
```

#### Use with Our Tutorials

Ollama exposes an OpenAI-compatible API at `http://localhost:11434/v1`:

```bash
export OPENAI_BASE_URL="http://localhost:11434/v1"
export RAG_MODEL="llama3"
# No OPENAI_API_KEY needed for local models
```

That's it — all RAG tutorials (08-11) will now use your local model.

### Option 2: llama.cpp (Maximum Control)

[llama.cpp](https://github.com/ggerganov/llama.cpp) is a C++ inference engine
that runs quantized models with minimal dependencies.

```bash
# Clone and build
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# Download a GGUF model from HuggingFace
# (e.g., TheBloke's quantized models)
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf

# Run the server
./server -m llama-2-7b-chat.Q4_K_M.gguf -c 4096 --port 8080

# Use with our tutorials
export OPENAI_BASE_URL="http://localhost:8080/v1"
export RAG_MODEL="llama-2-7b-chat"
```

### Option 3: LM Studio (GUI)

[LM Studio](https://lmstudio.ai) provides a desktop application with a model
browser, chat interface, and local API server.

1. Download from https://lmstudio.ai
2. Browse and download a model (search for "Llama 3", "Mistral", etc.)
3. Start the local server (Settings → Local Server → Start)
4. Configure:
   ```bash
   export OPENAI_BASE_URL="http://localhost:1234/v1"
   export RAG_MODEL="loaded-model-name"
   ```

### Option 4: vLLM (Production / GPU)

[vLLM](https://github.com/vllm-project/vllm) is a high-throughput inference
engine optimized for GPU serving.

```bash
pip install vllm
vllm serve meta-llama/Meta-Llama-3-8B-Instruct --port 8000

export OPENAI_BASE_URL="http://localhost:8000/v1"
export RAG_MODEL="meta-llama/Meta-Llama-3-8B-Instruct"
```

---

## Hardware Requirements

### RAM / VRAM Needed (Approximate)

| Model Size | Quantization | RAM Required | Quality |
|-----------|-------------|-------------|---------|
| 3B (Phi-3 Mini) | Q4_K_M | ~3 GB | Good for simple tasks |
| 7B (Llama 3, Mistral) | Q4_K_M | ~5 GB | Good all-around |
| 7B | Q8_0 | ~8 GB | Better quality |
| 13B | Q4_K_M | ~9 GB | Better reasoning |
| 70B | Q4_K_M | ~40 GB | Near GPT-4 quality |

**For this tutorial series:** A 7B model with Q4 quantization (5GB RAM) is
sufficient for RAG generation and evaluation tasks.

### What is Quantization?

Full-precision models use 16-bit floats (FP16) — each parameter takes 2 bytes.
A 7B model at FP16 = 14GB. Quantization reduces this:

| Format | Bits per weight | 7B model size | Quality loss |
|--------|:-:|:-:|:-:|
| FP16 | 16 | 14 GB | None (baseline) |
| Q8_0 | 8 | 7 GB | Minimal |
| Q5_K_M | 5 | 5 GB | Small |
| Q4_K_M | 4 | 4 GB | Noticeable on hard tasks |
| Q3_K_M | 3 | 3 GB | Significant |

**Recommendation:** Q4_K_M or Q5_K_M for local RAG — good quality/size tradeoff.

---

## Inference Parameters

When calling an LLM (locally or via API), these parameters control output:

| Parameter | What it does | Typical value |
|-----------|-------------|---------------|
| `temperature` | Randomness (0 = deterministic, 1 = creative) | 0.0–0.3 for RAG |
| `max_tokens` | Maximum response length | 500–2000 |
| `top_p` | Nucleus sampling (probability mass cutoff) | 0.9–0.95 |
| `top_k` | Sample from top-k most likely tokens | 40 |
| `repeat_penalty` | Penalize repeated tokens | 1.1 |

**For RAG specifically:** Use low temperature (0.0–0.2) because we want
factual, deterministic answers grounded in the context, not creative writing.

---

## Configuration for This Tutorial Series

Create a `.env` file in the repo root (or export these in your shell):

```bash
# === LLM Configuration ===
# Choose ONE of the following setups:

# --- Local (Ollama) ---
OPENAI_BASE_URL=http://localhost:11434/v1
RAG_MODEL=llama3

# --- Local (llama.cpp) ---
# OPENAI_BASE_URL=http://localhost:8080/v1
# RAG_MODEL=llama-2-7b-chat

# --- Local (LM Studio) ---
# OPENAI_BASE_URL=http://localhost:1234/v1
# RAG_MODEL=your-model-name

# --- Cloud (OpenAI) ---
# OPENAI_API_KEY=sk-...
# RAG_MODEL=gpt-4o-mini

# --- Cloud (Any OpenAI-compatible) ---
# OPENAI_BASE_URL=https://api.together.xyz/v1
# OPENAI_API_KEY=your-key
# RAG_MODEL=meta-llama/Llama-3-8b-chat-hf
```

The `llm_client.py` in Tutorial 08 reads these environment variables. You can
swap models at any time by changing `RAG_MODEL` — no code changes needed.

---

## Verifying Your Setup

```bash
# Test that Ollama is running
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3", "messages": [{"role": "user", "content": "Say hello"}]}'

# Or use Python
python3 -c "
from openai import OpenAI
client = OpenAI(base_url='http://localhost:11434/v1', api_key='not-needed')
r = client.chat.completions.create(
    model='llama3',
    messages=[{'role': 'user', 'content': 'Say hello in one sentence.'}]
)
print(r.choices[0].message.content)
"
```

---

## Tasks

### Task 1: Install Ollama and Pull a Model
```bash
brew install ollama  # or your platform's method
ollama pull llama3
ollama run llama3    # chat interactively, then Ctrl+D to exit
```

### Task 2: Start the API Server
```bash
ollama serve  # if not already running
```

### Task 3: Verify the OpenAI-Compatible API
```bash
curl http://localhost:11434/v1/models
# Should list your downloaded models
```

### Task 4: Set Environment Variables
```bash
export OPENAI_BASE_URL="http://localhost:11434/v1"
export RAG_MODEL="llama3"
```

### Task 5: Test from Python
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="not-needed")
response = client.chat.completions.create(
    model="llama3",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    temperature=0.0,
)
print(response.choices[0].message.content)
```

### Task 6: Try Different Models
Pull 2-3 models and compare their responses:
```bash
ollama pull mistral
ollama pull phi3
```
Ask the same question to each. Notice differences in style, accuracy, speed.

---

## Theory & References

### The Transformer Architecture

**"Attention Is All You Need"**
Vaswani et al., 2017 (Google Brain)
[arXiv:1706.03762](https://arxiv.org/abs/1706.03762)

The paper that introduced the Transformer. Replaced RNNs with self-attention,
enabling parallel computation and capturing long-range dependencies. Every
modern LLM is built on this architecture.

### Scaling Laws

**"Scaling Laws for Neural Language Models"**
Kaplan et al., 2020 (OpenAI)
[arXiv:2001.08361](https://arxiv.org/abs/2001.08361)

Discovered that model performance improves predictably with more parameters,
more data, and more compute. This power-law relationship is why models keep
getting larger — and why even small models (3B-7B) are remarkably capable
when trained well.

### Open-Weight Models

**"Llama 2: Open Foundation and Fine-Tuned Chat Models"**
Touvron et al., 2023 (Meta AI)
[arXiv:2307.09288](https://arxiv.org/abs/2307.09288)

Meta's release of Llama 2 democratized access to high-quality LLMs. The paper
details pre-training on 2T tokens, RLHF fine-tuning for safety, and
benchmarking against closed models. Llama 3 (2024) extended this further with
improved training recipes and 8B/70B/405B parameter options.

**"Mistral 7B"**
Jiang et al., 2023 (Mistral AI)
[arXiv:2310.06825](https://arxiv.org/abs/2310.06825)

Demonstrated that architectural innovations (grouped-query attention, sliding
window attention) can make a 7B model competitive with much larger models.
Particularly strong for its size on reasoning and code tasks.

### Quantization

**"GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers"**
Frantar et al., 2022
[arXiv:2210.17323](https://arxiv.org/abs/2210.17323)

Shows how to compress models from 16-bit to 4-bit with minimal quality loss.
This is what enables running 7B+ models on consumer hardware (laptops, etc.).

**"QLoRA: Efficient Finetuning of Quantized Language Models"**
Dettmers et al., 2023
[arXiv:2305.14314](https://arxiv.org/abs/2305.14314)

Extends quantization to fine-tuning — you can customize a quantized model
on your own data using a single consumer GPU (24GB).

### Inference Optimization

**"Efficient Memory Management for Large Language Model Serving with PagedAttention"**
Kwon et al., 2023 (UC Berkeley — vLLM)
[arXiv:2309.06180](https://arxiv.org/abs/2309.06180)

The paper behind vLLM. Introduces PagedAttention, which manages KV-cache
memory like virtual memory pages, achieving 2-4x throughput improvement.
This is why vLLM is the standard for production GPU serving.

### OpenAI on Model Selection

**OpenAI — "Models" Documentation**
[platform.openai.com/docs/models](https://platform.openai.com/docs/models)

Explains the tradeoff between model capability, speed, and cost. The same
tradeoff applies to local models: larger = more capable but slower.

### Anthropic on Prompting

**Anthropic — "Prompt Engineering Guide"**
[docs.anthropic.com/en/docs/build-with-claude/prompt-engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)

Best practices for structuring prompts. Directly applicable regardless of
which model you use — the principles (clear instructions, examples,
structured output) are universal.

---

## Check Your Work

- [ ] Ollama (or alternative) installed and running
- [ ] At least one model downloaded and responding to queries
- [ ] `OPENAI_BASE_URL` and `RAG_MODEL` environment variables set
- [ ] Can call the model from Python using the OpenAI SDK
- [ ] Understand the difference between open-weight and closed models
- [ ] Can explain what quantization is and why it matters for local inference
- [ ] Know the hardware requirements for different model sizes

---

## What's Next

In **Tutorial 08**, you'll wire this local LLM into a RAG pipeline: retrieve
relevant chunks from the vector store, format them as context, and generate
grounded answers with source citations. The model you just set up will do
all the generation — no cloud API needed.
