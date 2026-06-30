"""LLM-as-judge evaluation for answer quality."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "08-basic-rag"))

from rag_pipeline import ask
import llm_client


EVAL_DATA = Path(__file__).parent / "eval_dataset.json"

JUDGE_PROMPT = """You are evaluating the quality of a RAG (Retrieval-Augmented Generation) answer.

Given the question and answer, rate the answer on two dimensions:

1. **Faithfulness** (1-5): Does the answer stick to what the context says? (5 = perfectly grounded, 1 = hallucinating)
2. **Correctness** (1-5): Does the answer correctly address the question? (5 = perfect, 1 = completely wrong)

Respond with ONLY a JSON object:
{"faithfulness": <1-5>, "correctness": <1-5>, "reasoning": "<brief explanation>"}
"""


def judge_answer(question: str, answer: str) -> dict:
    """Use an LLM to judge answer quality."""
    messages = [
        {"role": "system", "content": JUDGE_PROMPT},
        {"role": "user", "content": f"Question: {question}\n\nAnswer: {answer}"},
    ]
    response = llm_client.generate(messages, temperature=0.0)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"faithfulness": 0, "correctness": 0, "reasoning": f"Failed to parse: {response[:200]}"}


def evaluate_generation(top_k: int = 5, max_questions: int = None):
    """Run end-to-end evaluation: generate answers and judge them."""
    with open(EVAL_DATA) as f:
        questions = json.load(f)

    if max_questions:
        questions = questions[:max_questions]

    results = []
    total_faithfulness = 0.0
    total_correctness = 0.0

    for q in questions:
        print(f"  Evaluating: {q['id']} — {q['question'][:50]}...")
        rag_result = ask(q["question"], top_k=top_k, pdf_name=q.get("pdf_name"))
        answer = rag_result["answer"]

        scores = judge_answer(q["question"], answer)

        results.append({
            "id": q["id"],
            "question": q["question"],
            "answer": answer[:200],
            **scores,
        })
        total_faithfulness += scores.get("faithfulness", 0)
        total_correctness += scores.get("correctness", 0)

    n = len(results)
    aggregate = {
        "avg_faithfulness": total_faithfulness / n if n else 0,
        "avg_correctness": total_correctness / n if n else 0,
    }

    return {"per_question": results, "aggregate": aggregate}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate answer generation quality")
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--max-questions", type=int, default=5, help="Limit for cost control")
    args = parser.parse_args()

    print(f"Evaluating generation (k={args.k}, max={args.max_questions})...\n")
    results = evaluate_generation(top_k=args.k, max_questions=args.max_questions)

    for r in results["per_question"]:
        print(f"  {r['id']}: faithfulness={r.get('faithfulness', '?')}/5, "
              f"correctness={r.get('correctness', '?')}/5")
        print(f"    Reason: {r.get('reasoning', 'N/A')[:80]}")

    agg = results["aggregate"]
    print(f"\nAverages: faithfulness={agg['avg_faithfulness']:.2f}/5, "
          f"correctness={agg['avg_correctness']:.2f}/5")


if __name__ == "__main__":
    main()
