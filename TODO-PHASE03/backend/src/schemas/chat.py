"""
Chat request/response schemas for AI chatbot.
Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Any


class ChatRequest(BaseModel):
    """Request schema for sending a chat message."""

    conversation_id: Optional[UUID] = Field(
        None, description="Existing conversation ID. If omitted, a new conversation is created."
    )
    message: str = Field(
        ..., min_length=1, max_length=4000, description="User's natural language message"
    )


class ToolCallSchema(BaseModel):
    """Schema for a single MCP tool invocation."""

    tool: str = Field(..., description="MCP tool name")
    parameters: dict = Field(default_factory=dict, description="Parameters passed to the tool")
    result: Optional[Any] = Field(None, description="Tool execution result")
    success: bool = Field(..., description="Whether the tool executed successfully")


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    conversation_id: UUID = Field(..., description="Conversation ID (existing or newly created)")
    response: str = Field(..., description="AI assistant's response text")
    tool_calls: List[ToolCallSchema] = Field(
        default_factory=list, description="List of MCP tools invoked during this request"
    )


class MessageSchema(BaseModel):
    """Schema for a single message in a conversation."""

    id: UUID = Field(..., description="Message ID")
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    tool_calls: Optional[List[ToolCallSchema]] = Field(
        None, description="Tool calls (only for assistant messages)"
    )
    created_at: datetime = Field(..., description="Message timestamp")

    class Config:
        from_attributes = True


class ConversationSummary(BaseModel):
    """Summary schema for listing conversations."""

    id: UUID = Field(..., description="Conversation ID")
    title: Optional[str] = Field(None, description="Conversation title")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last activity timestamp")
    message_count: int = Field(0, description="Number of messages in conversation")
    last_message_preview: Optional[str] = Field(None, description="Preview of the last message")

    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    """Response schema for listing conversations."""

    conversations: List[ConversationSummary] = Field(..., description="List of conversations")
    total: int = Field(..., description="Total number of conversations")


class ConversationDetailResponse(BaseModel):
    """Response schema for getting a single conversation with messages."""

    id: UUID = Field(..., description="Conversation ID")
    title: Optional[str] = Field(None, description="Conversation title")
    messages: List[MessageSchema] = Field(..., description="Conversation messages")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last activity timestamp")

    class Config:
        from_attributes = True


class DashboardStatsResponse(BaseModel):
    """Response schema for dashboard statistics."""

    total_tasks: int = Field(..., description="Total number of tasks")
    completed_tasks: int = Field(..., description="Number of completed tasks")
    pending_tasks: int = Field(..., description="Number of pending tasks")
    total_conversations: int = Field(..., description="Total number of conversations")
    messages_today: int = Field(..., description="Messages sent today")
