---
description: "Task list for Phase I CLI Todo App implementation"
---

# Tasks: Phase I CLI Todo App

**Input**: Design documents from `specs/001-phase-i-cli/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli_operations.md

**Tests**: Tests are REQUIRED per constitution Test-First Development principle (V). All tests must be written FIRST before implementation (Red-Green-Refactor cycle).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure (src/, tests/)
- [ ] T002 Initialize Python 3.13+ virtual environment using UV
- [ ] T003 Create pyproject.toml with project metadata and dependencies (Python 3.13+ standard library only)
- [ ] T004 [P] Create README.md with project description and usage instructions

**References**:
- Spec: Out of Scope section (no external dependencies)
- Plan: Technical Context (Python 3.13+, UV, standard library only)
- Plan: Project Structure section

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create Task data class in src/task.py with attributes (id, title, description, completed)
- [ ] T006 [P] Write unit tests for Task class in tests/test_task.py (verify attribute initialization and defaults)
- [ ] T007 Create TaskManager class skeleton in src/task_manager.py with internal state (tasks list, next_id counter)
- [ ] T008 [P] Write unit tests for TaskManager initialization in tests/test_task_manager.py (verify empty list, next_id=1)

**References**:
- Spec: Key Entities section (Task attributes)
- Plan: Data Model section
- Data-Model: Entity Task, Storage TaskManager
- Contracts: TaskManager class structure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View Task List (Priority: P1) 🎯 MVP

**Goal**: Users can view all tasks with their details, even when the list is empty

**Independent Test**: Launch app, select "view tasks", verify task list displays correctly (shows "No tasks found" when empty, or formatted task list when tasks exist)

### Tests for User Story 1 (TDD - Red Phase) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Write unit test for view_tasks() with empty list in tests/test_task_manager.py
- [ ] T010 [P] [US1] Write unit test for view_tasks() with single task in tests/test_task_manager.py
- [ ] T011 [P] [US1] Write unit test for view_tasks() with multiple tasks (complete and incomplete) in tests/test_task_manager.py

**References**:
- Spec: User Story 1 acceptance scenarios
- Contracts: Operation 2 (view_tasks method signature and contract)

### Implementation for User Story 1 (Green Phase)

- [ ] T012 [US1] Implement view_tasks() method in src/task_manager.py (return "No tasks found" for empty list)
- [ ] T013 [US1] Add task formatting logic to view_tasks() in src/task_manager.py (show ID, title, description, status)
- [ ] T014 [US1] Create CLI menu skeleton in src/todo_app.py with main loop and menu display (options 1-6)
- [ ] T015 [US1] Implement menu option 1 (View tasks) in src/todo_app.py that calls TaskManager.view_tasks()
- [ ] T016 [US1] Add exit option (option 6) to CLI menu in src/todo_app.py

**References**:
- Spec: User Story 1, FR-005 (view all tasks), FR-012 (menu loop), FR-013 (handle empty list)
- Plan: CLI Control Flow section
- Contracts: Operation 2 (view_tasks)
- Data-Model: View Tasks Flow

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (view tasks and exit)

---

## Phase 4: User Story 2 - Add Task (Priority: P2)

**Goal**: Users can create new tasks with title and optional description

**Independent Test**: Launch app, add task with title, view list to confirm it appears with correct ID and status

### Tests for User Story 2 (TDD - Red Phase) ⚠️

- [ ] T017 [P] [US2] Write unit test for add_task() with valid title in tests/test_task_manager.py
- [ ] T018 [P] [US2] Write unit test for add_task() with title and description in tests/test_task_manager.py
- [ ] T019 [P] [US2] Write unit test for add_task() with empty title (should fail) in tests/test_task_manager.py
- [ ] T020 [P] [US2] Write unit test for add_task() with whitespace-only title (should fail) in tests/test_task_manager.py
- [ ] T021 [P] [US2] Write unit test to verify next_id increments correctly in tests/test_task_manager.py

**References**:
- Spec: User Story 2 acceptance scenarios
- Contracts: Operation 1 (add_task method signature and contract)

### Implementation for User Story 2 (Green Phase)

- [ ] T022 [US2] Implement add_task() method in src/task_manager.py with title validation (non-empty check)
- [ ] T023 [US2] Add task creation logic to add_task() in src/task_manager.py (create Task with next_id, append to list, increment counter)
- [ ] T024 [US2] Implement menu option 2 (Add task) in src/todo_app.py with input prompts for title and description
- [ ] T025 [US2] Add input validation for add task in src/todo_app.py (handle empty title, display error, allow retry)

**References**:
- Spec: User Story 2, FR-002 (add with title and description), FR-003 (auto-increment ID), FR-009 (validate title)
- Plan: Error Handling Strategy section
- Contracts: Operation 1 (add_task)
- Data-Model: Add Task Flow, Validation Rules

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (view and add tasks)

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P3)

**Goal**: Users can toggle tasks between complete and incomplete states

**Independent Test**: Create task, mark complete, view list to verify status changed, mark incomplete again to verify toggle

### Tests for User Story 3 (TDD - Red Phase) ⚠️

- [ ] T026 [P] [US3] Write unit test for toggle_complete() with valid task ID in tests/test_task_manager.py
- [ ] T027 [P] [US3] Write unit test for toggle_complete() toggling from False to True in tests/test_task_manager.py
- [ ] T028 [P] [US3] Write unit test for toggle_complete() toggling from True to False in tests/test_task_manager.py
- [ ] T029 [P] [US3] Write unit test for toggle_complete() with non-existent task ID in tests/test_task_manager.py
- [ ] T030 [P] [US3] Write unit test for toggle_complete() with empty task list in tests/test_task_manager.py

**References**:
- Spec: User Story 3 acceptance scenarios
- Contracts: Operation 5 (toggle_complete method signature and contract)

### Implementation for User Story 3 (Green Phase)

- [ ] T031 [US3] Implement toggle_complete() method in src/task_manager.py (find task by ID, toggle completed boolean)
- [ ] T032 [US3] Add error handling for non-existent task ID in toggle_complete() in src/task_manager.py
- [ ] T033 [US3] Implement menu option 5 (Toggle complete) in src/todo_app.py with input prompt for task ID
- [ ] T034 [US3] Add input validation for task ID in src/todo_app.py (handle non-numeric input with try-except)

**References**:
- Spec: User Story 3, FR-008 (toggle completion status), FR-010 (validate task ID exists)
- Plan: Input Validation Strategy section
- Contracts: Operation 5 (toggle_complete)
- Data-Model: Toggle Complete Flow, State Transitions

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task (Priority: P4)

**Goal**: Users can edit task title and description without deleting and recreating

**Independent Test**: Create task, update title and description, view list to verify changes persisted

### Tests for User Story 4 (TDD - Red Phase) ⚠️

- [ ] T035 [P] [US4] Write unit test for update_task() with valid task ID and new title in tests/test_task_manager.py
- [ ] T036 [P] [US4] Write unit test for update_task() with both new title and description in tests/test_task_manager.py
- [ ] T037 [P] [US4] Write unit test for update_task() with empty new title (should fail) in tests/test_task_manager.py
- [ ] T038 [P] [US4] Write unit test for update_task() with non-existent task ID in tests/test_task_manager.py
- [ ] T039 [P] [US4] Write unit test for update_task() with empty description (should succeed) in tests/test_task_manager.py

**References**:
- Spec: User Story 4 acceptance scenarios
- Contracts: Operation 3 (update_task method signature and contract)

### Implementation for User Story 4 (Green Phase)

- [ ] T040 [US4] Implement update_task() method in src/task_manager.py (find task by ID, validate new title, update fields)
- [ ] T041 [US4] Add error handling for non-existent task ID in update_task() in src/task_manager.py
- [ ] T042 [US4] Add error handling for empty new title in update_task() in src/task_manager.py
- [ ] T043 [US4] Implement menu option 3 (Update task) in src/todo_app.py with input prompts for ID, title, description
- [ ] T044 [US4] Add input validation for update task in src/todo_app.py (handle non-numeric ID, empty title)

**References**:
- Spec: User Story 4, FR-006 (update title and description), FR-009 (validate title), FR-010 (validate ID exists)
- Plan: Error Handling Strategy section
- Contracts: Operation 3 (update_task)
- Data-Model: Update Task Flow, Validation Rules

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Delete Task (Priority: P5)

**Goal**: Users can permanently remove tasks from the list

**Independent Test**: Create task, delete by ID, view list to verify it's gone

### Tests for User Story 5 (TDD - Red Phase) ⚠️

- [ ] T045 [P] [US5] Write unit test for delete_task() with valid task ID in tests/test_task_manager.py
- [ ] T046 [P] [US5] Write unit test for delete_task() with non-existent task ID in tests/test_task_manager.py
- [ ] T047 [P] [US5] Write unit test for delete_task() with empty task list in tests/test_task_manager.py
- [ ] T048 [P] [US5] Write unit test to verify next_id does NOT decrement after deletion in tests/test_task_manager.py

**References**:
- Spec: User Story 5 acceptance scenarios
- Contracts: Operation 4 (delete_task method signature and contract)

### Implementation for User Story 5 (Green Phase)

- [ ] T049 [US5] Implement delete_task() method in src/task_manager.py (find task by ID, remove from list)
- [ ] T050 [US5] Add error handling for non-existent task ID in delete_task() in src/task_manager.py
- [ ] T051 [US5] Implement menu option 4 (Delete task) in src/todo_app.py with input prompt for task ID
- [ ] T052 [US5] Add input validation for delete task in src/todo_app.py (handle non-numeric ID)

**References**:
- Spec: User Story 5, FR-007 (delete task by ID), FR-010 (validate ID exists), FR-013 (handle empty list)
- Plan: Task Identification Strategy section
- Contracts: Operation 4 (delete_task)
- Data-Model: Delete Task Flow

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T053 [P] Add comprehensive error handling for invalid menu choices in src/todo_app.py (handle non-numeric input, out of range)
- [ ] T054 [P] Write integration test for complete workflow (add → view → toggle → update → delete) in tests/test_integration.py
- [ ] T055 [P] Write edge case tests for very long titles/descriptions (1000+ chars) in tests/test_task_manager.py
- [ ] T056 [P] Write edge case tests for many tasks (100+) in tests/test_task_manager.py
- [ ] T057 Add graceful exit message "Goodbye!" to menu option 6 in src/todo_app.py
- [ ] T058 Add main entry point guard (if __name__ == "__main__":) to src/todo_app.py
- [ ] T059 [P] Update README.md with installation instructions, usage examples, and quickstart reference
- [ ] T060 Run all tests and verify 100% pass rate (pytest or python -m unittest discover)
- [ ] T061 Validate against all acceptance criteria from spec.md (all 5 user stories)

**References**:
- Spec: Edge Cases section, Success Criteria section
- Plan: Testing Strategy section
- Quickstart: All user scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4 → US5)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (but integrates with US1 for viewing added tasks)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (but requires tasks to exist, typically from US2)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories (but requires tasks to exist)
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories (but requires tasks to exist)

**Note**: While US2-US5 technically depend on having tasks to operate on, they are independently testable using programmatically created tasks in unit tests. For end-to-end testing, implement in priority order (P1 → P2 → P3 → P4 → P5).

### Within Each User Story

- Tests (Red phase) MUST be written and FAIL before implementation
- Implementation tasks run sequentially within a story
- Multiple test tasks within a story can run in parallel (all marked [P])

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user story TEST tasks can start in parallel
- Tests within a story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- Polish phase tasks marked [P] can run in parallel

---

## Parallel Example: User Story 2 (Add Task)

```bash
# Launch all tests for User Story 2 together (Red phase):
Task T017: "Write unit test for add_task() with valid title"
Task T018: "Write unit test for add_task() with title and description"
Task T019: "Write unit test for add_task() with empty title"
Task T020: "Write unit test for add_task() with whitespace-only title"
Task T021: "Write unit test to verify next_id increments"

