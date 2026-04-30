import requests
import google.auth
import google.auth.transport.requests

from app.config import settings


def _get_access_token() -> str:
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)
    return credentials.token


def _template_name() -> str:
    return (
        f"projects/{settings.PROJECT_ID}/locations/"
        f"{settings.MODEL_ARMOR_LOCATION}/templates/"
        f"{settings.MODEL_ARMOR_TEMPLATE_ID}"
    )


def _call_model_armor(endpoint: str, text: str) -> dict:
    token = _get_access_token()

    url = (
        f"https://modelarmor.{settings.MODEL_ARMOR_LOCATION}.rep.googleapis.com/"
        f"v1/{_template_name()}:{endpoint}"
    )

    if endpoint == "sanitizeUserPrompt":
        payload = {
            "userPromptData": {
                "text": text
            }
        }
    else:
        payload = {
            "modelResponseData": {
                "text": text
            }
        }

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def sanitize_user_prompt(user_prompt: str) -> tuple[bool, str, dict]:
    result = _call_model_armor("sanitizeUserPrompt", user_prompt)

    sanitization_result = result.get("sanitizationResult", {})
    filter_match_state = sanitization_result.get("filterMatchState", "")

    allowed = filter_match_state != "MATCH_FOUND"
    return allowed, user_prompt, result


def sanitize_model_response(model_response: str) -> tuple[bool, str, dict]:
    result = _call_model_armor("sanitizeModelResponse", model_response)

    sanitization_result = result.get("sanitizationResult", {})
    filter_match_state = sanitization_result.get("filterMatchState", "")

    allowed = filter_match_state != "MATCH_FOUND"
    return allowed, model_response, result