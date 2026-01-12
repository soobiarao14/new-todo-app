# Quickstart Guide: Phase I CLI Todo App

**Feature**: 001-phase-i-cli
**Date**: 2026-01-06
**Audience**: End users

## Overview

This guide walks you through using the Phase I Todo CLI application to manage your tasks. The application is a simple, menu-based command-line tool that stores tasks in memory during your session.

**Important**: All tasks are lost when you exit the application. This is by design for Phase I.

---

## Prerequisites

- Python 3.13 or higher installed
- Terminal or command prompt access

---

## Installation

### Step 1: Clone or Download the Repository

```bash
# Navigate to your project directory
cd /path/to/TODO-PHASE1
```

### Step 2: Verify Python Version

```bash
python --version
# Should show Python 3.13.x or higher
```

---

## Running the Application

### Launch the Todo App

```bash
python src/todo_app.py
```

You'll see the main menu:

```
===== Todo App Menu =====
1. View all tasks
2. Add new task
3. Update task
4. Delete task
5. Toggle task complete/incomplete
6. Exit
==========================
Enter your choice (1-6):
```

---

## Walkthrough: Common Tasks

### 1. Adding Your First Task

**Goal**: Create a new task with a title and optional description.

**Steps**:

1. From the main menu, enter `2` to select "Add new task"
2. When prompted for the title, type: `Buy groceries`
3. When prompted for the description, type: `Milk, eggs, bread`
4. Press Enter

**Expected Result**:
```
Task added successfully with ID 1
```

**Try It**:
- Add another task: `Call dentist` with description `Schedule annual checkup`
- Add a task without description: `Submit report` (press Enter when asked for description)

---

### 2. Viewing Your Tasks

**Goal**: See all your current tasks.

**Steps**:

1. From the main menu, enter `1` to select "View all tasks"

**Expected Result**:
```
[1] Title: Buy groceries
    Description: Milk, eggs, bread
    Status: Incomplete

[2] Title: Call dentist
    Description: Schedule annual checkup
    Status: Incomplete

[3] Title: Submit report
    Description:
    Status: Incomplete
```

**Note**: If you have no tasks, you'll see: `No tasks found`

---

### 3. Marking a Task as Complete

**Goal**: Change a task's status to "Complete".

**Steps**:

1. From the main menu, enter `5` to select "Toggle task complete/incomplete"
2. When prompted for task ID, enter: `1` (or the ID of the task you want to mark complete)

**Expected Result**:
```
Task marked as complete
```

**Verify**: View all tasks again (option `1`) and you'll see:
```
[1] Title: Buy groceries
    Description: Milk, eggs, bread
    Status: Complete
```

**Try It**:
- Toggle task 1 again to mark it incomplete
- Mark task 2 as complete

---

### 4. Updating a Task

**Goal**: Change a task's title or description.

**Steps**:

1. From the main menu, enter `3` to select "Update task"
2. When prompted for task ID, enter: `2`
3. When prompted for new title, type: `Call dentist - urgent`
4. When prompted for new description, type: `Schedule checkup ASAP`

**Expected Result**:
```
Task updated successfully
```

**Verify**: View all tasks (option `1`) to see the updated task.

---

### 5. Deleting a Task

**Goal**: Permanently remove a task from your list.

**Steps**:

1. From the main menu, enter `4` to select "Delete task"
2. When prompted for task ID, enter: `3`

**Expected Result**:
```
Task deleted successfully
```

**Verify**: View all tasks (option `1`) and task 3 will be gone.

**Note**: The task ID is gone permanently. If you add a new task, it will get ID 4 (not 3).

---

### 6. Exiting the Application

**Goal**: Close the application.

**Steps**:

1. From the main menu, enter `6` to select "Exit"

**Expected Result**:
```
Goodbye!
```

The application closes and all tasks are lost (Phase I behavior).

---

## Common Scenarios

### Scenario 1: Daily Task Management

```
1. Launch app
2. Add tasks for the day:
   - "Morning standup" (description: "Team sync at 9 AM")
   - "Code review" (description: "Review PR #42")
   - "Write documentation" (description: "Update README")
3. View all tasks to confirm
4. As you complete tasks, toggle them to "Complete"
5. View tasks at end of day to see what's done
6. Exit app
```

### Scenario 2: Quick Todo List

```
1. Launch app
2. Add 5 quick tasks (no descriptions needed):
   - "Email client"
   - "Fix bug #123"
   - "Lunch meeting prep"
   - "Update spreadsheet"
   - "Call supplier"
3. View all tasks
4. Mark completed tasks as you finish them
5. Delete completed tasks to keep list clean
6. Exit when done
```

---

## Handling Errors

### Error: "Task title cannot be empty"

**Cause**: You tried to add or update a task without providing a title.

**Solution**: Always provide a title when prompted. Titles are required; descriptions are optional.

**Example**:
```
Enter title: [Press Enter without typing]
❌ Task title cannot be empty
```

### Error: "Task ID not found"

**Cause**: You entered an ID that doesn't exist in your task list.

**Solution**: View all tasks (option 1) to see valid IDs, then retry the operation.

**Example**:
```
Enter task ID: 999
❌ Task ID not found
```

### Error: "Invalid input. Please enter a number between 1 and 6."

**Cause**: You entered something other than a number for the menu choice.

**Solution**: Enter only numbers 1-6 for menu options.

**Example**:
```
Enter your choice (1-6): abc
❌ Invalid input. Please enter a number between 1 and 6.
```

---

## Tips and Best Practices

1. **View tasks frequently**: Use option 1 to check your task list before updating or deleting tasks to confirm IDs.

2. **Keep titles concise**: Titles should be short summaries. Use descriptions for details.

3. **Use descriptions wisely**: Descriptions are optional but helpful for complex tasks.

4. **Don't rely on persistence**: Remember that all tasks are lost when you exit. Phase I is for learning and testing only.

5. **Task IDs are sequential**: New tasks always get the next available ID, even if you've deleted tasks.

---

## Troubleshooting

### Application won't start

**Problem**: `python src/todo_app.py` gives an error

**Solution**:
1. Verify Python version: `python --version` (should be 3.13+)
2. Verify you're in the project root directory
3. Check that `src/todo_app.py` exists

### Can't find my task

**Problem**: I added a task but it's not showing up

**Solution**:
1. View all tasks (option 1) to see complete list
2. Verify you didn't accidentally delete it (option 4)
3. Check if you exited and restarted the app (tasks are lost on exit)

### Task IDs seem wrong

**Problem**: I deleted task 2 but new tasks start at ID 4 instead of 2

**Solution**: This is correct behavior. Task IDs are never reused for data integrity. New tasks always get the next sequential ID.

---

## Next Steps

**For Users**:
- Experiment with all five operations (add, view, update, delete, toggle)
- Try edge cases (empty descriptions, long titles, many tasks)
- Provide feedback on usability and error messages

**For Developers**:
- Phase II will add file persistence so tasks aren't lost on exit
- Phase III may add features like task categories, priorities, and search
- See specification for planned features

---

## Summary

You now know how to:
- ✅ Add tasks with titles and optional descriptions
- ✅ View all your tasks
- ✅ Mark tasks as complete or incomplete
- ✅ Update task details
- ✅ Delete tasks
- ✅ Handle common errors

**Remember**: All tasks are in-memory only and will be lost when you exit the application. This is Phase I behavior by design.

**Questions or Issues?**: Refer to the specification (`specs/001-phase-i-cli/spec.md`) for detailed requirements and acceptance criteria.
