from app.rag import split_text


def test_split_text_returns_chunks():
    text = "snow plowing updates " * 100
    chunks = split_text(text, chunk_size=100, overlap=20)

    assert len(chunks) > 1
    assert all(len(chunk) <= 100 for chunk in chunks)