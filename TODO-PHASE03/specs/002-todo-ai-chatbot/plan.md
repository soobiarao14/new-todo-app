# Implementation Plan: Todo AI Chatbot

**Branch**: `002-todo-ai-chatbot` | **Date**: 2026-01-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-ai-chatbot/spec.md`

## Summary

Add an AI-powered conversational chatbot to the Phase II Todo application that enables natural language task management. The chatbot uses OpenAI Agents SDK for intent detection and MCP tools for secure task operations, maintaining stateless architecture with conversation persistence in PostgreSQL.

**Key Deliverables**:
1. Database extension (Conversation, Message tables)
2. MCP server with 5 task operation tools
3. AI agent with intent detection and tool calling
4. Chat API endpoint (`POST /api/chat`)
5. Frontend chat interface with conversation management
6. Dashboard with task analytics

---

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, OpenAI SDK, MCP SDK (backend); Next.js 14+, React 18+ (frontend)
**Storage**: Neon PostgreSQL (reuse Phase II + new tables)
**Testing**: pytest (backend), Jest/React Testing Library (frontend) - if tests requested
**Target Platform**: Linux server (backend), Web browsers (frontend)
**Project Type**: Web application (monorepo with frontend/ and backend/)
**Performance Goals**: <5s chat response, <500ms conversation load
**Constraints**: Stateless requests, JWT authentication, user isolation
**Scale/Scope**: Single-user sessions, ~100 messages per conversation max

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Gates

| Gate | Status | Evidence |
|------|--------|----------|
| Phase III technologies only | ✅ PASS | OpenAI Agents SDK, MCP SDK - both authorized |
| No Phase IV technologies | ✅ PASS | No Kubernetes, event streaming, microservices |
| Phase II unchanged | ✅ PASS | Only additive changes, no modifications to existing code |
| Spec-driven development | ✅ PASS | spec.md completed before planning |
| Architecture first | ✅ PASS | Data model, contracts defined before implementation |

### Rule Compliance

| Rule | Status | Implementation |
|------|--------|----------------|
| Rule 1: No manual code edits | ✅ | All code generated from specs |
| Rule 2: JWT auth required | ✅ | Reuse existing middleware |
| Rule 3: JWT verification | ✅ | Reuse existing `get_current_user_id` |
| Rule 4: User isolation | ✅ | All queries filter by `user_id` from JWT |
| Rule 5: Monorepo structure | ✅ | New files in `backend/src/agents/`, `backend/src/mcp/`, `frontend/src/app/chat/` |
| Rule 6: MCP tools only | ✅ | Agent uses MCP tools, never direct DB |
| Rule 7: Stateless chat | ✅ | No in-memory state, all in PostgreSQL |

### Post-Design Re-Check

| Item | Status | Notes |
|------|--------|-------|
| Data model aligns with constitution | ✅ PASS | Conversation/Message tables per Section 5.6 |
| API contracts follow Phase II patterns | ✅ PASS | Same error format, JWT auth |
| MCP tools enforce user isolation | ✅ PASS | user_id from JWT context |
| No complexity violations | ✅ PASS | Minimal design, reuses Phase II services |

---

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-ai-chatbot/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Database schema
├── quickstart.md        # Getting started guide
├── contracts/
│   ├── chat-api.yaml    # OpenAPI specification
│   └── mcp-tools.md     # MCP tool definitions
└── checklists/
    └── requirements.md  # Specification checklist
```

### Source Code (Phase III Additions)

```text
backend/src/
├── agents/              # NEW: AI agent module
│   ├── __init__.py
│   └── chat_agent.py    # OpenAI agent with tool calling
├── mcp/                 # NEW: MCP tools module
│   ├── __init__.py
│   └── tools.py         # Task operation tools
├── models/
│   ├── __init__.py      # MODIFY: Import new models
│   ├── conversation.py  # NEW: Conversation entity
│   └── message.py       # NEW: Message entity
├── routes/
│   ├── __init__.py
│   └── chat.py          # NEW: Chat endpoints
├── services/
│   ├── __init__.py
│   ├── todo_service.py  # UNCHANGED (Phase II)
│   └── chat_service.py  # NEW: Chat business logic
└── schemas/
    ├── __init__.py
    └── chat.py          # NEW: Request/response schemas

frontend/src/
├── app/
│   ├── chat/
│   │   └── page.tsx     # NEW: Chat page
│   └── dashboard/
│       └── page.tsx     # NEW: Dashboard page
├── components/
│   ├── chat/            # NEW: Chat components
│   │   ├── ChatWindow.tsx
│   │   ├── MessageInput.tsx
│   │   ├── MessageBubble.tsx
│   │   └── ConversationList.tsx
│   └── dashboard/       # NEW: Dashboard components
│       └── StatsCard.tsx
└── lib/
    ├── api.ts           # UNCHANGED (Phase II)
    └── chatApi.ts       # NEW: Chat API client
```

**Structure Decision**: Web application with separate frontend/ and backend/ directories. All Phase III additions are new files; no modifications to Phase II code except importing new models.

---

## Implementation Phases

### Phase 1: Database Extension (Safe)

**Objective**: Add conversation storage without touching Phase II.

**Tasks**:
1. Create `backend/src/models/conversation.py` with Conversation model
2. Create `backend/src/models/message.py` with Message model
3. Update `backend/src/models/__init__.py` to export new models
4. Verify tables auto-create on startup (SQLModel)

**Validation**:
- Tables created: `conversations`, `messages`
- Foreign keys valid: `user_id`, `conversation_id`
- Phase II `todos` table unchanged

---

### Phase 2: MCP Server Setup

**Objective**: Create secure task operation layer for AI.

