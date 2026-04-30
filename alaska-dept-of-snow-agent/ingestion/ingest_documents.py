from google.cloud import storage
from app.config import settings


def list_documents():
    """
    Lists documents from the ADS Cloud Storage bucket/prefix.
    """
    client = storage.Client(project=settings.PROJECT_ID)

    blobs = client.list_blobs(
        settings.GCS_BUCKET,
        prefix=settings.GCS_PREFIX
    )

    documents = []

    for blob in blobs:
        if blob.name.endswith("/"):
            continue

        documents.append({
            "name": blob.name,
            "gcs_uri": f"gs://{settings.GCS_BUCKET}/{blob.name}",
            "content_type": blob.content_type,
            "size": blob.size,
        })

    return documents


def main():
    docs = list_documents()

    print(f"Found {len(docs)} documents:\n")

    for doc in docs:
        print(f"- {doc['gcs_uri']}")
        print(f"  Type: {doc['content_type']}")
        print(f"  Size: {doc['size']} bytes\n")


if __name__ == "__main__":
    main()