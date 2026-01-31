"""
Conversation model for AI chatbot sessions.
Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)
"""
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class Conversation(SQLModel, table=True):
    """
    Represents a chat session between a user and the AI assistant.

    Each conversation belongs to exactly one user (foreign key: user_id).
    All queries MUST filter by user_id from authenticated JWT.
    """

    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
