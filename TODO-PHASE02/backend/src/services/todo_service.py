"""
TodoService handles business logic for todo CRUD operations.
All operations enforce user isolation at the database query level.
"""
from sqlmodel import Session, select
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from src.models.todo import Todo
from src.schemas.todo import TodoCreateRequest, TodoUpdateRequest


class TodoService:
    """Service layer for todo operations with strict user isolation."""

    def __init__(self, session: Session):
        self.session = session

    def list_by_user(self, user_id: UUID) -> List[Todo]:
        """
        List all todos for a specific user.
        Orders by created_at descending (newest first).

        CRITICAL: Only returns todos WHERE user_id = <authenticated_user_id>
        """
        statement = (
            select(Todo)
            .where(Todo.user_id == user_id)
            .order_by(Todo.created_at.desc())
        )
        todos = self.session.exec(statement).all()
        return list(todos)

    def get_by_id(self, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """
        Get a single todo by ID with ownership verification.

        Args:
            todo_id: Todo ID
            user_id: Authenticated user ID from JWT

        Returns:
            Todo if found and owned by user, None otherwise

        CRITICAL: Returns None if todo doesn't exist OR user doesn't own it (404, not 403)
        """
        statement = select(Todo).where(
            Todo.id == todo_id, Todo.user_id == user_id
        )
        todo = self.session.exec(statement).first()
        return todo

    def create(self, user_id: UUID, request: TodoCreateRequest) -> Todo:
        """
        Create a new todo for the authenticated user.

        Args:
            user_id: Authenticated user ID from JWT (NEVER from request body)
            request: Todo creation data

        Returns:
            Created todo
        """
        todo = Todo(
            user_id=user_id,
            title=request.title,
            description=request.description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)

        return todo

    def update(self, todo_id: UUID, user_id: UUID, request: TodoUpdateRequest) -> Optional[Todo]:
        """
        Update an existing todo with ownership verification.

        Args:
            todo_id: Todo ID
            user_id: Authenticated user ID from JWT
            request: Todo update data (only provided fields updated)

        Returns:
            Updated todo if found and owned, None if not found/not owned

        CRITICAL: Returns None (404) if todo doesn't exist OR user doesn't own it
        """
        todo = self.get_by_id(todo_id, user_id)

        if not todo:
            return None

        # Update only provided fields
        if request.title is not None:
            todo.title = request.title

        if request.description is not None:
            todo.description = request.description

        todo.updated_at = datetime.utcnow()

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)

        return todo

    def delete(self, todo_id: UUID, user_id: UUID) -> bool:
        """
        Delete a todo with ownership verification.

        Args:
            todo_id: Todo ID
            user_id: Authenticated user ID from JWT

        Returns:
            True if deleted, False if not found/not owned

        CRITICAL: Returns False (404) if todo doesn't exist OR user doesn't own it
        """
        todo = self.get_by_id(todo_id, user_id)

        if not todo:
            return False

        self.session.delete(todo)
        self.session.commit()

        return True

    def toggle_completion(self, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """
        Toggle the completion status of a todo.

        Args:
            todo_id: Todo ID
            user_id: Authenticated user ID from JWT

        Returns:
            Updated todo if found and owned, None if not found/not owned

        CRITICAL: Returns None (404) if todo doesn't exist OR user doesn't own it
        """
        todo = self.get_by_id(todo_id, user_id)

        if not todo:
            return None

        todo.completed = not todo.completed
        todo.updated_at = datetime.utcnow()

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)

        return todo
