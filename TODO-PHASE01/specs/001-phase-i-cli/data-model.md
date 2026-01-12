# Data Model: Phase I CLI Todo App

**Feature**: 001-phase-i-cli
**Date**: 2026-01-06
**Status**: Complete

## Overview

Phase I uses a simple, single-entity data model with no relationships. All data is stored in memory using Python's built-in list data structure. This design prioritizes beginner-friendliness and aligns with Phase I constraints (no databases, no persistence).

---

## Entity: Task

**Purpose**: Represents a single todo item with title, description, and completion status.

### Attributes

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | int | Yes | Auto-assigned | Unique, auto-incrementing, starts at 1 | Unique identifier for the task |
| `title` | str | Yes | N/A | Non-empty string | Brief description of what needs to be done |
| `description` | str | No | Empty string `""` | Any string (can be empty) | Optional detailed information about the task |
| `completed` | bool | Yes | `False` | True or False | Indicates whether the task has been completed |

### Validation Rules

1. **id**:
   - Auto-assigned by TaskManager
   - Never set by user
   - Must be unique across all tasks
   - Increments sequentially (1, 2, 3, ...)
   - Never reused (even after task deletion)

2. **title**:
   - MUST NOT be empty string
   - MUST NOT be whitespace-only (e.g., "   ")
   - Length: No arbitrary limit (constrained only by memory)
   - Validation: Performed by TaskManager before create/update

3. **description**:
   - MAY be empty string (optional field)
   - Length: No arbitrary limit
   - No validation required (any string accepted)

4. **completed**:
   - MUST be boolean (True or False)
   - Defaults to False for new tasks
   - Toggled via dedicated operation (no direct setting)

### State Transitions

```
[New Task]
    ↓
[created] → completed = False
    ↓
[toggle_complete] → completed = True
    ↓
[toggle_complete] → completed = False
    ↓
[cycle continues...]
```

### Invariants

- A task MUST always have a non-empty title
- A task MUST always have a unique ID
- A task's completed status is always boolean (never None/null)
- A task's ID never changes after creation

---

## Storage: TaskManager

**Purpose**: Manages the in-memory collection of Task objects and provides CRUD operations.

### Internal State

| Attribute | Type | Description |
|-----------|------|-------------|
| `tasks` | list[Task] | Ordered list of all Task objects in memory |
| `next_id` | int | Counter for generating unique task IDs (starts at 1) |

### State Initialization

```python
tasks = []        # Empty list at startup
next_id = 1       # First task gets ID 1
```

### Operations

See [contracts/cli_operations.md](./contracts/cli_operations.md) for detailed method signatures.

---

## Data Flow

### Add Task Flow

```
User Input (title, description)
    ↓
TaskManager.add_task()
    ↓
Validate title (non-empty)
    ↓
Create Task(id=next_id, title, description, completed=False)
    ↓
Append to tasks list
    ↓
Increment next_id
    ↓
Return (True, "Task added successfully")
```

### View Tasks Flow

```
User requests view
    ↓
TaskManager.view_tasks()
    ↓
Check if tasks list is empty
    ↓
If empty: Return (True, "No tasks found")
    ↓
If not empty: Format each task as string
    ↓
Return (True, formatted_task_list)
```

### Update Task Flow

```
User Input (task_id, new_title, new_description)
    ↓
TaskManager.update_task()
    ↓
Find task in tasks list by ID
    ↓
If not found: Return (False, "Task ID not found")
    ↓
Validate new_title (non-empty)
    ↓
If invalid: Return (False, "Task title cannot be empty")
    ↓
Update task.title and task.description
    ↓
Return (True, "Task updated successfully")
```

### Delete Task Flow

```
User Input (task_id)
    ↓
TaskManager.delete_task()
    ↓
Find task in tasks list by ID
    ↓
If not found: Return (False, "Task ID not found")
    ↓
Remove task from tasks list
    ↓
Return (True, "Task deleted successfully")
```

### Toggle Complete Flow

```
User Input (task_id)
    ↓
TaskManager.toggle_complete()
    ↓
Find task in tasks list by ID
    ↓
If not found: Return (False, "Task ID not found")
    ↓
Toggle task.completed (True ↔ False)
    ↓
Return (True, "Task marked as [complete/incomplete]")
```

---

## Relationships

**None**: Phase I has a single entity (Task) with no relationships. Future phases may introduce:
- Task categories (one-to-many: Category → Tasks)
- User ownership (one-to-many: User → Tasks)
- Task dependencies (many-to-many: Task ↔ Task)

These are explicitly out of scope for Phase I.

---

## Persistence Strategy

**Phase I**: No persistence. All data lost when application exits.

**Rationale**:
- Specification explicitly excludes file and database persistence (FR-004, Out of Scope)
- Keeps Phase I simple and beginner-friendly
- Future phases will introduce persistence mechanisms

---

## Performance Considerations

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Add Task | O(1) | Append to list |
| View Tasks | O(n) | Iterate through all tasks |
| Update Task | O(n) | Linear search for task by ID |
| Delete Task | O(n) | Linear search + removal |
| Toggle Complete | O(n) | Linear search for task by ID |

### Space Complexity

- **Storage**: O(n) where n = number of tasks
- **Acceptable for Phase I**: Spec targets 100 tasks max (SC-007)
- **Memory usage**: ~100 bytes per task × 100 tasks = ~10 KB (negligible)

### Scalability Notes

- Linear search (O(n)) is acceptable for Phase I scale
- If future phases require better performance (e.g., 10,000+ tasks), consider:
  - Dictionary-based storage (id → Task) for O(1) lookup
  - Database with indexed queries
  - These optimizations are deferred to future phases

---

## Testing Considerations

### Unit Test Coverage

1. **Task Creation**:
   - Verify all attributes set correctly
   - Verify default values (completed=False, description="")

2. **TaskManager Operations**:
   - Add: Valid title, empty title, optional description
   - View: Empty list, single task, multiple tasks
   - Update: Existing ID, non-existent ID, empty title, valid update
   - Delete: Existing ID, non-existent ID, empty list
   - Toggle: Existing ID, non-existent ID, verify state change

3. **Edge Cases**:
   - Very long titles/descriptions (1000+ chars)
   - Many tasks (100+)
   - Deleting and re-adding tasks (verify ID increments)

### Test Data Examples

```python
# Valid task
Task(id=1, title="Buy groceries", description="Milk, eggs, bread", completed=False)

# Minimal task (no description)
Task(id=2, title="Call dentist", description="", completed=False)

# Completed task
Task(id=3, title="Submit report", description="Q4 financial summary", completed=True)
```

---

## Summary

- **Single entity**: Task (id, title, description, completed)
- **Storage**: Python list in TaskManager
- **No relationships**: Single-entity model
- **No persistence**: In-memory only
- **Validation**: Non-empty title enforced
- **Performance**: O(n) operations acceptable at Phase I scale (100 tasks)

**Status**: ✅ Data model complete and ready for implementation.