# After tests fail, implement sequentially (Green phase):
Task T022 → T023 → T024 → T025
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (View tasks)
4. Complete Phase 4: User Story 2 (Add tasks)
5. **STOP and VALIDATE**: Test US1 + US2 independently
6. Deploy/demo if ready (minimal but functional todo app)

**MVP delivers**: View empty list, add tasks, view tasks with details, exit

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (can view tasks!)
3. Add User Story 2 → Test independently → Deploy/Demo (can add and view!)
4. Add User Story 3 → Test independently → Deploy/Demo (can toggle completion!)
5. Add User Story 4 → Test independently → Deploy/Demo (can update tasks!)
6. Add User Story 5 → Test independently → Deploy/Demo (full CRUD + toggle!)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (View)
   - Developer B: User Story 2 (Add)
   - Developer C: User Story 3 (Toggle)
3. Stories complete and integrate independently

---

## Task Counts by Phase

- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundational)**: 4 tasks
- **Phase 3 (US1 - View)**: 8 tasks (3 tests + 5 implementation)
- **Phase 4 (US2 - Add)**: 9 tasks (5 tests + 4 implementation)
- **Phase 5 (US3 - Toggle)**: 9 tasks (5 tests + 4 implementation)
- **Phase 6 (US4 - Update)**: 10 tasks (5 tests + 5 implementation)
- **Phase 7 (US5 - Delete)**: 8 tasks (4 tests + 4 implementation)
- **Phase 8 (Polish)**: 9 tasks (cross-cutting concerns)

**Total**: 61 tasks

**Parallel Opportunities**: 38 tasks marked [P] (62% can run in parallel within their phase)

---

## Notes

- [P] tasks = different files, no dependencies within their phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD MANDATORY**: Verify tests fail (Red) before implementing (Green)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

**Constitution Compliance**:
- ✅ Test-First Development: All implementation preceded by tests (Red-Green-Refactor)
- ✅ Phase Governance: No future phase features introduced
- ✅ Technology Constraints: Python 3.13+, standard library only
- ✅ Quality Principles: Clear separation (task.py, task_manager.py, todo_app.py)
- ✅ Workflow Discipline: Sequential phases with clear checkpoints
