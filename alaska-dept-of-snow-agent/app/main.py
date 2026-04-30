from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import generate_answer
from app.model_armor import sanitize_user_prompt, sanitize_model_response
from app.logging_service import log_chat_interaction
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Alaska Department of Snow Online Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str


@app.get("/")
def health_check():
    return {"status": "ok", "service": "ADS Online Agent"}


@app.post("/chat")
def chat(request: ChatRequest):
    prompt_allowed, sanitized_prompt, prompt_security = sanitize_user_prompt(
        request.question
    )

    if not prompt_allowed:
        answer = "I can only help with safe Alaska Department of Snow public information questions."
        log_chat_interaction(request.question, answer, "blocked_by_model_armor", [])

        return {
            "question": request.question,
            "answer": answer,
            "sources": [],
            "status": "blocked_by_model_armor",
            "security": prompt_security,
        }

    result = generate_answer(sanitized_prompt)

    response_allowed, sanitized_response, response_security = sanitize_model_response(
        result["answer"]
    )

    if not response_allowed:
        answer = "I could not safely return that response. Please contact ADS directly."
        sources = result.get("sources", [])
        log_chat_interaction(request.question, answer, "response_blocked_by_model_armor", sources)

        return {
            "question": request.question,
            "answer": answer,
            "sources": sources,
            "status": "response_blocked_by_model_armor",
            "security": response_security,
        }

    log_chat_interaction(
        question=request.question,
        answer=sanitized_response,
        status="success",
        sources=result["sources"],
    )

    return {
        "question": request.question,
        "answer": sanitized_response,
        "sources": result["sources"],
        "status": "success",
    }