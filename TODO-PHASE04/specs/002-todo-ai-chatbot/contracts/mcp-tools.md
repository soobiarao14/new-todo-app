# MCP Tools Contract: Todo AI Chatbot

**Feature**: 002-todo-ai-chatbot
**Date**: 2026-01-20
**Status**: Complete

## Overview

This document defines the MCP (Model Context Protocol) tools that the AI agent can invoke to manage tasks. All tools enforce user isolation and operate through the existing Phase II `TodoService`.

---

## Security Model

**Critical Rules**:
1. `user_id` is NEVER passed from the AI agent
2. `user_id` is ALWAYS injected from the authenticated JWT context
3. Tools return 404-equivalent errors for unauthorized access (no enumeration)
4. All tool invocations are logged for audit trail

```python
# Tool execution context (injected by chat endpoint)
class ToolContext:
    user_id: UUID  # From JWT, NEVER from agent
    session: Session  # Database session
```

---

## Tool Definitions

### 1. add_task

**Purpose**: Create a new task for the authenticated user.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `title` | string | Yes | Task title (1-200 characters) |
| `description` | string | No | Task description (0-2000 characters) |

**Returns**:
```json
{
  "task_id": "uuid-string",
  "status": "created",
  "title": "string",
  "description": "string | null"
}
```

**Errors**:
| Error | Condition |
|-------|-----------|
| `VALIDATION_ERROR` | Title empty or too long |
| `VALIDATION_ERROR` | Description too long |

**Implementation**:
```python
@mcp_tool("add_task")
async def add_task(
    ctx: ToolContext,
    title: str,
    description: Optional[str] = None
) -> dict:
    # Validation
    if not title or len(title) > 200:
        raise ToolError("VALIDATION_ERROR", "Title must be 1-200 characters")
    if description and len(description) > 2000:
        raise ToolError("VALIDATION_ERROR", "Description must be under 2000 characters")

    # Use Phase II TodoService
    service = TodoService(ctx.session)
    todo = service.create(
        user_id=ctx.user_id,  # FROM JWT, NOT FROM AGENT
        request=TodoCreateRequest(title=title, description=description)
    )

    return {
        "task_id": str(todo.id),
        "status": "created",
        "title": todo.title,
        "description": todo.description
    }
```

---

### 2. list_tasks

**Purpose**: List tasks for the authenticated user with optional filtering.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `status` | string | No | Filter: "pending", "completed", or "all" (default: "all") |

**Returns**:
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "string",
      "description": "string | null",
      "completed": false,
      "created_at": "iso-datetime"
    }
  ],
  "total": 5,
  "pending": 3,
  "completed": 2
}
```

**Errors**: None (empty list is valid response)

**Implementation**:
```python
@mcp_tool("list_tasks")
async def list_tasks(
    ctx: ToolContext,
    status: Optional[str] = "all"
) -> dict:
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
                "created_at": t.created_at.isoformat()
            }
            for t in tasks
        ],
        "total": len(all_tasks),
        "pending": len([t for t in all_tasks if not t.completed]),
        "completed": len([t for t in all_tasks if t.completed])
    }
```

---

### 3. complete_task

**Purpose**: Mark a task as completed.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_id` | string (UUID) | Yes | Task ID to complete |

**Returns**:
```json
{
  "task_id": "uuid-string",
  "status": "completed",
  "title": "string"
}
```

**Errors**:
| Error | Condition |
|-------|-----------|
| `NOT_FOUND` | Task not found or not owned by user |
| `VALIDATION_ERROR` | Invalid task_id format |

**Implementation**:
```python
@mcp_tool("complete_task")
async def complete_task(
    ctx: ToolContext,
    task_id: str
) -> dict:
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
            "title": task.title
        }

    # Toggle completion (will set to True)
    updated = service.toggle_completion(task_uuid, ctx.user_id)

    return {
        "task_id": task_id,
        "status": "completed",
        "title": updated.title
    }
```

---

### 4. delete_task

