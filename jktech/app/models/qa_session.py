from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base

# Association table for many-to-many relationship between QASession and Document
qa_session_document = Table(
    "qa_session_document",
    Base.metadata,
    Column("qa_session_id", Integer, ForeignKey("qasession.id"), primary_key=True),
    Column("document_id", Integer, ForeignKey("document.id"), primary_key=True)
)

class QASession(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="qa_sessions")
    documents = relationship("Document", secondary=qa_session_document)
    questions = relationship("Question", back_populates="qa_session", cascade="all, delete-orphan")

class Question(Base):
    id = Column(Integer, primary_key=True, index=True)
    qa_session_id = Column(Integer, ForeignKey("qasession.id"))
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Metadata about the retrieval process
    retrieval_metadata = Column(JSONB, nullable=True)

    # Relationship
    qa_session = relationship("QASession", back_populates="questions")
