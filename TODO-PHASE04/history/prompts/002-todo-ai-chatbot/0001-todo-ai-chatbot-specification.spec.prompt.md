---
id: 0001
title: Todo AI Chatbot Specification
stage: spec
date: 2026-01-20
surface: agent
model: claude-opus-4-5
feature: 002-todo-ai-chatbot
branch: 002-todo-ai-chatbot
user: Since Tech
command: /sp.specify
labels: ["specification", "phase-iii", "ai-chatbot", "mcp", "openai-agents", "conversational-ui"]
links:
  spec: specs/002-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-todo-ai-chatbot/spec.md
 - specs/002-todo-ai-chatbot/checklists/requirements.md
 - history/prompts/002-todo-ai-chatbot/0001-todo-ai-chatbot-specification.spec.prompt.md
tests:
 - none
---

## Prompt

```text
# Phase III Todo AI Chatbot – Technical Specification

## System Overview
- Goal: AI-powered conversational Todo chatbot
- Backend: Python FastAPI (reuse Phase II)
- Frontend: OpenAI ChatKit
- AI Logic: OpenAI Agents SDK
- MCP Tools: Official MCP SDK
- Database: Neon PostgreSQL (existing Phase II + new tables: Conversation, Message)
- Auth: Better Auth (reuse Phase II JWT)
- Stateless: All requests independent; conversation state stored in DB
- Frontend UI: Modern SaaS-style dashboard with chat, tasks, and admin analytics

---

## 1) API Specification
### Endpoint: POST /api/{user_id}/chat
**Request:**
- `conversation_id` (integer, optional): Existing conversation ID; if omitted, a new conversation is created.
- `message` (string, required): User's natural language message.

**Response:**
- `conversation_id` (integer): ID of the conversation (existing or newly created)
- `response` (string): AI assistant reply
- `tool_calls` (array): List of MCP tools invoked with parameters and outputs

---

## 2) Database Models
### Task (reuse Phase II)
- `id` (integer, PK)
- `user_id` (string, FK → users)
- `title` (string)
- `description` (string, optional)
- `completed` (boolean)
- `created_at` (datetime)
- `updated_at` (datetime)

### Conversation (new)
- `id` (integer, PK)
- `user_id` (string, FK → users)
- `created_at` (datetime)
- `updated_at` (datetime)

### Message (new)
- `id` (integer, PK)
- `user_id` (string, FK → users)
- `conversation_id` (integer, FK → Conversation)
- `role` (string) → `'user'` or `'assistant'`
- `content` (string)
- `created_at` (datetime)

---

## 3) MCP Tools Specification
- `add_task(user_id, title, description?)` → Returns `task_id`, `status`, `title`
- `list_tasks(user_id, status?)` → Returns array of task objects
- `complete_task(user_id, task_id)` → Returns `task_id`, `status`, `title`
- `delete_task(user_id, task_id)` → Returns `task_id`, `status`, `title`
- `update_task(user_id, task_id, title?, description?)` → Returns `task_id`, `status`, `title`

---

## 4) Agent Behavior Rules
- Detect user intent from natural language message
- Call correct MCP tool based on intent
- Confirm every action with friendly message
- Handle errors gracefully (e.g., task not found, invalid input)
- Never modify DB directly; all operations via MCP tools

---

## 5) Stateless Request Flow
1. Receive user message from frontend
2. Fetch conversation history from DB
3. Store user message in `Message` table
4. Run AI agent via OpenAI Agents SDK
5. Agent invokes appropriate MCP tools
6. Store assistant response in `Message` table
7. Return `response` + `tool_calls` to frontend
8. Server holds no in-memory state

---

## 6) Frontend Integration & UI

### **Main UI Components**
| Component | Description |
|-----------|-------------|
| `Sidebar` | Navigation menu: Dashboard, Tasks, Conversations, Profile, Logout; collapsible |
| `Header` | Top bar: Logo/branding, user avatar, optional search |
| `ChatWindow` | Scrollable chat interface; user messages right, AI messages left |
| `MessageInput` | Text input with Send button and optional quick action buttons (Add Task, List Tasks, Complete Task) |
| `TaskList` | Shows all tasks of the user; filter by status |
| `ConversationList` | List of user conversations; shows last message + timestamp |
| `AdminStatsCard` | Dashboard card showing metrics (total tasks, completed tasks, active conversations) |
| `Footer` | Minimal footer with branding, version info |

### **UX Flow**
1. User opens chat → previous conversation loaded
2. User sends message → `POST /api/{user_id}/chat`
3. AI responds → message displayed in chat window
4. Quick action buttons trigger MCP tools
5. Task updates reflected immediately in TaskList
6. Admin dashboard shows analytics, conversation overview

### **Design Guidelines**
- Modern SaaS style: rounded corners, shadows, clean typography, accent colors
- Responsive: Sidebar collapsible on mobile, chat window scrollable
- Smooth transitions: Message fade-in, scroll animation
- Conversation search/filter
- Notifications for task updates
```

## Response snapshot

Feature specification successfully created at `specs/002-todo-ai-chatbot/spec.md` on branch `002-todo-ai-chatbot`.

**Feature Details**:
- Branch: `002-todo-ai-chatbot`
- Spec File: `specs/002-todo-ai-chatbot/spec.md`
- Status: Draft, ready for planning

**User Stories Defined (7 total)**:
1. **P1**: Conversational Task Creation - Create tasks via natural language
2. **P1**: Conversational Task Listing - Query and view tasks through chat
3. **P2**: Conversational Task Completion - Mark tasks done via conversation
4. **P2**: Conversational Task Deletion - Remove tasks with confirmation
5. **P3**: Conversational Task Update - Modify task titles/descriptions
6. **P3**: Conversation Persistence - Resume previous conversations
7. **P4**: Dashboard Analytics - View task metrics and activity

**Functional Requirements (17 total)**:
- FR-001 to FR-017 covering chat endpoint, message persistence, MCP tool usage, user isolation, AI agent behavior, frontend components, and authentication

**Key Entities**:
- Conversation: Chat session between user and AI
- Message: Individual messages with role (user/assistant)
- Task: Reused from Phase II
- User: Reused from Phase II (Better Auth)

**Success Criteria (10 measurable outcomes)**:
- Task creation under 10 seconds
- 100% accurate task listing
- 95% intent recognition for clear requests
- Conversation load under 2 seconds
- Zero cross-user data access
- User-friendly error handling

**Quality Checklist**: All 16 items passed
- No implementation details in spec
- All requirements testable and unambiguous
- Success criteria technology-agnostic
- Edge cases identified
- Scope clearly bounded

## Outcome

- ✅ Impact: Phase III feature specification created with comprehensive user stories, functional requirements, and measurable success criteria
- 🧪 Tests: Acceptance scenarios defined for all 7 user stories
- 📁 Files: Created `specs/002-todo-ai-chatbot/spec.md`, `specs/002-todo-ai-chatbot/checklists/requirements.md`
- 🔁 Next prompts: `/sp.plan` to create implementation plan, or `/sp.clarify` if additional requirements clarification needed
- 🧠 Reflection: Specification is comprehensive and ready for planning. No clarification markers needed - user input was detailed enough to make informed decisions. User stories prioritized for incremental MVP delivery.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification generated without ambiguity
- Graders run and results (PASS/FAIL): Quality checklist 16/16 PASS
- Prompt variant (if applicable): Detailed technical specification with API, database, MCP, and UI requirements
- Next experiment (smallest change to try): Proceed to `/sp.plan` to design implementation architecture based on this specification
