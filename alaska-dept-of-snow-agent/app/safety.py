from typing import Tuple


BLOCKED_TERMS = [
    "hack",
    "exploit",
    "bypass",
    "steal",
    "password",
    "private key",
    "credentials",
    "ignore previous instructions",
    "system prompt",
]


def is_prompt_allowed(user_query: str) -> Tuple[bool, str]:
    """
    Lightweight local safety check (fallback + testable).
    Model Armor is primary control.
    """
    query = user_query.lower()

    for term in BLOCKED_TERMS:
        if term in query:
            return False, f"Blocked unsafe term: {term}"

    if len(user_query.strip()) < 3:
        return False, "Prompt too short"

    if len(user_query) > 1000:
        return False, "Prompt too long"

    return True, "Allowed"


def validate_response(answer: str) -> Tuple[bool, str]:
    """
    Lightweight response validation.
    """
    if not answer or len(answer.strip()) == 0:
        return False, "Empty response"

    suspicious_phrases = [
        "ignore previous instructions",
        "system prompt",
        "private key",
        "credentials",
    ]

    answer_lower = answer.lower()

    for phrase in suspicious_phrases:
        if phrase in answer_lower:
            return False, f"Unsafe response phrase: {phrase}"

    return True, "Valid"