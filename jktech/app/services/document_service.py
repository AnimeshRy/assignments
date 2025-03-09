from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.document import Document, DocumentChunk
from app.services.embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self):
        """Initialize the document service."""
        self.embedding_service = EmbeddingService()
        logger.info("Document service initialized")

    async def create_document(
        self,
        session: AsyncSession,
        user_id: int,
        title: str,
        content: str,
        content_type: str
    ) -> Document:
        """Create a new document and process it for embeddings."""
        # Create the document
        document = Document(
            user_id=user_id,
            title=title,
            content=content,
            content_type=content_type
        )
        session.add(document)
        await session.flush()  # Flush to get the document ID

        # Process the document to create chunks and embeddings
        processed_chunks = self.embedding_service.process_document(content)

        # Create document chunks with embeddings
        for chunk_data in processed_chunks:
            chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=chunk_data["chunk_index"],
                content=chunk_data["content"],
                embedding=chunk_data["embedding"],
                metadata=chunk_data["metadata"]
            )
            session.add(chunk)

        await session.commit()
        return document

    async def get_document(self, session: AsyncSession, document_id: int) -> Optional[Document]:
        """Get a document by ID."""
        return await session.get(Document, document_id)

    async def get_documents(self, session: AsyncSession, user_id: Optional[int] = None) -> List[Document]:
        """Get all documents, optionally filtered by user ID."""
        if user_id:
            stmt = select(Document).where(Document.user_id == user_id)
        else:
            stmt = select(Document)

        result = await session.execute(stmt)
        return result.scalars().all()

    async def delete_document(self, session: AsyncSession, document_id: int) -> bool:
        """Delete a document and its chunks."""
        document = await session.get(Document, document_id)
        if not document:
            return False

        await session.delete(document)  # This will cascade delete chunks
        await session.commit()
        return True

    async def update_document(
        self,
        session: AsyncSession,
        document_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        content_type: Optional[str] = None
    ) -> Optional[Document]:
        """Update a document and reprocess if content changes."""
        document = await session.get(Document, document_id)
        if not document:
            return None

        # Update document fields
        if title is not None:
            document.title = title
        if content_type is not None:
            document.content_type = content_type

        # If content changes, reprocess the document
        if content is not None and content != document.content:
            document.content = content

            # Delete existing chunks
            stmt = select(DocumentChunk).where(DocumentChunk.document_id == document_id)
            result = await session.execute(stmt)
            chunks = result.scalars().all()
            for chunk in chunks:
                await session.delete(chunk)

            # Process the new content
            processed_chunks = self.embedding_service.process_document(content)

            # Create new document chunks with embeddings
            for chunk_data in processed_chunks:
                chunk = DocumentChunk(
                    document_id=document.id,
                    chunk_index=chunk_data["chunk_index"],
                    content=chunk_data["content"],
                    embedding=chunk_data["embedding"],
                    metadata=chunk_data["metadata"]
                )
                session.add(chunk)

        await session.commit()
        return document
