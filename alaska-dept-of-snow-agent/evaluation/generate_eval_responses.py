import json
from pathlib import Path

from app.agent import generate_answer
from app.model_armor import sanitize_user_prompt, sanitize_model_response


INPUT_FILE = Path("evaluation/evaluation_dataset.jsonl")
OUTPUT_FILE = Path("evaluation/evaluation_results_input.jsonl")


def main():
    rows = []

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            question = item["question"]

            prompt_allowed, sanitized_prompt, _ = sanitize_user_prompt(question)

            if not prompt_allowed:
                answer = "Blocked by Model Armor."
                sources = []
            else:
                result = generate_answer(sanitized_prompt)
                response_allowed, sanitized_response, _ = sanitize_model_response(
                    result["answer"]
                )

                answer = sanitized_response if response_allowed else "Blocked by Model Armor."
                sources = result.get("sources", [])

            rows.append({
                "prompt": question,
                "response": answer,
                "reference": item["reference_answer"],
                "category": item["category"],
                "sources": sources,
            })

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    print(f"Wrote evaluation input to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()