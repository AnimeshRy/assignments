from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the embedding service with a specific model."""
        self.model_name = model_name or settings.EMBEDDING_MODEL
        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        self.embedding_dimension = settings.EMBEDDING_DIMENSION
        logger.info(f"Embedding model loaded with dimension: {self.embedding_dimension}")

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of text chunks."""
        if not texts:
            return []

        try:
            embeddings = self.model.encode(texts)
            # Convert numpy arrays to Python lists for JSON serialization
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks for processing."""
        if not text:
            return []

        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            if len(chunk_words) < 10:  # Skip very small chunks
                continue

            chunk_text = " ".join(chunk_words)
            chunks.append({
                "chunk_index": len(chunks),
                "content": chunk_text,
                "metadata": {
                    "start_idx": i,
                    "end_idx": i + len(chunk_words),
                    "word_count": len(chunk_words)
                }
            })

        return chunks

    def process_document(self, content: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
        """Process a document by chunking and embedding it."""
        chunks = self.chunk_text(content, chunk_size, overlap)

        if not chunks:
            return []

        # Extract just the text content for embedding
        chunk_texts = [chunk["content"] for chunk in chunks]
        embeddings = self.get_embeddings(chunk_texts)

        # Add embeddings to chunks
        for i, embedding in enumerate(embeddings):
            chunks[i]["embedding"] = embedding

        return chunks

    def similarity_search(self, query: str, embeddings: List[List[float]], top_k: int = 5) -> List[Dict[str, Any]]:
        """Find the most similar chunks to a query."""
        if not embeddings:
            return []

        query_embedding = self.get_embeddings([query])[0]

        # Convert to numpy arrays for efficient computation
        query_embedding_np = np.array(query_embedding)
        embeddings_np = np.array(embeddings)

        # Compute cosine similarity
        similarities = np.dot(embeddings_np, query_embedding_np) / (
            np.linalg.norm(embeddings_np, axis=1) * np.linalg.norm(query_embedding_np)
        )

        # Get indices of top_k most similar chunks
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # Return results with scores
        results = []
        for idx in top_indices:
            results.append({
                "index": int(idx),
                "score": float(similarities[idx])
            })

        return results
