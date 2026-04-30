import pandas as pd
import vertexai

from vertexai.preview.evaluation import EvalTask
from app.config import settings


EVAL_INPUT = "evaluation/evaluation_results_input.jsonl"


def main():
    vertexai.init(
        project=settings.PROJECT_ID,
        location=settings.LOCATION,
        experiment="ads-online-agent-evaluation",
    )

    dataset = pd.read_json(EVAL_INPUT, lines=True)

    eval_task = EvalTask(
        dataset=dataset,
        metrics=[
            "fluency",
            "coherence",
            "safety",
            "groundedness",
            "instruction_following",
        ],
    )

    result = eval_task.evaluate(
        experiment_run_name="ads-agent-rag-eval"
    )

    print("Evaluation complete.")
    print(result.summary_metrics)

    if hasattr(result, "metrics_table"):
        print(result.metrics_table)


if __name__ == "__main__":
    main()