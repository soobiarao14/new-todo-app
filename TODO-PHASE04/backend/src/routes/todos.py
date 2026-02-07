"""
Todos router with CRUD endpoints.
All endpoints enforce user isolation via JWT authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from src.schemas.todo import (
    TodoResponse,
    TodoListResponse,
    TodoCreateRequest,
    TodoUpdateRequest,
)
from src.services.todo_service import TodoService
from src.db import get_session
from src.dependencies import get_current_user_id

router = APIRouter()


def get_todo_service(session: Session = Depends(get_session)) -> TodoService:
    """Dependency to get TodoService instance."""
    return TodoService(session)


@router.get("", response_model=TodoListResponse)
async def list_todos(
    user_id: UUID = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service),
):
    """
    List all todos for the authenticated user.
    Orders by created_at descending (newest first).

    SECURITY: user_id comes from verified JWT, never from request parameters.
    """
    todos = todo_service.list_by_user(user_id)
    return TodoListResponse(
        todos=[TodoResponse.model_validate(todo) for todo in todos]
    )


@router.get("/{task_id}", response_model=TodoResponse)
async def get_todo(
    task_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service),
):
    """
    Get a single todo by ID.

    SECURITY: Returns 404 if todo doesn't exist OR user doesn't own it (prevents enumeration).
    """
    todo = todo_service.get_by_id(task_id, user_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Todo not found"}},
        )

    return TodoResponse.model_validate(todo)


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    request: TodoCreateRequest,
    user_id: UUID = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service),
):
    """
    Create a new todo for the authenticated user.

    SECURITY: user_id comes from verified JWT, never from request body.
    """
    todo = todo_service.create(user_id, request)
    return TodoResponse.model_validate(todo)


@router.put("/{task_id}", response_model=TodoResponse)
async def update_todo(
    task_id: UUID,
    request: TodoUpdateRequest,
    user_id: UUID = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service),
):
    """
    Update an existing todo.

    SECURITY: Returns 404 if todo doesn't exist OR user doesn't own it.
    """
    todo = todo_service.update(task_id, user_id, request)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Todo not found"}},
        )

    return TodoResponse.model_validate(todo)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    task_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service),
):
    """
    Delete a todo.

    SECURITY: Returns 404 if todo doesn't exist OR user doesn't own it.
    """
    success = todo_service.delete(task_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Todo not found"}},
        )

    return None


@router.patch("/{task_id}/complete", response_model=TodoResponse)
async def toggle_todo_completion(
    task_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service),
):
    """
    Toggle the completion status of a todo.

    SECURITY: Returns 404 if todo doesn't exist OR user doesn't own it.
    """
    todo = todo_service.toggle_completion(task_id, user_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Todo not found"}},
        )

    return TodoResponse.model_validate(todo)
