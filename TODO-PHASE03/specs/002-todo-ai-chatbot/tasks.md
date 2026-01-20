# Tasks: Todo AI Chatbot

**Input**: Design documents from `/specs/002-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the feature specification. Test tasks omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Phase III dependencies

- [X] T001 Install OpenAI SDK dependency in backend/pyproject.toml (`openai>=1.0.0`)
- [X] T002 [P] Install MCP SDK dependency in backend/pyproject.toml (`mcp>=0.1.0`)
- [X] T003 [P] Add OPENAI_API_KEY and OPENAI_MODEL to backend/.env.example
- [X] T004 Verify Phase II backend runs without errors before Phase III changes

**Checkpoint**: Dependencies installed, Phase II verified stable

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models (Required by ALL stories)

- [X] T005 [P] Create Conversation model in backend/src/models/conversation.py
- [X] T006 [P] Create Message model in backend/src/models/message.py
- [X] T007 Update backend/src/models/__init__.py to export Conversation and Message

### MCP Tools Layer (Required by ALL stories)

- [X] T008 Create backend/src/mcp/__init__.py module file
- [X] T009 Create ToolContext class and ToolError exception in backend/src/mcp/tools.py
- [X] T010 [P] Implement add_task MCP tool in backend/src/mcp/tools.py
- [X] T011 [P] Implement list_tasks MCP tool in backend/src/mcp/tools.py
- [X] T012 [P] Implement complete_task MCP tool in backend/src/mcp/tools.py
- [X] T013 [P] Implement delete_task MCP tool in backend/src/mcp/tools.py
- [X] T014 [P] Implement update_task MCP tool in backend/src/mcp/tools.py

### AI Agent (Required by ALL stories)

- [X] T015 Create backend/src/agents/__init__.py module file
- [X] T016 Create ChatAgent class with system prompt in backend/src/agents/chat_agent.py
- [X] T017 Implement tool registration and OpenAI function calling in backend/src/agents/chat_agent.py
- [X] T018 Add agent response formatting and error handling in backend/src/agents/chat_agent.py

### Chat API Infrastructure (Required by ALL stories)

- [X] T019 Create ChatRequest and ChatResponse schemas in backend/src/schemas/chat.py
- [X] T020 Create ToolCallSchema in backend/src/schemas/chat.py
- [X] T021 Create ChatService class in backend/src/services/chat_service.py
- [X] T022 Implement conversation create/load methods in backend/src/services/chat_service.py
- [X] T023 Implement message persistence methods in backend/src/services/chat_service.py
- [X] T024 Create POST /api/chat endpoint in backend/src/routes/chat.py
- [X] T025 Register chat router in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 & 2 - Task Creation and Listing (Priority: P1) 🎯 MVP

**Goal**: Users can create and list tasks via natural language chat

**Independent Test**: Send "Add a task to buy groceries" and verify task created. Send "Show my tasks" and verify list returned.

### Implementation for User Stories 1 & 2

- [X] T026 [US1] Add intent detection for task creation in backend/src/agents/chat_agent.py
- [X] T027 [US1] Add confirmation response formatting for task creation
- [X] T028 [US2] Add intent detection for task listing in backend/src/agents/chat_agent.py
- [X] T029 [US2] Add formatted task list response generation
- [X] T030 [US1/US2] Create frontend/src/lib/chatApi.ts with sendMessage and getConversations functions
- [X] T031 [P] [US1/US2] Create MessageBubble component in frontend/src/components/chat/MessageBubble.tsx
- [X] T032 [P] [US1/US2] Create MessageInput component in frontend/src/components/chat/MessageInput.tsx
- [X] T033 [US1/US2] Create ChatWindow component in frontend/src/components/chat/ChatWindow.tsx
- [X] T034 [US1/US2] Create chat page in frontend/src/app/chat/page.tsx
- [X] T035 [US1/US2] Wire up chat page to send messages and display responses

**Checkpoint**: MVP complete - users can create and list tasks via chat

---

## Phase 4: User Story 3 - Task Completion (Priority: P2)

**Goal**: Users can mark tasks complete via natural language

**Independent Test**: Send "Complete the groceries task" and verify task marked complete

### Implementation for User Story 3

- [X] T036 [US3] Add intent detection for task completion in backend/src/agents/chat_agent.py
- [X] T037 [US3] Add task matching logic (find task by title/description) in backend/src/agents/chat_agent.py
- [X] T038 [US3] Add completion confirmation response formatting
- [X] T039 [US3] Handle "task not found" error case with helpful message

**Checkpoint**: Users can complete tasks via chat

---

## Phase 5: User Story 4 - Task Deletion (Priority: P2)

**Goal**: Users can delete tasks via natural language with confirmation

**Independent Test**: Send "Delete the old meeting task", confirm deletion, verify task removed

### Implementation for User Story 4

- [X] T040 [US4] Add intent detection for task deletion in backend/src/agents/chat_agent.py
- [X] T041 [US4] Implement confirmation flow - agent asks "Are you sure?" before delete
- [X] T042 [US4] Track pending delete state in conversation context
- [X] T043 [US4] Handle confirmation/cancellation responses
- [X] T044 [US4] Add deletion confirmation response formatting

**Checkpoint**: Users can safely delete tasks with confirmation

---

## Phase 6: User Story 5 - Task Update (Priority: P3)

**Goal**: Users can update task title/description via natural language

**Independent Test**: Send "Rename groceries to weekly shopping" and verify task updated

### Implementation for User Story 5

- [X] T045 [US5] Add intent detection for task update in backend/src/agents/chat_agent.py
- [X] T046 [US5] Parse title and description changes from user message
- [X] T047 [US5] Add update confirmation response formatting
- [X] T048 [US5] Handle partial updates (title only, description only)

**Checkpoint**: Users can update tasks via chat

---

## Phase 7: User Story 6 - Conversation Persistence (Priority: P3)

**Goal**: Users can view and resume previous conversations

**Independent Test**: Start conversation, close app, return and verify conversation history preserved

### Implementation for User Story 6

- [X] T049 [US6] Create GET /api/conversations endpoint in backend/src/routes/chat.py
- [X] T050 [US6] Create GET /api/conversations/{id} endpoint in backend/src/routes/chat.py
- [X] T051 [US6] Create DELETE /api/conversations/{id} endpoint in backend/src/routes/chat.py
- [X] T052 [US6] Create ConversationList component in frontend/src/components/chat/ConversationList.tsx
- [X] T053 [US6] Add conversation selection to chat page
- [X] T054 [US6] Load conversation history when conversation selected
- [X] T055 [US6] Auto-generate conversation title from first message

**Checkpoint**: Users can manage and resume conversations

---

## Phase 8: User Story 7 - Dashboard Analytics (Priority: P4)

**Goal**: Users see task metrics on dashboard

**Independent Test**: View dashboard and verify counts match actual tasks

### Implementation for User Story 7

- [X] T056 [US7] Create GET /api/dashboard/stats endpoint in backend/src/routes/chat.py
- [X] T057 [US7] Implement stats aggregation (total, completed, pending tasks, conversations)
- [X] T058 [US7] Create StatsCard component in frontend/src/components/dashboard/StatsCard.tsx
- [X] T059 [US7] Create dashboard page in frontend/src/app/dashboard/page.tsx
- [X] T060 [US7] Wire up dashboard to fetch and display stats

**Checkpoint**: Dashboard shows accurate task metrics

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T061 [P] Add loading states to chat UI during AI processing
- [X] T062 [P] Add auto-scroll to latest message in ChatWindow
- [X] T063 [P] Add error boundary and error display in chat UI
- [X] T064 Validate user isolation in all conversation/message queries
- [ ] T065 Add rate limiting to /api/chat endpoint
- [ ] T066 Run quickstart.md validation - test all documented commands
- [X] T067 Update navigation to include Chat and Dashboard links

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories 1 & 2 (Phase 3)**: Depends on Foundational - MVP milestone
- **User Stories 3-7 (Phases 4-8)**: Depend on Phase 3 for chat infrastructure
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

| Story | Priority | Dependencies | Can Parallelize With |
|-------|----------|--------------|---------------------|
| US1 + US2 | P1 | Foundational only | - |
| US3 | P2 | US1/US2 (chat infra) | US4, US5 |
| US4 | P2 | US1/US2 (chat infra) | US3, US5 |
| US5 | P3 | US1/US2 (chat infra) | US3, US4 |
| US6 | P3 | US1/US2 (chat infra) | US3, US4, US5 |
| US7 | P4 | US1/US2 (chat infra) | US3-US6 |

### Within Each User Story

- Backend agent changes before frontend UI
- API endpoints before frontend integration
- Core implementation before edge cases

### Parallel Opportunities

```bash
# Phase 1 - All parallel:
T001, T002, T003, T004

