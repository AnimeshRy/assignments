from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    content_type: str

class DocumentCreate(DocumentBase):
    content: str

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None

class DocumentChunkBase(BaseModel):
    chunk_index: int
    content: str
    metadata: Optional[Dict[str, Any]] = None

class DocumentChunkCreate(DocumentChunkBase):
    document_id: int

class DocumentChunkInDB(DocumentChunkBase):
    id: int
    document_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class DocumentInDBBase(DocumentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Document(DocumentInDBBase):
    chunks: List[DocumentChunkInDB] = []

class DocumentInDB(DocumentInDBBase):
    content: str
    chunks: List[DocumentChunkInDB] = []
