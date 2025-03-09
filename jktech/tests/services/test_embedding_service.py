import pytest
import numpy as np
from app.services.embedding_service import EmbeddingService

pytestmark = pytest.mark.asyncio

class TestEmbeddingService:
    """Test the embedding service."""

    def test_chunk_text(self):
        """Test text chunking functionality."""
        service = EmbeddingService()
        text = "This is a test document. " * 100  # Create a longer text
        chunks = service.chunk_text(text, chunk_size=50, overlap=10)

        # Check that chunks were created
        assert len(chunks) > 0

        # Check that each chunk has the expected structure
        for chunk in chunks:
            assert "chunk_index" in chunk
            assert "content" in chunk
            assert "metadata" in chunk
            assert isinstance(chunk["metadata"], dict)
            assert "start_idx" in chunk["metadata"]
            assert "end_idx" in chunk["metadata"]
            assert "word_count" in chunk["metadata"]

    def test_get_embeddings(self):
        """Test embedding generation."""
        service = EmbeddingService()
        texts = ["This is a test document.", "This is another test document."]
        embeddings = service.get_embeddings(texts)

        # Check that embeddings were created
        assert len(embeddings) == len(texts)

        # Check that embeddings have the expected dimension
        for embedding in embeddings:
            assert len(embedding) == service.embedding_dimension

    def test_similarity_search(self):
        """Test similarity search functionality."""
        service = EmbeddingService()
        texts = [
            "Python is a programming language.",
            "Java is another programming language.",
            "FastAPI is a web framework for Python.",
            "Spring is a web framework for Java.",
            "This text is completely unrelated to programming."
        ]
        embeddings = service.get_embeddings(texts)

        # Search for Python-related content
        query = "Python programming"
        results = service.similarity_search(query, embeddings, top_k=2)

        # Check that results were returned
        assert len(results) == 2

        # Check that results have the expected structure
        for result in results:
            assert "index" in result
            assert "score" in result
            assert isinstance(result["index"], int)
            assert isinstance(result["score"], float)
            assert 0 <= result["score"] <= 1  # Cosine similarity is between 0 and 1

        # The most relevant result should be the first text (about Python)
        assert results[0]["index"] in [0, 2]  # Either "Python is a programming language" or "FastAPI is a web framework for Python"
