"""
ChatService handles business logic for chat operations.
Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)

All operations enforce user isolation at the database query level.
"""
from sqlmodel import Session, select, func
from uuid import UUID
from typing import List, Optional
from datetime import datetime, timedelta

from src.models.conversation import Conversation
from src.models.message import Message
from src.agents.chat_agent import ChatAgent


class ChatService:
    """Service layer for chat operations with strict user isolation."""

    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: UUID, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation for the authenticated user.

        Args:
            user_id: Authenticated user ID from JWT
            title: Optional conversation title

        Returns:
            Created conversation
        """
        conversation = Conversation(
            user_id=user_id,
            title=title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def get_conversation(self, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
        """
        Get a conversation by ID with ownership verification.

        Args:
            conversation_id: Conversation ID
            user_id: Authenticated user ID from JWT

        Returns:
            Conversation if found and owned by user, None otherwise

        CRITICAL: Returns None if conversation doesn't exist OR user doesn't own it
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,  # CRITICAL: User isolation
        )
        return self.session.exec(statement).first()

    def list_conversations(
        self, user_id: UUID, limit: int = 20, offset: int = 0
    ) -> tuple[List[Conversation], int]:
        """
        List all conversations for a user with pagination.

        Args:
            user_id: Authenticated user ID from JWT
            limit: Maximum number of conversations to return
            offset: Number of conversations to skip

        Returns:
            Tuple of (conversations list, total count)

        CRITICAL: Only returns conversations WHERE user_id = <authenticated_user_id>
        """
        # Get total count
        count_statement = (
            select(func.count(Conversation.id))
            .where(Conversation.user_id == user_id)
        )
        total = self.session.exec(count_statement).one()

        # Get conversations with pagination
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        conversations = list(self.session.exec(statement).all())

        return conversations, total

    def delete_conversation(self, conversation_id: UUID, user_id: UUID) -> bool:
        """
        Delete a conversation and all its messages.

        Args:
            conversation_id: Conversation ID
            user_id: Authenticated user ID from JWT

        Returns:
            True if deleted, False if not found/not owned

        CRITICAL: Returns False if conversation doesn't exist OR user doesn't own it
        """
        conversation = self.get_conversation(conversation_id, user_id)
        if not conversation:
            return False

        # Delete all messages first (foreign key)
        messages_statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id,
        )
        messages = self.session.exec(messages_statement).all()
        for message in messages:
            self.session.delete(message)

        # Delete conversation
        self.session.delete(conversation)
        self.session.commit()

        return True

    def add_message(
        self,
        user_id: UUID,
        conversation_id: UUID,
        role: str,
        content: str,
        tool_calls: Optional[dict] = None,
    ) -> Message:
        """
        Add a message to a conversation.

        Args:
            user_id: Authenticated user ID from JWT
            conversation_id: Conversation ID
            role: 'user' or 'assistant'
            content: Message content
            tool_calls: Optional tool calls (for assistant messages)

        Returns:
            Created message
        """
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            created_at=datetime.utcnow(),
        )

        self.session.add(message)

        # Update conversation's updated_at
        conversation = self.get_conversation(conversation_id, user_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)

        self.session.commit()
        self.session.refresh(message)

        return message

    def get_conversation_messages(
        self, conversation_id: UUID, user_id: UUID
    ) -> List[Message]:
        """
        Get all messages in a conversation.

        Args:
            conversation_id: Conversation ID
            user_id: Authenticated user ID from JWT

        Returns:
            List of messages in chronological order

        CRITICAL: Only returns messages WHERE user_id = <authenticated_user_id>
        """
        statement = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id,  # CRITICAL: User isolation
            )
            .order_by(Message.created_at.asc())
        )
        return list(self.session.exec(statement).all())

    def get_message_count(self, conversation_id: UUID, user_id: UUID) -> int:
        """Get the number of messages in a conversation."""
        statement = (
            select(func.count(Message.id))
            .where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id,
            )
        )
        return self.session.exec(statement).one()

    def get_last_message(
        self, conversation_id: UUID, user_id: UUID
    ) -> Optional[Message]:
        """Get the last message in a conversation."""
        statement = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id,
            )
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        return self.session.exec(statement).first()

    def update_conversation_title(
        self, conversation_id: UUID, user_id: UUID, title: str
    ) -> Optional[Conversation]:
        """Update the title of a conversation."""
        conversation = self.get_conversation(conversation_id, user_id)
        if not conversation:
            return None

        conversation.title = title[:200]  # Truncate to max length
        conversation.updated_at = datetime.utcnow()

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def auto_generate_title(self, first_message: str) -> str:
        """Generate a conversation title from the first message."""
        # Take first 50 chars or until newline
        title = first_message.split("\n")[0][:50]
        if len(first_message) > 50:
            title += "..."
        return title

    async def process_chat_message(
        self, user_id: UUID, conversation_id: Optional[UUID], message: str
    ) -> tuple[Conversation, Message, str, list]:
        """
        Process a chat message through the AI agent.

        Args:
            user_id: Authenticated user ID from JWT
            conversation_id: Existing conversation ID (or None to create new)
            message: User's message

        Returns:
            Tuple of (conversation, user_message, assistant_response, tool_calls)
        """
        # Get or create conversation
        if conversation_id:
            conversation = self.get_conversation(conversation_id, user_id)
            if not conversation:
                raise ValueError("Conversation not found")
        else:
            # Create new conversation
            conversation = self.create_conversation(user_id)

        # Save user message
        user_msg = self.add_message(
            user_id=user_id,
            conversation_id=conversation.id,
            role="user",
            content=message,
        )

        # Auto-generate title from first message if not set
        if not conversation.title:
            title = self.auto_generate_title(message)
            self.update_conversation_title(conversation.id, user_id, title)

        # Get conversation history for context
        messages = self.get_conversation_messages(conversation.id, user_id)
        history = [
            {"role": m.role, "content": m.content}
            for m in messages[:-1]  # Exclude the message we just added
        ]

        # Process through AI agent
        agent = ChatAgent(user_id, self.session)
        result = await agent.process_message(message, history)

        # Save assistant response
        tool_calls_data = None
        if result["tool_calls"]:
            tool_calls_data = {"calls": result["tool_calls"]}

        self.add_message(
            user_id=user_id,
            conversation_id=conversation.id,
            role="assistant",
            content=result["content"],
            tool_calls=tool_calls_data,
        )

        return conversation, user_msg, result["content"], result["tool_calls"]

    def get_messages_today_count(self, user_id: UUID) -> int:
        """Get the number of messages sent today by the user."""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        statement = (
            select(func.count(Message.id))
            .where(
                Message.user_id == user_id,
                Message.created_at >= today_start,
            )
        )
        return self.session.exec(statement).one()

    def get_conversation_count(self, user_id: UUID) -> int:
        """Get the total number of conversations for a user."""
        statement = (
            select(func.count(Conversation.id))
            .where(Conversation.user_id == user_id)
        )
        return self.session.exec(statement).one()
