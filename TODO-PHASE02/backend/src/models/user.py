"""
User model (read-only reference).
User data is managed by Better Auth; this model is for reference only.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    User entity managed by Better Auth.
    This is a read-only reference model for the application.
    DO NOT create, update, or delete users directly through this model.
    """

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        # Ensure timestamps are always in UTC
        json_encoders = {datetime: lambda v: v.isoformat()}
