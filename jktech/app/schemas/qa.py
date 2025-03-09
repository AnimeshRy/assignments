from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class QuestionBase(BaseModel):
    question_text: str

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    qa_session_id: int
    answer_text: Optional[str] = None
    created_at: datetime
    retrieval_metadata: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class QASessionBase(BaseModel):
    name: str

class QASessionCreate(QASessionBase):
    document_ids: List[int]

class QASessionUpdate(BaseModel):
    name: Optional[str] = None
    document_ids: Optional[List[int]] = None

class QASessionResponse(QASessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    document_ids: List[int]
    questions: List[QuestionResponse] = []

    class Config:
        orm_mode = True

class AskQuestionRequest(BaseModel):
    question: str
    qa_session_id: int

class AskQuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[Dict[str, Any]]
