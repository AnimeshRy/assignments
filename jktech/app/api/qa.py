from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_async_session
from app.models.user import User
from app.schemas.qa import (
    QASessionCreate, QASessionResponse, QASessionUpdate,
    AskQuestionRequest, AskQuestionResponse
)
from app.services.qa_session_service import QASessionService
from app.services.rag_service import RAGService
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/sessions", response_model=QASessionResponse, status_code=status.HTTP_201_CREATED)
async def create_qa_session(
    *,
    session: AsyncSession = Depends(get_async_session),
    qa_session_in: QASessionCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Create a new QA session with selected documents."""
    qa_session_service = QASessionService()
    qa_session = await qa_session_service.create_qa_session(
        session=session,
        user_id=current_user.id,
        name=qa_session_in.name,
        document_ids=qa_session_in.document_ids
    )

    if not qa_session:
        raise HTTPException(
            status_code=400,
            detail="Could not create QA session. Check that all document IDs are valid and belong to you."
        )

    # Prepare response with document IDs
    return {
        "id": qa_session.id,
        "user_id": qa_session.user_id,
        "name": qa_session.name,
        "created_at": qa_session.created_at,
        "updated_at": qa_session.updated_at,
        "document_ids": [doc.id for doc in qa_session.documents],
        "questions": []
    }

@router.get("/sessions", response_model=List[QASessionResponse])
async def read_qa_sessions(
    *,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get all QA sessions for current user."""
    qa_session_service = QASessionService()
    qa_sessions = await qa_session_service.get_qa_sessions(session, current_user.id)

    # Prepare response with document IDs for each session
    result = []
    for qa_session in qa_sessions:
        result.append({
            "id": qa_session.id,
            "user_id": qa_session.user_id,
            "name": qa_session.name,
            "created_at": qa_session.created_at,
            "updated_at": qa_session.updated_at,
            "document_ids": [doc.id for doc in qa_session.documents],
            "questions": qa_session.questions
        })

    return result

@router.get("/sessions/{qa_session_id}", response_model=QASessionResponse)
async def read_qa_session(
    *,
    session: AsyncSession = Depends(get_async_session),
    qa_session_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get a QA session by ID."""
    qa_session_service = QASessionService()
    qa_session = await qa_session_service.get_qa_session(session, qa_session_id)

    if not qa_session:
        raise HTTPException(
            status_code=404,
            detail="QA session not found"
        )

    # Check if user has access to this QA session
    if qa_session.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    # Prepare response with document IDs
    return {
        "id": qa_session.id,
        "user_id": qa_session.user_id,
        "name": qa_session.name,
        "created_at": qa_session.created_at,
        "updated_at": qa_session.updated_at,
        "document_ids": [doc.id for doc in qa_session.documents],
        "questions": qa_session.questions
    }

@router.put("/sessions/{qa_session_id}", response_model=QASessionResponse)
async def update_qa_session(
    *,
    session: AsyncSession = Depends(get_async_session),
    qa_session_id: int,
    qa_session_in: QASessionUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update a QA session."""
    qa_session_service = QASessionService()

    # Check if user has access to this QA session
    qa_session = await qa_session_service.get_qa_session(session, qa_session_id)
    if not qa_session:
        raise HTTPException(
            status_code=404,
            detail="QA session not found"
        )

    if qa_session.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    qa_session = await qa_session_service.update_qa_session(
        session=session,
        qa_session_id=qa_session_id,
        name=qa_session_in.name,
        document_ids=qa_session_in.document_ids
    )

    if not qa_session:
        raise HTTPException(
            status_code=400,
            detail="Could not update QA session. Check that all document IDs are valid."
        )

    # Prepare response with document IDs
    return {
        "id": qa_session.id,
        "user_id": qa_session.user_id,
        "name": qa_session.name,
        "created_at": qa_session.created_at,
        "updated_at": qa_session.updated_at,
        "document_ids": [doc.id for doc in qa_session.documents],
        "questions": qa_session.questions
    }

@router.delete("/sessions/{qa_session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_qa_session(
    *,
    session: AsyncSession = Depends(get_async_session),
    qa_session_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Delete a QA session."""
    qa_session_service = QASessionService()

    # Check if user has access to this QA session
    qa_session = await qa_session_service.get_qa_session(session, qa_session_id)
    if not qa_session:
        raise HTTPException(
            status_code=404,
            detail="QA session not found"
        )

    if qa_session.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    await qa_session_service.delete_qa_session(session, qa_session_id)
    return None

@router.post("/ask", response_model=AskQuestionResponse)
async def ask_question(
    *,
    session: AsyncSession = Depends(get_async_session),
    question_in: AskQuestionRequest,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Ask a question and get an answer based on the documents in the QA session."""
    # Check if user has access to this QA session
    qa_session_service = QASessionService()
    qa_session = await qa_session_service.get_qa_session(session, question_in.qa_session_id)

    if not qa_session:
        raise HTTPException(
            status_code=404,
            detail="QA session not found"
        )

    if qa_session.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    # Use RAG service to answer the question
    rag_service = RAGService()
    answer = await rag_service.answer_question(
        session=session,
        question=question_in.question,
        qa_session_id=question_in.qa_session_id
    )

    return answer
