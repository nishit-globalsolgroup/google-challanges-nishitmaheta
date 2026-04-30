from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


@patch("app.main.generate_answer")
@patch("app.main.sanitize_user_prompt")
@patch("app.main.sanitize_model_response")
def test_chat_success(mock_response_safety, mock_prompt_safety, mock_agent):
    mock_prompt_safety.return_value = (True, "test question", {})
    mock_agent.return_value = {
        "answer": "Snow plowing is active",
        "sources": ["gs://test/doc1.txt"],
    }
    mock_response_safety.return_value = (True, "Snow plowing is active", {})

    response = client.post("/chat", json={"question": "Snow updates?"})

    assert response.status_code == 200
    assert response.json()["status"] == "success"


@patch("app.main.sanitize_user_prompt")
def test_chat_blocked(mock_prompt_safety):
    mock_prompt_safety.return_value = (False, "bad prompt", {})

    response = client.post("/chat", json={"question": "hack system"})

    assert response.json()["status"] == "blocked_by_model_armor"