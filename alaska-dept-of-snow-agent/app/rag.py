from google.cloud import storage
from app.config import settings


def load_documents_from_gcs():
    """
    Loads text-like documents from Cloud Storage.

    For this prototype, we keep retrieval simple:
    - list files from GCS
    - download readable text files
    - split into chunks
    - search chunks using keyword overlap

    This is acceptable for a PoC.
    """
    client = storage.Client(project=settings.PROJECT_ID)
    blobs = client.list_blobs(settings.GCS_BUCKET, prefix=settings.GCS_PREFIX)

    chunks = []

    for blob in blobs:
        if blob.name.endswith("/"):
            continue

        # Prototype supports text-like files directly.
        # PDFs can be added later using Document AI or PyPDF.
        if not (
            blob.name.endswith(".txt")
            or blob.name.endswith(".md")
            or blob.name.endswith(".html")
            or blob.name.endswith(".csv")
        ):
            continue

        try:
            content = blob.download_as_text()
        except Exception:
            content = blob.download_as_bytes().decode("utf-8", errors="ignore")
            
        for i, chunk in enumerate(split_text(content)):
            chunks.append({
                "source": f"gs://{settings.GCS_BUCKET}/{blob.name}",
                "chunk_id": i,
                "text": chunk
            })

    return chunks


def split_text(text, chunk_size=900, overlap=150):
    """
    Splits large text into overlapping chunks.
    """
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def retrieve_context(query, top_k=3):
    """
    Simple keyword-based retriever for prototype RAG.
    """
    chunks = load_documents_from_gcs()

    query_terms = set(query.lower().split())

    scored_chunks = []

    for chunk in chunks:
        chunk_terms = set(chunk["text"].lower().split())
        score = len(query_terms.intersection(chunk_terms))

        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    return [chunk for score, chunk in scored_chunks[:top_k]]