# Phase 2 - Models parallel, then tools parallel:
T005, T006  # Models in parallel
T010, T011, T012, T013, T014  # MCP tools in parallel

# Phase 3 - Components parallel:
T031, T032  # MessageBubble and MessageInput in parallel

# Phase 4-8 - User stories can run in parallel after Phase 3
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Stories 1 & 2
4. **STOP and VALIDATE**: Test task creation and listing via chat
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 + US2 → MVP: Create and list tasks via chat
3. US3 + US4 → Complete CRUD: Add complete and delete
4. US5 → Full task management via chat
5. US6 → Conversation history
6. US7 → Dashboard analytics
7. Polish → Production-ready

### Suggested MVP Scope

**Stop after Phase 3** for minimum viable chatbot:
- Users can create tasks: "Add a task to buy groceries"
- Users can list tasks: "Show me my tasks"
- Chat interface functional
- 35 tasks total for MVP

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 4 | Dependencies and verification |
| Phase 2: Foundational | 21 | DB, MCP, Agent, API infrastructure |
| Phase 3: US1 & US2 | 10 | Task creation and listing (MVP) |
| Phase 4: US3 | 4 | Task completion |
| Phase 5: US4 | 5 | Task deletion with confirmation |
| Phase 6: US5 | 4 | Task update |
| Phase 7: US6 | 7 | Conversation persistence |
| Phase 8: US7 | 5 | Dashboard analytics |
| Phase 9: Polish | 7 | Cross-cutting concerns |
| **TOTAL** | **67** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Phase II code remains UNTOUCHED - all new files only
