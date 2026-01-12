# Implementation Plan: Phase I CLI Todo App

**Branch**: `001-phase-i-cli` | **Date**: 2026-01-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-phase-i-cli/spec.md`

## Summary

Phase I delivers a beginner-friendly, in-memory Python console application for managing todo tasks. Users interact via a menu-based CLI to perform CRUD operations (Create, Read, Update, Delete) and toggle task completion status. All data is stored in memory during runtime with no persistence. The implementation prioritizes simplicity, clean separation of concerns, and adherence to constitution principles (Python 3.13+, standard library only, test-first development).

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (no external packages)
**Storage**: In-memory (Python list data structure)
**Testing**: Python unittest (standard library)
**Target Platform**: Cross-platform console (Windows, macOS, Linux)
**Project Type**: Single console application
**Performance Goals**: <1 second response time for all operations with up to 100 tasks
**Constraints**: No file I/O, no databases, no external services, no GUI
**Scale/Scope**: Single-user, session-scoped, supports 100+ tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Specification-Driven Development ✅

- Plan derived strictly from approved spec.md
- No new features introduced beyond specification
- All design decisions traceable to functional requirements

### II. Phase Governance ✅

- Implementation scoped to Phase I only
- No persistence mechanisms (reserved for Phase II)
- No web/API concepts (reserved for future phases)
- No external libraries (Phase I constraint)

### III. Technology Constraints ✅

- Python 3.13+ (compliant)
- UV for environment management (will be configured)
- Standard library only (compliant - no external dependencies)
- No FastAPI, databases, or web frameworks (Phase I exclusion)

### IV. Quality Principles ✅

- Clean separation: Task logic vs CLI interaction
- Self-documenting code with clear function names
- Deterministic behavior (no random IDs, no hidden state)
- Explicit error handling for all edge cases
- Beginner-friendly patterns (simple classes, minimal abstraction)

### V. Test-First Development ✅

- TDD mandatory for all implementation
- Tests written before code
- Red-Green-Refactor cycle enforced
- Tests will use Python unittest framework

### VI. Workflow Discipline ✅

- Spec → Plan → Tasks → Test → Implement → Refactor → Validate
- This plan follows specification strictly
- Tasks.md will define concrete implementation steps
- No backtracking or ad-hoc changes

**Constitution Check Result**: ✅ PASSED - No violations. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-i-cli/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── cli_operations.md  # CLI operation signatures
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── todo_app.py          # Main entry point with CLI loop
├── task_manager.py      # Task business logic (CRUD operations)
└── task.py              # Task data class

tests/
├── test_task.py         # Unit tests for Task class
├── test_task_manager.py # Unit tests for TaskManager operations
└── test_integration.py  # Integration tests for full workflows

pyproject.toml           # UV project configuration
README.md                # User-facing documentation
```

**Structure Decision**: Single project structure selected. This is a standalone console application with no web, mobile, or API components. All source code lives in `src/` with corresponding tests in `tests/`. This aligns with Phase I simplicity constraints and beginner-friendly architecture principles.

## Complexity Tracking

**No violations detected.** Constitution check passed all gates. No complexity justification required.

---

## Phase 0: Research & Technical Decisions

### Decision 1: In-Memory Data Structure

**Decision**: Use Python list to store Task objects

**Rationale**:
- Spec requires in-memory storage (FR-004)
- List provides O(n) lookup by ID, acceptable for Phase I scale (100 tasks)
- Simple and beginner-friendly
- No external dependencies needed

**Alternatives Considered**:
- Dictionary (id → Task): Faster lookup but adds unnecessary complexity for Phase I
- SQLite in-memory: Violates "no database" constraint for Phase I

**Trade-offs**:
- Pro: Simple, readable, no dependencies
- Con: Linear search for task lookup (acceptable at Phase I scale)

### Decision 2: Task ID Generation Strategy

**Decision**: Auto-incrementing integer counter starting from 1

**Rationale**:
- Spec requires unique auto-incrementing IDs (FR-003)
- Simple counter guarantees uniqueness and sequential ordering
- IDs never reused (even after deletion) per spec assumptions
- Deterministic and predictable for testing

**Alternatives Considered**:
- UUID: Overly complex for Phase I, not beginner-friendly
- Hash-based: Non-deterministic, harder to test

**Trade-offs**:
- Pro: Simple, deterministic, human-readable
- Con: IDs not reused after deletion (acceptable per spec)

### Decision 3: Module Separation Strategy

**Decision**: Three-module design (task.py, task_manager.py, todo_app.py)

**Rationale**:
- Follows constitution's "clear separation of concerns" principle
- task.py: Data representation only
- task_manager.py: Business logic (CRUD operations)
- todo_app.py: CLI interaction and user I/O
- Enables independent unit testing of each layer

**Alternatives Considered**:
- Single-file monolith: Violates separation of concerns
- More granular modules: Over-engineering for Phase I scope

**Trade-offs**:
- Pro: Clean boundaries, testable, maintainable
- Con: Slightly more files (acceptable for clarity)

