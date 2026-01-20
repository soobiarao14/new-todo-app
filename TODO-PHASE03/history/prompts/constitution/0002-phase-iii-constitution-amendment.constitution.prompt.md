---
id: 0002
title: Phase III Constitution Amendment
stage: constitution
date: 2026-01-20
surface: agent
model: claude-opus-4-5
feature: none
branch: main
user: Since Tech
command: /sp.constitution
labels: ["constitution", "governance", "phase-iii", "ai-chatbot", "mcp", "openai-agents"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - history/prompts/constitution/0002-phase-iii-constitution-amendment.constitution.prompt.md
tests:
 - none
---

## Prompt

```text
Amend the global Project Constitution for the "Evolution of Todo" hackathon project to include Phase III: Todo AI Chatbot.

Preserve Phase II rules fully (backend, database, authentication, user isolation, REST endpoints).

Add Phase III rules specifically for AI chatbot, MCP, and stateless conversational flow.

====================
PROJECT CONSTITUTION – AMENDMENT FOR PHASE III
====================

Phase III (Todo AI Chatbot):
----------------------------
1. Goal:
- Build an AI-powered conversational Todo chatbot.
- Use OpenAI Agents SDK for AI logic.
- Use Official MCP SDK for all task operations.
- Stateless chat endpoint.
- Persist conversation + messages in Neon PostgreSQL.
- Integrate with existing Phase II backend and Better Auth.

2. Architecture Additions:
- Frontend: OpenAI ChatKit
- Backend: FastAPI (reuse Phase II endpoints)
- AI: OpenAI Agents SDK
- Tools: MCP Server exposing add/list/update/delete/complete task
- DB: Reuse Phase II Neon PostgreSQL with new tables:
    - Conversation
    - Message
- Stateless flow: Every chat request independent; no in-memory state.

3. Agent & MCP Rules:
- Agent interprets user natural language to call correct MCP tools.
- Always confirm actions.
- Handle errors gracefully.
- Agent must **never modify DB directly**; only via MCP tools.

4. API:
- POST /api/{user_id}/chat
  Request: conversation_id (optional), message (required)
  Response: conversation_id, response, tool_calls

5. Database Models (Phase III additions):
- Conversation: id, user_id, created_at, updated_at
- Message: id, user_id, conversation_id, role (user/assistant), content, created_at

6. Strict Phase III Rules:
- Phase II backend rules remain unchanged.
- No manual code edits.
- User isolation enforced via JWT.
- AI actions use MCP tools only.
- Stateless architecture enforced.
- Chat conversation persisted for resuming sessions.

7. Quality & Compliance:
- Follow spec-driven development.
- Type safety: SQLModel (backend), TypeScript strict mode (frontend)
- Code formatting and testing standard
```

## Response snapshot

Constitution successfully amended at `.specify/memory/constitution.md` from version 2.0.0 to 3.0.0 (MAJOR version bump).

**Version Change**: 2.0.0 → 3.0.0 (MAJOR)
**Rationale**: Introduction of Phase III with AI chatbot, MCP integration, OpenAI Agents SDK, and new database models (Conversation, Message) constitutes a major architectural expansion.

**Key Additions for Phase III**:

1. **Vision Updated**: Added Phase III objective for AI-powered conversational chatbot with natural language task management

2. **Technology Commitments (Phase Matrix)**:
   - Phase II status changed to "Completed, maintained for integration"
   - Phase III (CURRENT PHASE) added with authorized technologies:
     - AI Framework: OpenAI Agents SDK
     - Tool Protocol: Official MCP SDK
     - Chat UI: OpenAI ChatKit
     - Backend additions: `agents/` and `mcp/` modules
     - Database additions: `conversation` and `message` tables
   - Phase IV+ defined as future (cloud orchestration, Kubernetes, microservices)

3. **New Strict Rules**:
   - Rule 6: MCP Tools Only for Task Operations - AI agent MUST NEVER modify database directly
   - Rule 7: Stateless Chat Architecture - Every chat request independently processable

4. **Architecture Guidelines Added**:
   - AI Chatbot Architecture: 11-step chat flow with agent rules and conversation persistence
   - MCP Server Architecture: Tool definitions (`add_task`, `list_tasks`, `update_task`, `delete_task`, `complete_task`), security, error handling
   - Conversation Database Architecture: Schema additions for `Conversation` and `Message` tables with user isolation

5. **Security Requirements Enhanced**:
   - AI Security section added with:
     - Prompt injection prevention
     - Tool execution safety (MCP validation, confirmation for destructive actions)
     - Data leakage prevention (user-scoped data access)
   - OpenAI API keys added to secrets management
   - Chat endpoint rate limiting added

6. **Quality Standards Extended**:
   - Agent behavior tests added to test organization (`tests/agent/`)
   - Correct tool selection testing added to coverage requirements

**All Phase II Rules Preserved**:
- JWT authentication, user isolation, monorepo structure, no manual code edits - all maintained unchanged
- REST endpoints `/api/tasks/*` unchanged
- Better Auth integration unchanged
- Database architecture maintained with additive schema changes only

## Outcome

- ✅ Impact: Project constitution amended to authorize Phase III AI chatbot development with MCP integration while preserving all Phase II security and architecture rules
- 🧪 Tests: No tests required (governance document)
- 📁 Files: Updated `.specify/memory/constitution.md` (638 lines), created PHR in `history/prompts/constitution/`
- 🔁 Next prompts: `/sp.specify todo-ai-chatbot` to create Phase III feature specification for the conversational chatbot
- 🧠 Reflection: Amendment maintains backward compatibility with Phase II while introducing AI-specific rules (MCP-only tool execution, stateless chat, prompt injection prevention). The phase isolation principle updated to forbid Phase IV technologies in Phase III.

## Evaluation notes (flywheel)

- Failure modes observed: None - amendment successfully applied with all Phase II rules preserved and Phase III rules added
- Graders run and results (PASS/FAIL): N/A (governance document, no automated grading applicable)
- Prompt variant (if applicable): Constitutional amendment prompt with detailed Phase III requirements (AI chatbot, MCP, stateless architecture)
- Next experiment (smallest change to try): Create Phase III feature specification (`/sp.specify todo-ai-chatbot`) to validate constitutional Phase III rules are practically enforceable for AI agent development
