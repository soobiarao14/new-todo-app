# Todo CLI - Phase I

A simple, beginner-friendly command-line todo application built with Python. This is Phase I of the "Evolution of Todo" project, featuring in-memory task management with a menu-based interface.

## Features

- **Add Tasks**: Create tasks with a title and optional description
- **View Tasks**: Display all tasks with their details and completion status
- **Update Tasks**: Edit task titles and descriptions
- **Delete Tasks**: Remove tasks permanently
- **Toggle Completion**: Mark tasks as complete or incomplete
- **Menu-Based Interface**: Simple numbered menu for all operations

## Requirements

- Python 3.12 or higher
- No external dependencies (uses Python standard library only)

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd TODO-PHASE1
   ```

## Usage

Run the application from the command line:

```bash
python src/todo_app.py
```

### Main Menu

```
===== Todo App Menu =====
1. View all tasks
2. Add new task
3. Update task
4. Delete task
5. Toggle task complete/incomplete
6. Exit
==========================
```

### Example Workflow

1. **Add a task**:
   - Select option `2`
   - Enter title: "Buy groceries"
   - Enter description: "Milk, eggs, bread"

2. **View tasks**:
   - Select option `1`
   - See your task listed with ID, title, description, and status

3. **Mark task complete**:
   - Select option `5`
   - Enter task ID: `1`
   - Task is marked as complete

4. **Exit**:
   - Select option `6`

## Important Notes

- **In-Memory Only**: All tasks are stored in memory and will be lost when you exit the application
- **No Persistence**: This is Phase I - file and database persistence will be added in future phases
- **Single User**: Designed for single-user, single-session use

## Phase I Constraints

This implementation follows strict Phase I constraints:
- Python 3.12+ standard library only
- No external dependencies
- No file I/O or databases
- No web or API functionality
- Simple, beginner-friendly code

## Project Structure

```
TODO-PHASE1/
├── src/
│   ├── task.py           # Task data class
│   ├── task_manager.py   # Business logic (CRUD operations)
│   └── todo_app.py       # CLI interface (main entry point)
├── tests/
│   ├── test_task.py
│   ├── test_task_manager.py
│   └── test_integration.py
├── pyproject.toml
└── README.md
```

## Running Tests

Run all tests using Python's built-in unittest:

```bash
python -m unittest discover tests
```

## Documentation

For detailed specifications and design documents, see:
- `specs/001-phase-i-cli/spec.md` - Feature specification
- `specs/001-phase-i-cli/plan.md` - Implementation plan
- `specs/001-phase-i-cli/quickstart.md` - User guide

## Future Phases

Future phases will add:
- File persistence (Phase II)
- Database storage (Phase III)
- Web interface (Phase IV)
- Multi-user support (Phase V)

## License

This project is part of the "Evolution of Todo" educational series.
