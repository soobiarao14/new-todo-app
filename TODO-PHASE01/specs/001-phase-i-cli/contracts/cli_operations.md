# CLI Operations Contract: Phase I CLI Todo App

**Feature**: 001-phase-i-cli
**Date**: 2026-01-06
**Status**: Complete

## Overview

This document defines the method signatures and contracts for the TaskManager class, which implements all business logic for task management. The CLI layer (todo_app.py) calls these methods and displays results to the user.

---

## Module: task_manager.py

### Class: TaskManager

**Purpose**: Manages in-memory task collection and provides CRUD operations.

**Internal State**:
- `tasks: list[Task]` - List of all tasks
- `next_id: int` - Counter for generating unique IDs

---

## Operation 1: Add Task

### Method Signature

```python
def add_task(self, title: str, description: str = "") -> tuple[bool, str]:
    """
    Add a new task to the task list.

    Args:
        title: Task title (required, must be non-empty)
        description: Task description (optional, defaults to empty string)

    Returns:
        Tuple of (success: bool, message: str)
        - On success: (True, "Task added successfully with ID {id}")
        - On failure: (False, "Task title cannot be empty")

    Side Effects:
        - Appends new Task to tasks list
        - Increments next_id counter
    """
```

### Contract

**Preconditions**:
- title must be a string
- description must be a string (can be empty)

**Postconditions**:
- If title is non-empty:
  - New Task created with id=next_id, completed=False
  - Task appended to tasks list
  - next_id incremented by 1
  - Returns (True, success message with task ID)
- If title is empty or whitespace-only:
  - No task created
  - tasks list unchanged
  - next_id unchanged
  - Returns (False, error message)

**Error Cases**:
- Empty title: `(False, "Task title cannot be empty")`
- Whitespace-only title: `(False, "Task title cannot be empty")`

---

## Operation 2: View Tasks

### Method Signature

```python
def view_tasks(self) -> tuple[bool, str]:
    """
    Retrieve all tasks formatted for display.

    Returns:
        Tuple of (success: bool, message: str)
        - If tasks exist: (True, formatted string with all task details)
        - If no tasks: (True, "No tasks found")

    Side Effects:
        None (read-only operation)
    """
```

### Contract

**Preconditions**:
- None

**Postconditions**:
- If tasks list is empty:
  - Returns (True, "No tasks found")
- If tasks list has items:
  - Returns (True, formatted string containing all tasks)
  - Format per task:
    ```
    [ID] Title: {title}
        Description: {description}
        Status: {Completed/Incomplete}
    ```

**Error Cases**:
- None (always succeeds)

---

## Operation 3: Update Task

### Method Signature

```python
def update_task(self, task_id: int, new_title: str, new_description: str = "") -> tuple[bool, str]:
    """
    Update an existing task's title and description.

    Args:
        task_id: ID of task to update
        new_title: New title (required, must be non-empty)
        new_description: New description (optional, defaults to empty string)

    Returns:
        Tuple of (success: bool, message: str)
        - On success: (True, "Task updated successfully")
        - On failure: (False, error message)

    Side Effects:
        - Updates task.title and task.description in tasks list
    """
```

### Contract

**Preconditions**:
- task_id must be an integer
- new_title must be a string
- new_description must be a string (can be empty)

**Postconditions**:
- If task_id exists AND new_title is non-empty:
  - Task with matching ID has title updated to new_title
  - Task with matching ID has description updated to new_description
  - Returns (True, "Task updated successfully")
- If task_id does not exist:
  - No tasks modified
  - Returns (False, "Task ID not found")
- If new_title is empty or whitespace-only:
  - No tasks modified
  - Returns (False, "Task title cannot be empty")

**Error Cases**:
- Task ID not found: `(False, "Task ID not found")`
- Empty new title: `(False, "Task title cannot be empty")`
- Whitespace-only new title: `(False, "Task title cannot be empty")`

---

## Operation 4: Delete Task

### Method Signature

```python
def delete_task(self, task_id: int) -> tuple[bool, str]:
    """
    Permanently remove a task from the task list.

    Args:
        task_id: ID of task to delete

    Returns:
        Tuple of (success: bool, message: str)
        - On success: (True, "Task deleted successfully")
        - On failure: (False, "Task ID not found")

    Side Effects:
        - Removes task from tasks list
        - Does NOT decrement next_id (IDs never reused)
    """
```

