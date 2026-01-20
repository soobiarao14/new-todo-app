---
id: 0002
title: Todo AI Chatbot Implementation Plan
stage: plan
date: 2026-01-20
surface: agent
model: claude-opus-4-5
feature: 002-todo-ai-chatbot
branch: 002-todo-ai-chatbot
user: Since Tech
command: /sp.plan
labels: ["planning", "phase-iii", "ai-chatbot", "mcp", "openai-agents", "architecture"]
links:
  spec: specs/002-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-todo-ai-chatbot/plan.md
 - specs/002-todo-ai-chatbot/research.md
 - specs/002-todo-ai-chatbot/data-model.md
 - specs/002-todo-ai-chatbot/quickstart.md
 - specs/002-todo-ai-chatbot/contracts/chat-api.yaml
 - specs/002-todo-ai-chatbot/contracts/mcp-tools.md
 - history/prompts/002-todo-ai-chatbot/0002-todo-ai-chatbot-implementation-plan.plan.prompt.md
tests:
 - none
---

## Prompt

```text
Phase III Todo AI Chatbot Implementation Plan

## Goal
Add an **AI-powered conversational chatbot** to the existing Phase II Todo application **without modifying or breaking Phase II**.

The chatbot will:
- Understand natural language
- Manage user tasks (add, list, complete, delete, update)
- Be fully stateless
- Use secure JWT-based authentication

---

## Phase Structure Overview

Phase III is divided into **6 safe and isolated steps**:

1. Database Extension (Safe)
2. MCP Server Setup
3. AI Agent Design
4. Chat API Layer
5. Frontend Chat Integration
6. Testing & Hardening

---

## STEP 1: Database Extension (No Phase II Changes)

### Objective
Store conversation history without affecting existing task logic.

### Actions
- Add **new tables only**:
  - `conversations`
  - `messages`

### Rules
- ❌ Do NOT modify Task table
- ❌ Do NOT change existing APIs
- ✅ Use migrations (SQLModel / Alembic)

### Output
- Persistent chat history
- Stateless chatbot architecture

---

## STEP 2: MCP Server (Task Operations Layer)

### Objective
Allow AI to manage tasks **safely and securely**.

### MCP Tools to Implement
| Tool Name | Purpose |
|--------|--------|
| add_task | Create a task |
| list_tasks | Fetch tasks |
| complete_task | Mark task complete |
| delete_task | Delete task |
| update_task | Update task details |

### Rules
- MCP tools must reuse Phase II service logic
- ❌ Agent must NEVER access DB directly
- ✅ Validate `user_id` in every tool

### Output
- Secure tool layer for AI actions

---

## STEP 3: AI Agent Design (Chatbot Brain)

### Objective
Convert natural language into correct task actions.

### Agent Responsibilities
- Detect user intent (add, list, complete, delete, update)
- Call the correct MCP tool
- Confirm every action in plain English
- Handle errors gracefully

### Agent Rules
- ❌ No guessing
- ❌ No silent actions
- ✅ Ask for clarification when input is ambiguous
- ✅ Always return user-friendly responses

### Output
- Predictable and reliable AI behavior

---

## STEP 4: Chat API Layer (Backend Bridge)

### Endpoint
`POST /api/chat`

### Request Flow
1. Authenticate user via JWT
2. Load or create conversation
3. Save user message
4. Run AI agent
5. Execute MCP tools
6. Save assistant response
7. Return response + tool calls

### Rules
- ❌ No in-memory sessions
- ❌ Never trust `user_id` from URL
- ✅ Fully stateless
- ✅ Reuse Phase II authentication

### Output
- Production-ready chat endpoint

---

## STEP 5: Frontend Chat Integration

### Objective
Create a modern SaaS-style chatbot UI.

### UI Layout
- Sidebar Navigation
  - Dashboard
  - Tasks
  - AI Chat
- Chat Screen
  - Conversation list (left panel)
  - Chat window (right panel)
  - Input box + Send button
- Optional Admin Panel
  - Conversation monitoring
  - Usage analytics

### UX Rules
- Auto-scroll to latest message
- Loading / typing indicators
- Clear action confirmations
- Responsive design

### Output
- Clean and intuitive chat experience
- Zero impact on existing UI

---

## STEP 6: Testing & Hardening
```

## Response snapshot

Implementation plan successfully created at `specs/002-todo-ai-chatbot/plan.md` with all supporting artifacts.

**Artifacts Generated (6 total)**:

1. **research.md** - Technology decisions resolved:
   - OpenAI Agents SDK for AI logic (authorized in Phase III)
   - MCP SDK for tool abstraction
   - Additive database changes only
   - Stateless chat architecture

2. **data-model.md** - Database schema additions:
   - `conversations` table (id, user_id, title, timestamps)
   - `messages` table (id, user_id, conversation_id, role, content, tool_calls, timestamp)
   - User isolation enforced via user_id foreign keys
   - No modifications to Phase II tables

3. **contracts/chat-api.yaml** - OpenAPI specification:
   - `POST /api/chat` - Main chat endpoint
   - `GET /api/conversations` - List conversations
   - `GET /api/conversations/{id}` - Get conversation with messages
   - `DELETE /api/conversations/{id}` - Delete conversation
   - `GET /api/dashboard/stats` - Dashboard metrics

4. **contracts/mcp-tools.md** - MCP tool definitions:
   - `add_task(title, description?)` - Create task
   - `list_tasks(status?)` - List/filter tasks
   - `complete_task(task_id)` - Mark complete
   - `delete_task(task_id)` - Delete (requires confirmation)
   - `update_task(task_id, title?, description?)` - Update

5. **quickstart.md** - Getting started guide:
   - Environment setup
   - Running the application
   - Example chat commands
   - API endpoint examples

6. **plan.md** - Implementation plan:
   - 6-phase implementation approach
   - Constitution compliance verification (all rules pass)
   - Project structure with new files mapped
   - Risk assessment and dependencies

**Constitution Compliance**:
- All Phase III rules verified: ✅
- MCP tools only (Rule 6): ✅
- Stateless chat (Rule 7): ✅
- User isolation (Rule 4): ✅
- JWT authentication (Rules 2, 3): ✅

## Outcome

- ✅ Impact: Complete implementation plan with architecture, contracts, and data model ready for task generation
- 🧪 Tests: Test strategy defined in Phase 6 (optional, if requested)
- 📁 Files: Created 6 artifacts in `specs/002-todo-ai-chatbot/`
- 🔁 Next prompts: `/sp.tasks` to generate implementation task list
- 🧠 Reflection: Plan preserves Phase II integrity with additive-only changes. All new code in new files. MCP abstraction ensures AI never touches database directly. Stateless design enables horizontal scaling.

## Evaluation notes (flywheel)

- Failure modes observed: None - all technical decisions resolved in research phase
- Graders run and results (PASS/FAIL): Constitution check 7/7 rules PASS
- Prompt variant (if applicable): Detailed implementation plan with 6-step breakdown in user input
- Next experiment (smallest change to try): Generate tasks via `/sp.tasks` and validate Phase 1 (database extension) can be implemented without touching Phase II code
