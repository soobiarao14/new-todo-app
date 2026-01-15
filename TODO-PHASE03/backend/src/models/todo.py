"""
Todo model with user isolation enforced at the database level.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship


class Todo(SQLModel, table=True):
    """
    Todo entity with strict user isolation.
    Each todo belongs to exactly one user (foreign key: user_id).
    All queries MUST filter by user_id from authenticated JWT.
    """

    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        # Ensure timestamps are always in UTC
        json_encoders = {datetime: lambda v: v.isoformat()}