### Contract

**Preconditions**:
- task_id must be an integer

**Postconditions**:
- If task_id exists:
  - Task with matching ID removed from tasks list
  - next_id unchanged (IDs never reused)
  - Returns (True, "Task deleted successfully")
- If task_id does not exist:
  - tasks list unchanged
  - Returns (False, "Task ID not found")

**Error Cases**:
- Task ID not found: `(False, "Task ID not found")`

---

## Operation 5: Toggle Task Complete

### Method Signature

```python
def toggle_complete(self, task_id: int) -> tuple[bool, str]:
    """
    Toggle a task's completion status between complete and incomplete.

    Args:
        task_id: ID of task to toggle

    Returns:
        Tuple of (success: bool, message: str)
        - On success: (True, "Task marked as complete") or (True, "Task marked as incomplete")
        - On failure: (False, "Task ID not found")

    Side Effects:
        - Toggles task.completed boolean (True ↔ False)
    """
```

### Contract

**Preconditions**:
- task_id must be an integer

**Postconditions**:
- If task_id exists:
  - Task's completed status toggled (True → False or False → True)
  - Returns (True, "Task marked as complete") if new status is True
  - Returns (True, "Task marked as incomplete") if new status is False
- If task_id does not exist:
  - No tasks modified
  - Returns (False, "Task ID not found")

**Error Cases**:
- Task ID not found: `(False, "Task ID not found")`

---

## Module: task.py

### Class: Task

**Purpose**: Data class representing a single todo item.

### Constructor

```python
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique integer identifier
        title: Non-empty string describing the task
        description: String with optional details (can be empty)
        completed: Boolean completion status
    """

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a Task instance.

        Args:
            task_id: Unique integer ID (assigned by TaskManager)
            title: Task title (must be non-empty, validated by TaskManager)
            description: Optional task description (defaults to empty string)
            completed: Completion status (defaults to False)
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
```

**Note**: Task class performs NO validation. All validation happens in TaskManager layer.

---

## Module: todo_app.py

### Main Loop Structure

```python
def main():
    """
    Main CLI loop.

    Displays menu, handles user input, calls TaskManager methods,
    and displays results.
    """
    manager = TaskManager()

    while True:
        # Display menu
        # Get user choice
        # Call appropriate TaskManager method
        # Display result
        # Continue loop until user chooses exit
```

### Menu Options

```
Todo App Menu:
1. View all tasks
2. Add new task
3. Update task
4. Delete task
5. Toggle task complete/incomplete
6. Exit
```

### Input Handling Pattern

```python
try:
    choice = int(input("Enter your choice (1-6): "))
except ValueError:
    print("Invalid input. Please enter a number between 1 and 6.")
    continue
```

---

## Error Message Standards

All error messages must be clear, actionable, and user-friendly:

| Error Condition | Message |
|-----------------|---------|
| Empty task title | "Task title cannot be empty" |
| Task ID not found | "Task ID not found" |
| Invalid menu choice | "Invalid choice. Please enter a number between 1 and 6." |
| Non-numeric menu input | "Invalid input. Please enter a number between 1 and 6." |
| Non-numeric task ID input | "Invalid input. Please enter a valid task ID." |

---

## Success Message Standards

| Operation | Message |
|-----------|---------|
| Add task | "Task added successfully with ID {id}" |
| View tasks (none) | "No tasks found" |
| View tasks (exists) | [Formatted task list] |
| Update task | "Task updated successfully" |
| Delete task | "Task deleted successfully" |
| Toggle complete (to True) | "Task marked as complete" |
| Toggle complete (to False) | "Task marked as incomplete" |

---

## Testing Contract Compliance

Each method contract must be verified with unit tests:

1. **Precondition Tests**: Verify behavior with valid and invalid inputs
2. **Postcondition Tests**: Verify state changes and return values
3. **Error Case Tests**: Verify all error paths return correct error messages
4. **Side Effect Tests**: Verify internal state (tasks list, next_id) changes correctly

---

## Summary

- **5 public methods** in TaskManager (add, view, update, delete, toggle)
- **Consistent return pattern**: All methods return `(bool, str)` tuple
- **No exceptions for business logic**: All expected errors handled via return tuples
- **Clear error messages**: User-friendly, actionable error text
- **Stateless CLI layer**: All state managed in TaskManager

**Status**: ✅ Contracts complete and ready for implementation.
