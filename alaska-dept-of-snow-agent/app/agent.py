import vertexai
from vertexai.generative_models import GenerativeModel

from app.config import settings
from app.rag import retrieve_context


def build_prompt(user_query: str, context_chunks: list[dict]) -> str:
    context_text = "\n\n".join(
        f"Source: {chunk['source']}\nContent: {chunk['text']}"
        for chunk in context_chunks
    )

    return f"""
You are the Alaska Department of Snow public information assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Be concise and helpful.
- Do not invent facts.
- If the answer is not in the context, say:
  "I don't have enough information from ADS documents to answer that."
- Include source references when possible.

Context:
{context_text}

User question:
{user_query}

Answer:
"""


def generate_answer(user_query: str) -> dict:
    vertexai.init(
        project=settings.PROJECT_ID,
        location=settings.LOCATION
    )

    context_chunks = retrieve_context(user_query)

    if not context_chunks:
        return {
            "answer": "I don't have enough information from ADS documents to answer that.",
            "sources": []
        }

    prompt = build_prompt(user_query, context_chunks)

    model = GenerativeModel(settings.MODEL_NAME)
    response = model.generate_content(prompt)

    sources = list({chunk["source"] for chunk in context_chunks})

    return {
        "answer": response.text,
        "sources": sources
    }