# Research: Todo AI Chatbot

**Feature**: 002-todo-ai-chatbot
**Date**: 2026-01-20
**Status**: Complete

## Overview

This document captures research decisions for implementing the Phase III AI Chatbot, ensuring all technical choices are validated and unknowns resolved.

---

## 1. OpenAI Agents SDK Integration

### Decision
Use **OpenAI Agents SDK** (Python) for AI agent logic with function calling capabilities.

### Rationale
- Official SDK with first-class support for tool/function calling
- Native async support compatible with FastAPI
- Structured output parsing for reliable intent detection
- Active maintenance and documentation
- Constitutional mandate: Phase III authorizes OpenAI Agents SDK

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| LangChain | Over-engineered for simple tool-calling use case |
| Raw OpenAI API | Requires manual tool orchestration |
| Anthropic Claude | Not authorized in Phase III constitution |

### Implementation Notes
- Use `openai` Python package (latest version)
- Configure via `OPENAI_API_KEY` environment variable
- Model: `gpt-4o` for best tool-calling performance
- Temperature: 0.3 for consistent, predictable responses

---

## 2. MCP (Model Context Protocol) SDK Integration

### Decision
Use **Official MCP SDK** for Python to expose task operations as tools.

### Rationale
- Standard protocol for AI-tool communication
- Type-safe tool definitions with Pydantic
- Clean separation between AI logic and business operations
- Constitutional mandate: Phase III authorizes MCP SDK

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Custom tool protocol | Non-standard, maintenance burden |
| Direct function calls | No abstraction, harder to audit |

### Implementation Notes
- MCP tools wrap existing `TodoService` methods
- Each tool receives `user_id` from JWT context (not from AI)
- Tools return structured responses for AI to interpret
- All tool calls logged for audit trail

---

## 3. Database Schema Extension Strategy

### Decision
Add new tables (`conversations`, `messages`) without modifying existing Phase II schema.

### Rationale
- Phase II isolation preserved (constitutional requirement)
- Additive changes minimize risk
- Foreign keys maintain referential integrity
- Existing `users` and `todos` tables untouched

### Schema Design
```
conversations
├── id (UUID, PK)
├── user_id (UUID, FK → users.id)
├── title (VARCHAR, optional, for conversation naming)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

messages
├── id (UUID, PK)
├── user_id (UUID, FK → users.id)
├── conversation_id (UUID, FK → conversations.id)
├── role (VARCHAR: 'user' | 'assistant')
├── content (TEXT)
├── tool_calls (JSONB, nullable, stores tool invocations)
└── created_at (TIMESTAMP)
```

### Implementation Notes
- Use SQLModel for consistency with Phase II
- Add indexes on `user_id` and `conversation_id`
- No Alembic migrations needed (SQLModel handles table creation)

---

## 4. Chat API Endpoint Design

### Decision
Single endpoint `POST /api/chat` with stateless request/response pattern.

### Rationale
- Simple, RESTful design
- Stateless per constitutional Rule 7
- Consistent with Phase II API patterns
- JWT authentication reused from middleware

### Request/Response Design
```json
// Request
{
  "conversation_id": "uuid-optional",
  "message": "string-required"
}

// Response
{
  "conversation_id": "uuid",
  "response": "string",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {"title": "..."},
      "result": {"task_id": "...", "status": "created"}
    }
  ]
}
```

### Implementation Notes
- user_id extracted from JWT (never from request body)
- New conversation created if conversation_id omitted
- Messages persisted before and after AI processing
- Error responses follow Phase II error format

---

## 5. Agent Behavior Design

### Decision
Implement structured agent with explicit tool mapping and confirmation flows.

### Rationale
- Predictable behavior (constitutional requirement)
- Clear user feedback on all actions
- Graceful error handling
- No silent modifications

### Intent Categories
| Intent | MCP Tool | Confirmation Required |
|--------|----------|----------------------|
| Create task | `add_task` | No (non-destructive) |
| List tasks | `list_tasks` | No (read-only) |
| Complete task | `complete_task` | No (reversible) |
| Update task | `update_task` | No (non-destructive) |
| Delete task | `delete_task` | **Yes** (destructive) |

### Agent Prompt Strategy
- System prompt defines available tools and rules
- User messages passed as-is (no prompt injection risk via separation)
- Ambiguous requests trigger clarification response
- All responses confirm action taken or explain why not

---

## 6. Frontend Integration Strategy

### Decision
Add new chat page (`/chat`) with conversation UI, preserving existing Phase II pages.

### Rationale
- Zero impact on existing Phase II UI
- New route for new functionality
- Reuse existing auth context and API client patterns

### Component Structure
```
frontend/src/
├── app/
│   ├── chat/
│   │   └── page.tsx         # Main chat page (NEW)
│   └── dashboard/
│       └── page.tsx         # Dashboard with stats (NEW)
├── components/
│   ├── chat/
│   │   ├── ChatWindow.tsx   # Message display (NEW)
│   │   ├── MessageInput.tsx # Input with send (NEW)
│   │   ├── MessageBubble.tsx # Single message (NEW)
│   │   └── ConversationList.tsx # Sidebar list (NEW)
│   └── dashboard/
│       └── StatsCard.tsx    # Metrics card (NEW)
└── lib/
    └── chatApi.ts           # Chat API client (NEW)
```

### Implementation Notes
- All new files, no modifications to existing components
- Reuse `AuthContext` for JWT handling
- Reuse Tailwind CSS classes for consistent styling

---

## 7. Security Considerations

### Decision
Apply defense-in-depth security model consistent with Phase II.

### Implementation Checklist
- [x] JWT verification via existing middleware (reuse)
- [x] User isolation enforced in MCP tools (via user_id from JWT)
- [x] Prompt injection prevention (system/user message separation)
- [x] Rate limiting on chat endpoint (new, per-user)
- [x] Tool calls logged for audit trail
- [x] No sensitive data in AI prompts

### Prompt Injection Mitigation
```python
# GOOD: Clear separation
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},  # Fixed, trusted
    {"role": "user", "content": user_message}       # Untrusted input
]

# BAD: Never do this
prompt = f"Help the user: {user_message}"  # Injection risk
```

---

## 8. Performance Considerations

### Decision
Optimize for acceptable latency with async processing.

### Targets
- Chat response: <5 seconds (includes AI API call)
- Conversation history load: <500ms for 100 messages
- Database queries: <50ms each

### Implementation Notes
- Async database operations (SQLModel with asyncio)
- Pagination for long conversation histories
- Connection pooling already in Phase II
- Consider streaming responses for long AI replies (future enhancement)

---

## Summary

All technical decisions have been made with constitutional compliance as primary constraint. Key outcomes:

1. **OpenAI Agents SDK** for AI logic
2. **MCP SDK** for tool abstraction
3. **Additive database changes** only
4. **Stateless chat endpoint** at `/api/chat`
5. **New frontend pages** without modifying Phase II UI
6. **Defense-in-depth security** with JWT and user isolation

No NEEDS CLARIFICATION items remain. Ready for Phase 1 design.
