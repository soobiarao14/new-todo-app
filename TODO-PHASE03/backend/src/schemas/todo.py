"""
Todo request/response schemas for CRUD operations.
"""
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional, List


class TodoResponse(BaseModel):
    """Todo entity returned in API responses."""

    id: UUID = Field(..., description="Todo ID")
    user_id: UUID = Field(..., description="User ID (owner)")
    title: str = Field(..., max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=2000, description="Todo description")
    completed: bool = Field(default=False, description="Completion status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility


class TodoListResponse(BaseModel):
    """Response for listing all todos."""

    todos: List[TodoResponse] = Field(..., description="List of todos")


class TodoCreateRequest(BaseModel):
    """Request schema for creating a new todo."""

    title: str = Field(..., min_length=1, max_length=200, description="Todo title (required)")
    description: Optional[str] = Field(None, max_length=2000, description="Todo description (optional)")

    @field_validator("title")
    @classmethod
    def title_not_whitespace(cls, v: str) -> str:
        """Ensure title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()


class TodoUpdateRequest(BaseModel):
    """Request schema for updating an existing todo."""

    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=2000, description="Todo description")

    @field_validator("title")
    @classmethod
    def title_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Ensure title is not empty or whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip() if v else None

    class Config:
        extra = "forbid"  # Reject extra fields
