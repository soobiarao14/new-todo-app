"""
MCP tool implementations for task operations.
Phase III: Todo AI Chatbot - NEW FILE (does not modify Phase II)

SECURITY: user_id is NEVER passed from the AI agent.
It is ALWAYS injected from the authenticated JWT context.
"""
from dataclasses import dataclass
from typing import Optional, Callable, Any
from uuid import UUID
from sqlmodel import Session

from src.services.todo_service import TodoService
from src.schemas.todo import TodoCreateRequest, TodoUpdateRequest


class ToolError(Exception):
    """Standard error for MCP tool failures."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ToolContext:
    """
    Execution context for MCP tools.

    CRITICAL: user_id comes from JWT, NEVER from agent input.
    """

    user_id: UUID
    session: Session


# Tool registry for dynamic lookup
_TOOLS: dict[str, Callable] = {}


def mcp_tool(name: str):
    """Decorator to register an MCP tool."""

    def decorator(func: Callable) -> Callable:
        _TOOLS[name] = func
        func.tool_name = name
        return func

    return decorator


def get_all_tools() -> list[dict]:
    """
    Get tool definitions for OpenAI function calling.

    Returns:
        List of tool schemas in OpenAI function format.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Task title (1-200 characters)",
                        },
                        "description": {
                            "type": "string",
                            "description": "Task description (optional, max 2000 characters)",
                        },
                    },
                    "required": ["title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List user's tasks with optional status filter",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter by status: 'pending', 'completed', or 'all' (default: 'all')",
                        },
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "UUID of the task to complete",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task permanently. Use with caution - requires user confirmation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "UUID of the task to delete",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update task title and/or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "UUID of the task to update",
                        },
                        "title": {
                            "type": "string",
                            "description": "New task title (1-200 characters)",
                        },
                        "description": {
                            "type": "string",
                            "description": "New task description (max 2000 characters)",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
    ]


async def execute_tool(ctx: ToolContext, tool_name: str, parameters: dict) -> dict:
    """
    Execute an MCP tool by name.

    Args:
        ctx: Tool execution context (user_id from JWT, session)
        tool_name: Name of the tool to execute
        parameters: Tool parameters from agent

    Returns:
        Tool result dictionary

    Raises:
        ToolError: On validation or execution failure
    """
    if tool_name not in _TOOLS:
        raise ToolError("INVALID_TOOL", f"Unknown tool: {tool_name}")

    tool_func = _TOOLS[tool_name]
    return await tool_func(ctx, **parameters)


@mcp_tool("add_task")
async def add_task(
    ctx: ToolContext, title: str, description: Optional[str] = None
) -> dict:
    """
    Create a new task for the authenticated user.

    Args:
        ctx: Tool context with user_id from JWT
        title: Task title (1-200 characters)
        description: Optional task description

    Returns:
        Created task information
    """
    # Validation
    if not title or len(title.strip()) == 0:
        raise ToolError("VALIDATION_ERROR", "Title cannot be empty")
    if len(title) > 200:
        raise ToolError("VALIDATION_ERROR", "Title must be 1-200 characters")
    if description and len(description) > 2000:
        raise ToolError("VALIDATION_ERROR", "Description must be under 2000 characters")

    # Use Phase II TodoService
    service = TodoService(ctx.session)
    todo = service.create(
        user_id=ctx.user_id,  # FROM JWT, NOT FROM AGENT
        request=TodoCreateRequest(title=title.strip(), description=description),
    )

    return {
        "task_id": str(todo.id),
        "status": "created",
        "title": todo.title,
        "description": todo.description,
    }


@mcp_tool("list_tasks")
async def list_tasks(ctx: ToolContext, status: Optional[str] = "all") -> dict:
    """
    List tasks for the authenticated user with optional filtering.

    Args:
        ctx: Tool context with user_id from JWT
        status: Filter - "pending", "completed", or "all"

    Returns:
        Task list with counts
    """
    service = TodoService(ctx.session)
    all_tasks = service.list_by_user(ctx.user_id)

    # Filter by status
    if status == "pending":
        tasks = [t for t in all_tasks if not t.completed]
    elif status == "completed":
        tasks = [t for t in all_tasks if t.completed]
    else:
        tasks = all_tasks

    return {
        "tasks": [
            {
                "id": str(t.id),
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "created_at": t.created_at.isoformat(),
            }
            for t in tasks
        ],
        "total": len(all_tasks),
        "pending": len([t for t in all_tasks if not t.completed]),
        "completed": len([t for t in all_tasks if t.completed]),
    }


@mcp_tool("complete_task")
async def complete_task(ctx: ToolContext, task_id: str) -> dict:
    """
    Mark a task as completed.

    Args:
        ctx: Tool context with user_id from JWT
        task_id: UUID of the task to complete

    Returns:
        Completion result
    """
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        raise ToolError("VALIDATION_ERROR", "Invalid task ID format")

    service = TodoService(ctx.session)

    # Get task first to check current status
    task = service.get_by_id(task_uuid, ctx.user_id)
    if not task:
        raise ToolError("NOT_FOUND", "Task not found")

    if task.completed:
        return {
            "task_id": task_id,
            "status": "already_completed",
            "title": task.title,
        }

    # Toggle completion (will set to True)
    updated = service.toggle_completion(task_uuid, ctx.user_id)

    return {
        "task_id": task_id,
        "status": "completed",
        "title": updated.title,
    }


@mcp_tool("delete_task")
async def delete_task(ctx: ToolContext, task_id: str) -> dict:
    """
    Delete a task permanently.

    IMPORTANT: Agent MUST request user confirmation before calling this tool.

    Args:
        ctx: Tool context with user_id from JWT
        task_id: UUID of the task to delete

    Returns:
        Deletion result
    """
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        raise ToolError("VALIDATION_ERROR", "Invalid task ID format")

    service = TodoService(ctx.session)

    # Get task info before deletion
    task = service.get_by_id(task_uuid, ctx.user_id)
    if not task:
        raise ToolError("NOT_FOUND", "Task not found")

    title = task.title  # Save before deletion

    # Delete
    deleted = service.delete(task_uuid, ctx.user_id)
    if not deleted:
        raise ToolError("NOT_FOUND", "Task not found")

    return {
        "task_id": task_id,
        "status": "deleted",
        "title": title,
    }


@mcp_tool("update_task")
async def update_task(
    ctx: ToolContext,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> dict:
    """
    Update task title and/or description.

    Args:
        ctx: Tool context with user_id from JWT
        task_id: UUID of the task to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        Updated task information
    """
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        raise ToolError("VALIDATION_ERROR", "Invalid task ID format")

    if title is None and description is None:
        raise ToolError("VALIDATION_ERROR", "At least one field must be provided")

    if title is not None:
        if len(title.strip()) == 0:
            raise ToolError("VALIDATION_ERROR", "Title cannot be empty")
        if len(title) > 200:
            raise ToolError("VALIDATION_ERROR", "Title must be 1-200 characters")

    if description is not None and len(description) > 2000:
        raise ToolError("VALIDATION_ERROR", "Description must be under 2000 characters")

    service = TodoService(ctx.session)
    updated = service.update(
        task_uuid,
        ctx.user_id,
        TodoUpdateRequest(
            title=title.strip() if title else None, description=description
        ),
    )

    if not updated:
        raise ToolError("NOT_FOUND", "Task not found")

    return {
        "task_id": task_id,
        "status": "updated",
        "title": updated.title,
        "description": updated.description,
    }
