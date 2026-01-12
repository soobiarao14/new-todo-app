# Research: Phase I CLI Todo App

**Feature**: 001-phase-i-cli
**Date**: 2026-01-06
**Status**: Complete

## Research Summary

This document consolidates research findings for the Phase I CLI Todo application. All technical decisions are made with Phase I constraints in mind: Python 3.13+ standard library only, in-memory storage, beginner-friendly architecture, and no external dependencies.

---

## Research Area 1: In-Memory Data Storage for Python CLI Applications

**Question**: What is the most appropriate data structure for storing tasks in memory for a beginner-friendly CLI application?

**Research Findings**:

Python provides several built-in data structures suitable for in-memory storage:

1. **List**: Ordered collection, supports indexing, simple iteration
   - Lookup by ID: O(n) - requires linear search
   - Append: O(1) amortized
   - Delete: O(n) - requires finding item first, then removing

2. **Dictionary (id → Task)**: Key-value mapping
   - Lookup by ID: O(1) average case
   - Insert: O(1) average case
   - Delete: O(1) average case

3. **Custom data structure**: Could implement linked list, tree, etc.
   - More complex, not beginner-friendly
   - No performance benefit at Phase I scale

**Decision**: Use Python **list** to store Task objects

**Rationale**:
- Beginner-friendly and widely understood
- Simple iteration for "view all tasks" operation
- Linear search acceptable for Phase I scale (100 tasks max per spec)
- No external dependencies
- Aligns with constitution's "beginner-friendly architecture" principle
- Performance adequate: Even with 100 tasks, O(n) lookup is <1ms on modern hardware

**Alternatives Rejected**:
- Dictionary: Adds unnecessary complexity for marginal performance gain at Phase I scale
- Custom structures: Over-engineering, violates YAGNI and beginner-friendly principles

---

## Research Area 2: Task ID Generation Strategies

**Question**: How should unique task IDs be generated in a single-user, in-memory application?

**Research Findings**:

Common ID generation strategies:

1. **Auto-incrementing integer**: Counter starting at 1, increments on each add
   - Simple, deterministic, human-readable
   - IDs can be reused after deletion (requires tracking deleted IDs)
   - Or IDs never reused (simpler, counter only increments)

2. **UUID (Universally Unique Identifier)**: Random 128-bit identifier
   - Guarantees uniqueness across distributed systems
   - Complex for beginners (e.g., "550e8400-e29b-41d4-a716-446655440000")
   - Overkill for single-user, non-distributed application

3. **Hash-based**: Hash of task content (title + timestamp)
   - Non-deterministic due to timestamp
   - Collision risk (low but non-zero)
   - Harder to test deterministically

**Decision**: Use **auto-incrementing integer** starting from 1, never reusing IDs

**Rationale**:
- Specification explicitly requires "unique auto-incrementing integer ID starting from 1" (FR-003)
- Specification states "Task IDs are assigned sequentially and never reused (even after deletion)" (Assumptions section)
- Simple to implement: `self.next_id = 1`, increment after each add
- Deterministic for testing
- Human-readable for CLI users (ID 1, 2, 3... vs UUID gibberish)
- No external libraries needed

**Alternatives Rejected**:
- UUID: Violates beginner-friendly principle, unnecessary complexity
- Hash-based: Non-deterministic, conflicts with testing requirements
- Reusable IDs: Spec explicitly states IDs never reused

---

## Research Area 3: Separation of Concerns in Python Console Applications

**Question**: How should a beginner-friendly CLI application separate data, logic, and presentation?

**Research Findings**:

Common architectural patterns for console applications:

1. **Single-file monolith**: All code in one file
   - Simple to start
   - Hard to test, violates separation of concerns
   - Becomes unmaintainable as features grow

2. **Three-layer separation**: Data / Business Logic / Presentation
   - Data layer: Entity classes (e.g., Task)
   - Logic layer: Operations on entities (e.g., TaskManager)
   - Presentation layer: User I/O (e.g., CLI menu loop)
   - Clear boundaries, easy to test each layer independently

3. **MVC (Model-View-Controller)**: Formal design pattern
   - Overkill for simple CLI application
   - More complex than needed for Phase I

**Decision**: Use **three-module separation** (task.py, task_manager.py, todo_app.py)

**Rationale**:
- Constitution requires "clear separation of concerns" (Quality Principles IV)
- Enables independent unit testing of each layer
- Beginner-friendly: Each file has single, clear responsibility
- Modules:
  - `task.py`: Task data class (id, title, description, completed)
  - `task_manager.py`: Business logic (add, view, update, delete, toggle)
  - `todo_app.py`: CLI interaction (menu display, input handling, main loop)
- Follows Single Responsibility Principle without over-engineering

**Alternatives Rejected**:
- Monolith: Violates separation of concerns, hard to test
- MVC: Over-engineering for Phase I, not beginner-friendly

---

## Research Area 4: Error Handling Patterns in Python