**Tasks**:
1. Create `backend/src/mcp/__init__.py`
2. Create `backend/src/mcp/tools.py` with 5 tools:
   - `add_task`
   - `list_tasks`
   - `complete_task`
   - `delete_task`
   - `update_task`
3. Implement `ToolContext` for user_id injection
4. Add error handling with `ToolError`

**Validation**:
- Tools reuse `TodoService` methods
- user_id always from JWT context
- Error responses are structured

---

### Phase 3: AI Agent Design

**Objective**: Implement intelligent task management assistant.

**Tasks**:
1. Create `backend/src/agents/__init__.py`
2. Create `backend/src/agents/chat_agent.py` with:
   - System prompt with tool definitions
   - Intent detection via function calling
   - Tool execution with context
   - Response formatting
3. Add OpenAI API configuration
4. Implement confirmation flow for delete

**Validation**:
- Agent correctly maps intent to tools
- Destructive actions request confirmation
- Ambiguous requests trigger clarification
- Errors produce user-friendly messages

---

### Phase 4: Chat API Layer

**Objective**: Create stateless chat endpoint.

**Tasks**:
1. Create `backend/src/schemas/chat.py` with:
   - `ChatRequest`
   - `ChatResponse`
   - `ToolCallSchema`
2. Create `backend/src/services/chat_service.py` with:
   - Conversation creation/loading
   - Message persistence
   - Agent invocation
3. Create `backend/src/routes/chat.py` with:
   - `POST /api/chat`
   - `GET /api/conversations`
   - `GET /api/conversations/{id}`
   - `DELETE /api/conversations/{id}`
   - `GET /api/dashboard/stats`
4. Register routes in `main.py`
5. Update auth middleware PUBLIC_PATHS if needed

**Validation**:
- Endpoint requires JWT authentication
- New conversation created if no conversation_id
- Messages persisted before and after AI processing
- Response includes tool_calls array
- User isolation enforced

---

### Phase 5: Frontend Chat Integration

**Objective**: Build modern chat UI.

**Tasks**:
1. Create `frontend/src/lib/chatApi.ts` with API client
2. Create chat components:
   - `ChatWindow.tsx` - Message display area
   - `MessageInput.tsx` - Input with send button
   - `MessageBubble.tsx` - Single message styling
   - `ConversationList.tsx` - Sidebar conversation list
3. Create `frontend/src/app/chat/page.tsx` - Main chat page
4. Create dashboard components:
   - `StatsCard.tsx` - Metrics display
5. Create `frontend/src/app/dashboard/page.tsx` - Dashboard page
6. Update navigation (if applicable)

**Validation**:
- Chat messages display correctly (user right, assistant left)
- Conversation list shows all user conversations
- Input sends message and displays response
- Auto-scroll to latest message
- Loading states during AI processing

---

### Phase 6: Testing & Hardening

**Objective**: Ensure reliability and security.

**Tasks** (if tests requested):
1. Add agent behavior tests
2. Add user isolation tests
3. Add error handling tests
4. Performance testing for conversation load

**Security Validation**:
- [ ] JWT required for all chat endpoints
- [ ] User isolation verified (User A can't access User B's conversations)
- [ ] Prompt injection mitigated (system/user separation)
- [ ] Tool calls logged for audit

---

## Complexity Tracking

> No violations to justify - design follows constitutional guidelines.

| Aspect | Complexity Level | Justification |
|--------|-----------------|---------------|
| Database | Low | 2 new tables, standard foreign keys |
| MCP Tools | Low | 5 tools wrapping existing service |
| AI Agent | Medium | OpenAI function calling (standard pattern) |
| Chat API | Low | Single endpoint, stateless design |
| Frontend | Medium | New pages and components (no modifications) |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| OpenAI API latency | Medium | Low | Show loading indicator, set expectations |
| OpenAI API errors | Low | Medium | Graceful error handling, retry logic |
| Prompt injection | Low | High | Strict system/user message separation |
| User data leakage | Low | Critical | User isolation at query level |

---

## Dependencies

### External Dependencies (New for Phase III)

| Package | Version | Purpose |
|---------|---------|---------|
| openai | >=1.0.0 | OpenAI Agents SDK |
| mcp | >=0.1.0 | Model Context Protocol SDK |

### Internal Dependencies (Reused from Phase II)

| Component | Location | Purpose |
|-----------|----------|---------|
| TodoService | `backend/src/services/todo_service.py` | Task CRUD operations |
| AuthMiddleware | `backend/src/middleware/auth.py` | JWT verification |
| get_current_user_id | `backend/src/dependencies.py` | User ID extraction |
| AuthContext | `frontend/src/contexts/AuthContext.tsx` | Frontend auth state |
| api.ts | `frontend/src/lib/api.ts` | API client patterns |

---

## Artifacts Generated

| Artifact | Path | Purpose |
|----------|------|---------|
| Research | `specs/002-todo-ai-chatbot/research.md` | Technology decisions |
| Data Model | `specs/002-todo-ai-chatbot/data-model.md` | Database schema |
| Chat API Contract | `specs/002-todo-ai-chatbot/contracts/chat-api.yaml` | OpenAPI specification |
| MCP Tools Contract | `specs/002-todo-ai-chatbot/contracts/mcp-tools.md` | Tool definitions |
| Quickstart | `specs/002-todo-ai-chatbot/quickstart.md` | Getting started guide |
| Plan | `specs/002-todo-ai-chatbot/plan.md` | This document |

---

## Next Steps

1. Run `/sp.tasks` to generate implementation task list
2. Implement Phase 1 (Database Extension) first
3. Proceed sequentially through phases
4. Run tests after each phase (if tests requested)

---

## Approval

- [ ] Technical approach reviewed
- [ ] Constitution compliance verified
- [ ] User approved for implementation

**Ready for**: `/sp.tasks`
