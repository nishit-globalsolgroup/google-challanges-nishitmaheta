from unittest.mock import patch

from app.agent import build_prompt


def test_build_prompt_contains_query_and_context():
    query = "What are snow updates?"
    context = [
        {"source": "gs://test/doc1.txt", "text": "Snow plowing is ongoing"}
    ]

    prompt = build_prompt(query, context)

    assert "Snow plowing is ongoing" in prompt
    assert "What are snow updates?" in prompt