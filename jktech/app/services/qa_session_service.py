from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.qa_session import QASession, Question
from app.models.document import Document
import logging

logger = logging.getLogger(__name__)

class QASessionService:
    def __init__(self):
        """Initialize the QA session service."""
        logger.info("QA session service initialized")

    async def create_qa_session(
        self,
        session: AsyncSession,
        user_id: int,
        name: str,
        document_ids: List[int]
    ) -> Optional[QASession]:
        """Create a new QA session with selected documents."""
        # Verify that all documents exist and belong to the user
        for doc_id in document_ids:
            document = await session.get(Document, doc_id)
            if not document or document.user_id != user_id:
                logger.warning(f"Document {doc_id} not found or doesn't belong to user {user_id}")
                return None

        # Create the QA session
        qa_session = QASession(
            user_id=user_id,
            name=name
        )
        session.add(qa_session)
        await session.flush()  # Flush to get the QA session ID

        # Add documents to the QA session
        for doc_id in document_ids:
            document = await session.get(Document, doc_id)
            qa_session.documents.append(document)

        await session.commit()
        return qa_session

    async def get_qa_session(self, session: AsyncSession, qa_session_id: int) -> Optional[QASession]:
        """Get a QA session by ID."""
        return await session.get(QASession, qa_session_id)

    async def get_qa_sessions(self, session: AsyncSession, user_id: int) -> List[QASession]:
        """Get all QA sessions for a user."""
        stmt = select(QASession).where(QASession.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def update_qa_session(
        self,
        session: AsyncSession,
        qa_session_id: int,
        name: Optional[str] = None,
        document_ids: Optional[List[int]] = None
    ) -> Optional[QASession]:
        """Update a QA session."""
        qa_session = await session.get(QASession, qa_session_id)
        if not qa_session:
            return None

        # Update name if provided
        if name is not None:
            qa_session.name = name

        # Update documents if provided
        if document_ids is not None:
            # Verify that all documents exist
            for doc_id in document_ids:
                document = await session.get(Document, doc_id)
                if not document:
                    logger.warning(f"Document {doc_id} not found")
                    return None

            # Clear existing documents
            qa_session.documents = []

            # Add new documents
            for doc_id in document_ids:
                document = await session.get(Document, doc_id)
                qa_session.documents.append(document)

        await session.commit()
        return qa_session

    async def delete_qa_session(self, session: AsyncSession, qa_session_id: int) -> bool:
        """Delete a QA session."""
        qa_session = await session.get(QASession, qa_session_id)
        if not qa_session:
            return False

        await session.delete(qa_session)  # This will cascade delete questions
        await session.commit()
        return True

    async def get_questions(self, session: AsyncSession, qa_session_id: int) -> List[Question]:
        """Get all questions for a QA session."""
        stmt = select(Question).where(Question.qa_session_id == qa_session_id)
        result = await session.execute(stmt)
        return result.scalars().all()
