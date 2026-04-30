from datetime import datetime, timezone
from google.cloud import bigquery

from app.config import settings
from typing import List, Optional



def log_chat_interaction(
    question: str,
    answer: str,
    status: str,
    sources: Optional[List[str]] = None,
) -> None:
    """
    Logs prompt/response activity to BigQuery.
    """
    client = bigquery.Client(project=settings.PROJECT_ID)

    table_id = (
        f"{settings.PROJECT_ID}."
        f"{settings.LOG_DATASET}."
        f"{settings.LOG_TABLE}"
    )

    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_query": question,
        "response": answer,
        "status": status,
        "sources": ", ".join(sources or []),
    }

    errors = client.insert_rows_json(table_id, [row])

    if errors:
        print(f"BigQuery logging errors: {errors}")