**Purpose**: Delete a task permanently.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_id` | string (UUID) | Yes | Task ID to delete |

**Returns**:
```json
{
  "task_id": "uuid-string",
  "status": "deleted",
  "title": "string"
}
```

**Errors**:
| Error | Condition |
|-------|-----------|
| `NOT_FOUND` | Task not found or not owned by user |
| `VALIDATION_ERROR` | Invalid task_id format |

**Note**: Agent MUST request user confirmation before calling this tool (destructive action).

**Implementation**:
```python
@mcp_tool("delete_task")
async def delete_task(
    ctx: ToolContext,
    task_id: str
) -> dict:
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
        "title": title
    }
```

---

### 5. update_task

**Purpose**: Update task title and/or description.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_id` | string (UUID) | Yes | Task ID to update |
| `title` | string | No | New title (1-200 characters) |
| `description` | string | No | New description (0-2000 characters) |

**Note**: At least one of `title` or `description` must be provided.

**Returns**:
```json
{
  "task_id": "uuid-string",
  "status": "updated",
  "title": "string",
  "description": "string | null"
}
```

**Errors**:
| Error | Condition |
|-------|-----------|
| `NOT_FOUND` | Task not found or not owned by user |
| `VALIDATION_ERROR` | Invalid task_id format |
| `VALIDATION_ERROR` | No fields to update |
| `VALIDATION_ERROR` | Title/description length violation |

**Implementation**:
```python
@mcp_tool("update_task")
async def update_task(
    ctx: ToolContext,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        raise ToolError("VALIDATION_ERROR", "Invalid task ID format")

    if title is None and description is None:
        raise ToolError("VALIDATION_ERROR", "At least one field must be provided")

    if title is not None and (len(title) == 0 or len(title) > 200):
        raise ToolError("VALIDATION_ERROR", "Title must be 1-200 characters")

    if description is not None and len(description) > 2000:
        raise ToolError("VALIDATION_ERROR", "Description must be under 2000 characters")

    service = TodoService(ctx.session)
    updated = service.update(
        task_uuid,
        ctx.user_id,
        TodoUpdateRequest(title=title, description=description)
    )

    if not updated:
        raise ToolError("NOT_FOUND", "Task not found")

    return {
        "task_id": task_id,
        "status": "updated",
        "title": updated.title,
        "description": updated.description
    }
```

---

## Error Handling

All tools raise `ToolError` with standardized codes:

```python
class ToolError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

# Standard error codes
VALIDATION_ERROR = "VALIDATION_ERROR"  # Invalid input
NOT_FOUND = "NOT_FOUND"                # Resource not found (or unauthorized)
INTERNAL_ERROR = "INTERNAL_ERROR"      # Unexpected error
```

The chat endpoint catches `ToolError` and includes it in the response:

```json
{
  "tool_calls": [
    {
      "tool": "delete_task",
      "parameters": {"task_id": "invalid"},
      "result": {
        "error": {
          "code": "NOT_FOUND",
          "message": "Task not found"
        }
      },
      "success": false
    }
  ]
}
```

---

## Agent Tool Selection Prompt

The following prompt is used to instruct the agent on tool selection:

```text
You are a helpful task management assistant. You can help users manage their todo list using the following tools:

AVAILABLE TOOLS:
1. add_task(title, description?) - Create a new task
2. list_tasks(status?) - List tasks (status: "pending", "completed", or "all")
3. complete_task(task_id) - Mark a task as completed
4. delete_task(task_id) - Delete a task (REQUIRES USER CONFIRMATION)
5. update_task(task_id, title?, description?) - Update task details

RULES:
- For delete operations, ALWAYS ask the user to confirm before calling delete_task
- If a user's request is ambiguous, ask for clarification
- When listing tasks, summarize them in a readable format
- When multiple tasks match a description, list them and ask the user to specify
- Always confirm what action was taken after a successful tool call
- Handle errors gracefully with user-friendly explanations

EXAMPLES:
User: "Add a task to buy groceries"
→ Call add_task(title="buy groceries")

User: "What are my tasks?"
→ Call list_tasks()

User: "Mark the groceries task as done"
→ First call list_tasks() to find the task ID, then call complete_task(task_id)

User: "Delete the old meeting task"
→ First ask: "Are you sure you want to delete 'old meeting'? This cannot be undone."
→ Only call delete_task() after user confirms
```
