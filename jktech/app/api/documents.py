from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_async_session
from app.models.user import User
from app.schemas.document import DocumentCreate, Document as DocumentSchema
from app.services.document_service import DocumentService
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=DocumentSchema, status_code=status.HTTP_201_CREATED)
async def create_document(
    *,
    session: AsyncSession = Depends(get_async_session),
    document_in: DocumentCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Create new document."""
    document_service = DocumentService()
    document = await document_service.create_document(
        session=session,
        user_id=current_user.id,
        title=document_in.title,
        content=document_in.content,
        content_type=document_in.content_type
    )
    return document

@router.post("/upload", response_model=DocumentSchema, status_code=status.HTTP_201_CREATED)
async def upload_document(
    *,
    session: AsyncSession = Depends(get_async_session),
    file: UploadFile = File(...),
    title: str = Form(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Upload a document file."""
    document_service = DocumentService()

    # Read file content
    content = await file.read()
    content_str = content.decode("utf-8")

    # Determine content type from file
    content_type = file.content_type or "text/plain"

    document = await document_service.create_document(
        session=session,
        user_id=current_user.id,
        title=title,
        content=content_str,
        content_type=content_type
    )
    return document

@router.get("/{document_id}", response_model=DocumentSchema)
async def read_document(
    *,
    session: AsyncSession = Depends(get_async_session),
    document_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get document by ID."""
    document_service = DocumentService()
    document = await document_service.get_document(session, document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Check if user has access to this document
    if document.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    return document

@router.get("/", response_model=List[DocumentSchema])
async def read_documents(
    *,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get all documents for current user."""
    document_service = DocumentService()

    # If superuser, get all documents, otherwise only user's documents
    if current_user.is_superuser:
        documents = await document_service.get_documents(session)
    else:
        documents = await document_service.get_documents(session, current_user.id)

    return documents

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    *,
    session: AsyncSession = Depends(get_async_session),
    document_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Delete a document."""
    document_service = DocumentService()
    document = await document_service.get_document(session, document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Check if user has access to delete this document
    if document.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    await document_service.delete_document(session, document_id)
    return None
