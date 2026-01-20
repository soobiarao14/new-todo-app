"""
Message model for conversation messages.
Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)
"""
from datetime import datetime
from typing import Optional, Any
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column
from sqlalchemy.dialects.postgresql import JSONB


class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation (user or assistant).

    Each message belongs to exactly one user and one conversation.
    The role field indicates who sent the message ('user' or 'assistant').
    Tool calls are stored as JSONB for assistant messages that invoke MCP tools.

    CRITICAL: All queries MUST filter by user_id from authenticated JWT.
    """

    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True, nullable=False)
    role: str = Field(max_length=20, nullable=False)  # 'user' or 'assistant'
    content: str = Field(nullable=False)
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
