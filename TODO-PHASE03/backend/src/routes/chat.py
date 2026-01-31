"""
Chat API endpoints for AI chatbot.
Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)

All endpoints require JWT authentication and enforce user isolation.
"""
import logging
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from src.db import get_session
from src.dependencies import get_current_user_id
from src.services.chat_service import ChatService
from src.services.todo_service import TodoService
from src.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ToolCallSchema,
    MessageSchema,
    ConversationSummary,
    ConversationListResponse,
    ConversationDetailResponse,
    DashboardStatsResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def send_chat_message(
    request: ChatRequest,
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Send a chat message to the AI assistant.

    The assistant interprets the message and performs task operations via MCP tools.
    If conversation_id is not provided, a new conversation is created.

    **Authentication**: Required (JWT Bearer token)
    **User Isolation**: user_id extracted from JWT, not from request body
    """
    chat_service = ChatService(session)

    try:
        # Verify conversation exists and is owned by user (if provided)
        if request.conversation_id:
            conversation = chat_service.get_conversation(request.conversation_id, user_id)
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "error": {
                            "code": "NOT_FOUND",
                            "message": "Conversation not found",
                        }
                    },
                )

        # Process the message through the AI agent
        conversation, user_msg, response_text, tool_calls = (
            await chat_service.process_chat_message(
                user_id=user_id,
                conversation_id=request.conversation_id,
                message=request.message,
            )
        )

        # Convert tool calls to response schema
        tool_call_schemas = [
            ToolCallSchema(
                tool=tc["tool"],
                parameters=tc["parameters"],
                result=tc["result"],
                success=tc["success"],
            )
            for tc in tool_calls
        ]

        return ChatResponse(
            conversation_id=conversation.id,
            response=response_text,
            tool_calls=tool_call_schemas,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": str(e)}},
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                }
            },
        )


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    limit: int = Query(20, ge=1, le=100, description="Maximum conversations to return"),
    offset: int = Query(0, ge=0, description="Number of conversations to skip"),
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    List all conversations for the authenticated user.

    Sorted by most recent activity.

    **Authentication**: Required (JWT Bearer token)
    """
    chat_service = ChatService(session)
    conversations, total = chat_service.list_conversations(user_id, limit, offset)

    # Build response with message counts and previews
    summaries = []
    for conv in conversations:
        message_count = chat_service.get_message_count(conv.id, user_id)
        last_message = chat_service.get_last_message(conv.id, user_id)
        preview = None
        if last_message:
            preview = last_message.content[:100] + "..." if len(last_message.content) > 100 else last_message.content

        summaries.append(
            ConversationSummary(
                id=conv.id,
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=message_count,
                last_message_preview=preview,
            )
        )

    return ConversationListResponse(conversations=summaries, total=total)


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Get a specific conversation with its message history.

    **Authentication**: Required (JWT Bearer token)
    **User Isolation**: Returns 404 if conversation not owned by user
    """
    chat_service = ChatService(session)
    conversation = chat_service.get_conversation(conversation_id, user_id)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Conversation not found"}},
        )

    # Get messages
    messages = chat_service.get_conversation_messages(conversation_id, user_id)

    # Convert messages to schema
    message_schemas = []
    for msg in messages:
        tool_calls = None
        if msg.tool_calls and "calls" in msg.tool_calls:
            tool_calls = [
                ToolCallSchema(
                    tool=tc["tool"],
                    parameters=tc["parameters"],
                    result=tc.get("result"),
                    success=tc["success"],
                )
                for tc in msg.tool_calls["calls"]
            ]

        message_schemas.append(
            MessageSchema(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                tool_calls=tool_calls,
                created_at=msg.created_at,
            )
        )

    return ConversationDetailResponse(
        id=conversation.id,
        title=conversation.title,
        messages=message_schemas,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Delete a conversation and all its messages.

    **Authentication**: Required (JWT Bearer token)
    **User Isolation**: Returns 404 if conversation not owned by user
    """
    chat_service = ChatService(session)
    deleted = chat_service.delete_conversation(conversation_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Conversation not found"}},
        )

    return None


@router.get("/dashboard/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Get aggregated statistics for the authenticated user.

    **Authentication**: Required (JWT Bearer token)
    """
    try:
        chat_service = ChatService(session)
        todo_service = TodoService(session)

        # Get task counts
        all_tasks = todo_service.list_by_user(user_id)
        total_tasks = len(all_tasks)
        completed_tasks = len([t for t in all_tasks if t.completed])
        pending_tasks = total_tasks - completed_tasks

        # Get conversation/message counts
        total_conversations = chat_service.get_conversation_count(user_id)
        messages_today = chat_service.get_messages_today_count(user_id)

        return DashboardStatsResponse(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
            total_conversations=total_conversations,
            messages_today=messages_today,
        )
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Failed to retrieve dashboard statistics",
                }
            },
        )