### Decision 4: Error Handling Strategy

**Decision**: Return tuple (success: bool, message: str) from TaskManager methods

**Rationale**:
- Spec requires clear error messages (FR-011)
- Simple pattern: (True, "Success message") or (False, "Error message")
- CLI layer displays messages directly to user
- No exceptions for business logic errors (saves beginner complexity)

**Alternatives Considered**:
- Exceptions: More Pythonic but harder for beginners to trace
- Return None on error: Loses error message context

**Trade-offs**:
- Pro: Explicit, beginner-friendly, clear error messages
- Con: Caller must check success flag (acceptable with clear pattern)

### Decision 5: CLI Input Validation Strategy

**Decision**: Try-except for numeric conversions, loop until valid input

**Rationale**:
- Edge cases require handling non-numeric input (spec edge cases)
- Python's int() raises ValueError on invalid input
- Re-prompt on error (spec: "allow retry")
- Graceful handling without crashes

**Alternatives Considered**:
- Regex validation: Overcomplicated for simple integer checks
- Exit on error: Violates "allow retry" requirement

**Trade-offs**:
- Pro: Pythonic, handles all invalid inputs gracefully
- Con: None identified

### Decision 6: Testing Framework

**Decision**: Python unittest (standard library)

**Rationale**:
- Constitution requires standard library only for Phase I
- unittest is built-in, no external dependencies
- Sufficient for TDD workflow (Red-Green-Refactor)
- Beginner-friendly with clear assertion methods

**Alternatives Considered**:
- pytest: More powerful but external dependency (Phase I violation)
- doctest: Too limited for comprehensive test coverage

**Trade-offs**:
- Pro: No dependencies, beginner-friendly, adequate for scope
- Con: More verbose than pytest (acceptable for Phase I)

---

## Phase 1: Design Artifacts

### Data Model

See [data-model.md](./data-model.md) for detailed entity design.

**Summary**:
- Task entity with 4 attributes (id, title, description, completed)
- TaskManager maintains list of Tasks and next_id counter
- No relationships (single entity model)
- Validation rules embedded in TaskManager methods

### CLI Operation Contracts

See [contracts/cli_operations.md](./contracts/cli_operations.md) for method signatures.

**Summary**:
- TaskManager exposes 5 public methods (add, view, update, delete, toggle)
- Each method returns (success: bool, message: str)
- Input validation happens in TaskManager layer
- CLI layer handles user I/O and calls TaskManager methods

### Application Flow

See [quickstart.md](./quickstart.md) for user-facing walkthrough.

**Summary**:
1. User launches todo_app.py
2. Main loop displays menu with 6 options (view, add, update, delete, toggle, exit)
3. User selects option by number
4. Application calls appropriate TaskManager method
5. Result message displayed to user
6. Loop continues until user selects exit

---

## Phase 2: Implementation Planning

**Note**: Detailed tasks will be generated by `/sp.tasks` command. This section provides high-level implementation guidance.

### Implementation Approach

1. **TDD Workflow**: Write tests first for each module, ensure they fail (Red), implement to pass (Green), refactor for clarity
2. **Bottom-up Construction**: Task class → TaskManager logic → CLI integration
3. **Incremental Validation**: Each user story implemented and tested independently (P1 → P2 → P3 → P4 → P5)

### Key Implementation Principles

- **No Premature Optimization**: Focus on correctness and readability over performance
- **Explicit Over Implicit**: All error cases handled explicitly with clear messages
- **Single Responsibility**: Each function/method does one thing well
- **No Magic Numbers**: Use named constants for menu options and messages

### Testing Strategy

- **Unit Tests**: Test Task class, TaskManager methods in isolation
- **Integration Tests**: Test full workflows (menu → operation → result)
- **Edge Case Coverage**: Empty list, invalid IDs, empty titles, non-numeric input
- **Test Data**: Use realistic task titles/descriptions in tests

### Expected Challenges

1. **Input Validation**: Handling all edge cases gracefully (mitigation: comprehensive try-except blocks)
2. **State Management**: Keeping task list and next_id in sync (mitigation: encapsulate in TaskManager)
3. **User Experience**: Clear menu and error messages (mitigation: user testing with quickstart.md)

---

## Architectural Decision Records (ADRs)

No architecturally significant decisions requiring ADRs were identified. All design choices are straightforward applications of:
- Python standard patterns (classes, lists, loops)
- Constitution principles (separation of concerns, no external deps)
- Specification requirements (in-memory, CLI, CRUD operations)

If future phases introduce frameworks, persistence, or API design, those will warrant ADR documentation.

---

## Next Steps

1. ✅ Plan complete (this document)
2. ⏭️ Run `/sp.tasks` to generate detailed implementation tasks
3. ⏭️ Implement tests (Red phase)
4. ⏭️ User approval of test cases
5. ⏭️ Implement code (Green phase)
6. ⏭️ Refactor for clarity (Refactor phase)
7. ⏭️ Validate against acceptance criteria

**Plan Status**: ✅ Ready for task generation