**Question**: What is the most beginner-friendly error handling pattern for CLI applications?

**Research Findings**:

Python error handling approaches:

1. **Exceptions**: Raise and catch exceptions for error conditions
   - Pythonic and standard practice
   - Can be confusing for beginners (stack traces, try-except blocks)
   - Good for unexpected errors (e.g., file I/O, network)

2. **Return codes**: Return (success, message) tuples
   - Explicit and predictable
   - Caller must check return value
   - Common in C-style programming, less Pythonic

3. **Sentinel values**: Return None or special value on error
   - Loses error context (no message)
   - Caller must know what None means
   - Not beginner-friendly

**Decision**: Use **return tuple (success: bool, message: str)** for business logic errors; use **exceptions** only for unexpected errors

**Rationale**:
- Business logic errors are expected (e.g., task ID not found, empty title)
- Return tuple makes error handling explicit and traceable
- CLI layer can directly display message to user
- Beginner-friendly: Easy to see what succeeded and what failed
- Example: `(True, "Task added successfully")` or `(False, "Task ID not found")`
- Exceptions reserved for truly unexpected errors (e.g., out of memory)

**Alternatives Rejected**:
- Pure exceptions: Too much complexity for beginners, stack traces scary
- Sentinel values: Loses error message context

---

## Research Area 5: Input Validation for Python CLI Applications

**Question**: How should a CLI application validate and handle invalid user input?

**Research Findings**:

Input validation strategies:

1. **Try-except blocks**: Catch conversion errors (e.g., int("abc") raises ValueError)
   - Pythonic and standard
   - Handles all invalid inputs gracefully
   - Easy to re-prompt user

2. **Regex validation**: Use regular expressions to validate format
   - Overly complex for simple integer/string validation
   - Harder for beginners to understand

3. **Manual parsing**: Check each character manually
   - Reinvents the wheel
   - Error-prone, not Pythonic

**Decision**: Use **try-except blocks** with ValueError for numeric input validation

**Rationale**:
- Specification edge cases require handling "non-numeric input for menu selection" and "non-numeric input for task ID"
- Python's `int()` naturally raises `ValueError` on invalid input
- Simple pattern:
  ```python
  try:
      choice = int(input("Enter choice: "))
  except ValueError:
      print("Invalid input. Please enter a number.")
      continue
  ```
- Re-prompt on error (specification: "allow retry")
- Beginner-friendly and Pythonic

**Alternatives Rejected**:
- Regex: Overcomplicated for integer validation
- Manual parsing: Not Pythonic, error-prone

---

## Research Area 6: Testing Frameworks for Python (Standard Library Only)

**Question**: What testing framework should be used given Phase I constraint of standard library only?

**Research Findings**:

Python testing frameworks:

1. **unittest**: Built into Python standard library
   - TestCase classes with setUp/tearDown
   - Rich assertion methods (assertEqual, assertTrue, etc.)
   - Adequate for TDD workflow
   - More verbose than modern alternatives

2. **pytest**: Third-party framework (requires pip install)
   - More concise syntax
   - Better error messages
   - **Violates Phase I "no external dependencies" constraint**

3. **doctest**: Built into standard library
   - Embeds tests in docstrings
   - Good for simple examples
   - Too limited for comprehensive test coverage

**Decision**: Use **unittest** (standard library)

**Rationale**:
- Constitution requires "no external libraries" for Phase I (Technology Constraints III)
- unittest is built into Python 3.13+, no installation needed
- Supports TDD workflow (Red-Green-Refactor)
- Provides all necessary assertion methods
- Beginner-friendly with clear structure:
  ```python
  class TestTaskManager(unittest.TestCase):
      def setUp(self):
          self.manager = TaskManager()

      def test_add_task(self):
          success, msg = self.manager.add_task("Test", "Description")
          self.assertTrue(success)
  ```

**Alternatives Rejected**:
- pytest: Requires external dependency (Phase I violation)
- doctest: Too limited for comprehensive coverage

---

## Summary of Technical Decisions

| Decision Area | Choice | Rationale |
|---------------|--------|-----------|
| Data Structure | Python list | Simple, beginner-friendly, adequate performance at Phase I scale |
| ID Generation | Auto-incrementing integer | Spec requirement, deterministic, human-readable |
| Module Separation | 3 modules (task, manager, CLI) | Clear separation of concerns, testable, beginner-friendly |
| Error Handling | Return (bool, str) tuples | Explicit, beginner-friendly, provides error messages |
| Input Validation | Try-except with ValueError | Pythonic, handles all invalid inputs, allows retry |
| Testing Framework | unittest (standard library) | No external deps, supports TDD, beginner-friendly |

All decisions align with:
- ✅ Phase I specification requirements
- ✅ Constitution principles (beginner-friendly, no external deps, separation of concerns)
- ✅ Python 3.13+ standard library constraints
- ✅ Test-first development workflow

**Research Status**: ✅ Complete. All unknowns resolved. Ready for Phase 1 design artifacts.
