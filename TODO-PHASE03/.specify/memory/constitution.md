<!--
SYNC IMPACT REPORT:
==================
Version Change: 2.0.0 → 3.0.0 (MAJOR)
Date: 2026-01-20
Rationale: Introduction of Phase III with AI chatbot, MCP integration, OpenAI Agents SDK,
           and new database models (Conversation, Message). This constitutes a major
           architectural expansion requiring constitutional amendment.

Modified Principles:
- Phase Isolation and Technology Discipline: Updated to reflect Phase III authorization
- Technology Commitments: Phase III now active, Phase IV added as future

Added Sections:
- Section 4.3: Phase III Technology Stack (AI Chatbot)
- Section 5.4: AI Chatbot Architecture
- Section 5.5: MCP Server Architecture
- Section 5.6: Conversation Database Architecture
- Section 7.3: AI Security Requirements
- Strict Rules: Rule 6 (MCP Tools Only), Rule 7 (Stateless Architecture)

Removed Sections:
- None (Phase II rules preserved in full)

Templates Requiring Updates:
✅ plan-template.md - Constitution Check section compatible
✅ spec-template.md - Requirements section compatible
✅ tasks-template.md - Task organization compatible
✅ CLAUDE.md - References constitution correctly

Follow-up TODOs:
- None - all placeholders resolved
-->

# Evolution of Todo – Project Constitution (Phase III: Todo AI Chatbot)

## 1. Vision

**Phase III Objective**: Extend the Evolution of Todo with an AI-powered conversational chatbot that enables natural language task management. Building upon Phase II's production-ready web application:

- **AI-Powered Conversations**: OpenAI Agents SDK for intelligent natural language understanding
- **MCP Tool Integration**: Official MCP SDK for all task operations (add/list/update/delete/complete)
- **Stateless Chat Architecture**: Every chat request is independent; no in-memory state
- **Conversation Persistence**: Neon PostgreSQL stores conversations and messages for session continuity
- **Phase II Integration**: Reuses existing Better Auth, REST endpoints, and database infrastructure

**Implementation Mandate**: All code MUST be generated exclusively from written specifications using Claude Code and Spec-Kit Plus. Manual code writing is strictly forbidden.

**Evolution Path**: Phase III builds upon Phase II (full-stack web app) to add conversational AI capabilities, demonstrating intelligent agent integration while maintaining the secure, user-isolated architecture established in earlier phases.

---

## 2. Core Principles

### I. Spec-Driven Development Only

**Non-Negotiable Rules**:
- Every feature MUST begin with a written specification in `/specs/<feature-name>/spec.md`
- No implementation work may commence without an approved specification
- All architectural decisions MUST be documented in `/specs/<feature-name>/plan.md`
- Task lists MUST be generated in `/specs/<feature-name>/tasks.md` before implementation

**Rationale**: Specifications ensure clarity, enable review before implementation, reduce rework, and create an auditable trail of requirements and decisions. This prevents scope creep and ensures alignment with project goals.

### II. Architecture First

**Non-Negotiable Rules**:
- System design MUST precede implementation
- API contracts MUST be defined before backend implementation
- Data models MUST be documented with relationships and constraints
- Security model (authentication, authorization, data isolation) MUST be established upfront

**Rationale**: Upfront architecture prevents costly refactoring, ensures scalability, maintains security posture, and enables parallel development of frontend and backend components.

### III. Reusability and Consistency

**Non-Negotiable Rules**:
- All projects MUST include a `CLAUDE.md` file with agent instructions
- Templates in `.specify/templates/` MUST be used for all artifact generation
- Naming conventions MUST be consistent across all features and components
- Shared utilities and patterns MUST be documented and reused

**Rationale**: Consistency reduces cognitive load, accelerates onboarding, prevents duplication, and ensures maintainability across the monorepo.

### IV. Iterative Refinement

**Non-Negotiable Rules**:
- Specifications MUST be refined through clarification questions until unambiguous
- Plans MUST address all edge cases and failure modes identified
- Tasks MUST be validated for completeness and correctness before execution
- Code MUST be clean, type-safe, and production-ready (no placeholders or TODOs)

**Rationale**: Iteration catches issues early when they're cheap to fix. Rushing to implementation creates technical debt that compounds over time.

### V. Phase Isolation and Technology Discipline

**Non-Negotiable Rules**:
- Technologies MUST only be introduced in their designated phase (see Technology Commitments)
- Phase I features (in-memory, console-only) MUST NOT be mixed with Phase II features
- Phase IV technologies (cloud orchestration, microservices) are STRICTLY FORBIDDEN in Phase III
- Each phase MUST complete fully before advancing to the next

**Rationale**: Phase discipline prevents scope creep, maintains focus, ensures proper foundation building, and allows thorough validation at each stage.

---

## 3. Strict Rules

### Rule 1: No Manual Code Edits

**Enforcement**: All code MUST be generated by Claude Code following specifications. Manual editing violates the Spec-Driven Development principle and creates undocumented changes.

**Exception Process**: If manual intervention is absolutely necessary, it MUST be:
1. Documented in a Prompt History Record (PHR)
2. Justified with reasoning
3. Followed by spec update to reflect the change

### Rule 2: JWT Authentication Required for All API Calls

**Enforcement**: All frontend API requests MUST include `Authorization: Bearer <JWT>` header.

**Technical Requirements**:
- JWTs issued by Better Auth
- JWTs MUST contain `user_id` claim
- Token expiration MUST be enforced
- Refresh token mechanism MUST be implemented

**Exceptions**: Only public endpoints (signup, signin, health checks) may omit authentication.

### Rule 3: Backend JWT Verification on Every Protected Route

**Enforcement**: Every protected API endpoint MUST:
1. Validate JWT signature using JWKS
2. Check token expiration
3. Extract `user_id` from verified token
4. Use `user_id` for all data access authorization

**Technical Requirements**:
- Middleware MUST verify JWT before route handler execution
- Invalid/expired tokens MUST return 401 Unauthorized
- Missing tokens MUST return 401 Unauthorized

### Rule 4: User Isolation Enforcement

**Enforcement**: All data access MUST be filtered by authenticated `user_id` from JWT.

**Technical Requirements**:
- NO `user_id` in URL paths (derived only from JWT)
- Database queries MUST include `WHERE user_id = <authenticated_user_id>`
- Cross-user data access attempts MUST return 404 Not Found (not 403, to prevent enumeration)
- User isolation MUST be enforced at the database query level, not application logic level

**Testing**: Every feature MUST include tests verifying user isolation (User A cannot access User B's data).

### Rule 5: Monorepo Structure Compliance

**Enforcement**: Project structure MUST follow hackathon rules exactly:

```
TODO-PHASE03/
├── frontend/          # Next.js application
│   ├── src/
│   │   ├── app/       # App router pages
│   │   ├── components/
│   │   └── lib/       # API client, utilities
│   └── package.json
├── backend/           # FastAPI application
│   ├── src/
│   │   ├── models/    # SQLModel entities
│   │   ├── routes/    # API endpoints
│   │   ├── services/  # Business logic
│   │   ├── auth/      # JWT verification
│   │   ├── agents/    # AI agent logic (Phase III)
│   │   └── mcp/       # MCP server and tools (Phase III)
│   └── pyproject.toml
├── .specify/          # SpecKit Plus templates and scripts
├── specs/             # Feature specifications
├── history/           # PHRs and ADRs
└── CLAUDE.md          # Agent instructions
```

**Prohibition**: Do NOT deviate from this structure without constitutional amendment.

### Rule 6: MCP Tools Only for Task Operations (Phase III)

**Enforcement**: The AI agent MUST NEVER modify database records directly. All task operations (create, read, update, delete, complete) MUST be executed through MCP tools.

**Technical Requirements**:
- MCP server exposes tools: `add_task`, `list_tasks`, `update_task`, `delete_task`, `complete_task`
- Agent interprets user intent and calls appropriate MCP tools
- Agent MUST confirm actions before execution
- Errors from MCP tools MUST be handled gracefully with user-friendly messages

**Rationale**: MCP abstraction ensures consistent business logic, audit trail, and prevents bypassing validation or user isolation.

### Rule 7: Stateless Chat Architecture (Phase III)

**Enforcement**: Every chat request MUST be independently processable. No in-memory state may persist between requests.

**Technical Requirements**:
- Chat endpoint receives `conversation_id` (optional) and `message` (required)
- Conversation history loaded from database at request start
- Response includes `conversation_id`, `response`, and `tool_calls`
- All state persisted to database before response returns

**Rationale**: Stateless architecture enables horizontal scaling, fault tolerance, and session resumption.

---

## 4. Technology Commitments (Phase Matrix)

### Phase I (Completed)
**Status**: Foundation complete, read-only reference

**Technology Stack**:
- Runtime: Python console application
- Storage: In-memory (no persistence)
- Interface: Command-line only
- Authentication: None
- Database: None

**Prohibitions**: No web frontend, no authentication, no database in Phase I.

---

### Phase II (Completed)
**Status**: Foundation complete, maintained for Phase III integration

**Backend Stack**:
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Authentication**: Better Auth (JWT-based)
- **Validation**: Pydantic models

**Frontend Stack**:
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **UI Library**: React 18+
- **Styling**: Tailwind CSS
- **HTTP Client**: fetch with JWT interceptor

**Database Stack**:
- **Provider**: Neon Serverless PostgreSQL
- **Connection**: psycopg2 or asyncpg
- **Migrations**: Alembic (if needed)
- **Schema**:
  - `users` table (managed by Better Auth)
  - `tasks` table with `user_id` foreign key

**Architecture**:
- REST API endpoints under `/api/tasks`
- Stateless authentication with JWT
- User isolation enforced at database layer
- Frontend deployed separately from backend

---

### Phase III (CURRENT PHASE)
**Status**: Active development, AI technologies authorized

**AI/Agent Stack**:
- **AI Framework**: OpenAI Agents SDK
- **Tool Protocol**: Official MCP SDK (Model Context Protocol)
- **Chat UI**: OpenAI ChatKit (frontend component)

**Backend Additions**:
- **Language**: Python 3.11+ (same as Phase II)
- **Framework**: FastAPI (reuse Phase II)
- **Agent Logic**: `backend/src/agents/` module
- **MCP Server**: `backend/src/mcp/` module exposing task tools

**Database Additions** (extend Phase II schema):
- `conversation` table: `id`, `user_id`, `created_at`, `updated_at`
- `message` table: `id`, `user_id`, `conversation_id`, `role` (user/assistant), `content`, `created_at`

**New API Endpoint**:
- `POST /api/chat` - Stateless chat endpoint
  - Request: `{ conversation_id?: string, message: string }`
  - Response: `{ conversation_id: string, response: string, tool_calls: ToolCall[] }`

**Authorization Matrix**:
✅ **Allowed**: OpenAI Agents SDK, MCP SDK, ChatKit UI, conversation/message tables, stateless chat API
✅ **Reused from Phase II**: Better Auth, JWT, REST endpoints, tasks table, user isolation
❌ **Forbidden**: Cloud orchestration, Kubernetes, event streaming, microservices decomposition

---

### Phase IV and Later (FUTURE)
**Status**: Not yet authorized, planning only

**Planned Technologies** (requires constitutional amendment to activate):
- Cloud infrastructure (AWS/Azure/GCP)
- Container orchestration (Kubernetes)
- Event streaming (Kafka/RabbitMQ)
- Microservices architecture
- Advanced ML models for task prediction

**Current Prohibition**: These technologies MUST NOT be introduced until Phase IV constitutional amendment is ratified.

---

## 5. Architecture Guidelines

### Backend Architecture (Phase II - Maintained)

**API Design**:
- Base path: `/api/tasks`
- Endpoints:
  - `GET /api/tasks` - List user's tasks (filtered by JWT user_id)
  - `POST /api/tasks` - Create new task (user_id from JWT)
  - `GET /api/tasks/{task_id}` - Get single task (verify ownership)
  - `PUT /api/tasks/{task_id}` - Update task (verify ownership)
  - `DELETE /api/tasks/{task_id}` - Delete task (verify ownership)

**Security Requirements**:
- JWT verification middleware on all `/api/tasks/*` routes
- Extract `user_id` from verified JWT claims
- Never trust `user_id` from request body or query parameters
- Return 404 for unauthorized access attempts (not 403)

**Data Model (Phase II)**:
```python
# Conceptual model (implementation details in spec)
User:
  - id (UUID, primary key)
  - email (unique, indexed)
  - created_at, updated_at

Task:
  - id (UUID, primary key)
  - user_id (UUID, foreign key to User, indexed)
  - title (string, required)
  - description (text, optional)
  - completed (boolean, default false)
  - created_at, updated_at
```

**Error Handling**:
- 400 Bad Request - Invalid input
- 401 Unauthorized - Missing or invalid JWT
- 404 Not Found - Resource not found or unauthorized access
- 500 Internal Server Error - Unexpected errors (logged securely)

---

### Frontend Architecture (Phase II - Maintained)

**Authentication Flow**:
1. User signs up/signs in via Better Auth UI
2. Backend returns JWT on successful authentication
3. Frontend stores JWT securely (httpOnly cookie or localStorage with XSS protections)
4. Frontend includes JWT in `Authorization: Bearer <token>` header on all API requests
5. Frontend handles 401 responses by redirecting to login

**API Client**:
- Centralized API client module (`frontend/src/lib/api.ts`)
- Automatic JWT injection into request headers
- Automatic token refresh handling
- Error handling with user-friendly messages

**Component Structure**:
- `app/` - Next.js App Router pages
- `components/` - Reusable UI components
- `lib/` - Utilities, API client, type definitions

---

### Database Architecture (Phase II - Maintained)

**Connection**:
- Use Neon connection string from environment variable
- Connection pooling enabled
- SSL required for production

**Schema Management**:
- Migrations managed via Alembic (if schema changes needed)
- Schema version tracked
- Rollback strategy documented

**Query Patterns**:
- Always filter by `user_id` from JWT
- Use parameterized queries to prevent SQL injection
- Index on `user_id` for performance
- Index on `created_at` for sorting

---

### AI Chatbot Architecture (Phase III)

**Chat Flow**:
1. User sends message to `POST /api/chat`
2. Backend extracts `user_id` from JWT
3. If `conversation_id` provided, load conversation history from database
4. If no `conversation_id`, create new conversation record
5. Store user message in `message` table
6. Pass conversation context to OpenAI Agent
7. Agent interprets user intent and determines required MCP tool calls
8. Agent confirms action with user (if destructive)
9. Execute MCP tool calls (add/list/update/delete/complete task)
10. Store assistant response in `message` table
11. Return response with `conversation_id`, `response`, and `tool_calls`

**Agent Rules**:
- Agent MUST interpret natural language and map to correct MCP tools
- Agent MUST confirm destructive actions (delete, complete) before execution
- Agent MUST handle errors gracefully with user-friendly messages
- Agent MUST respect user isolation (only access authenticated user's tasks)
- Agent MUST NOT bypass MCP tools to modify database directly

**Conversation Persistence**:
- Conversations enable session continuity across requests
- Message history provides context for follow-up questions
- User can resume previous conversations by providing `conversation_id`

---

### MCP Server Architecture (Phase III)

**Tool Definitions**:
```python
# MCP tools exposed by backend/src/mcp/
add_task(title: str, description: str | None) -> Task
list_tasks(completed: bool | None) -> list[Task]
update_task(task_id: str, title: str | None, description: str | None) -> Task
delete_task(task_id: str) -> bool
complete_task(task_id: str) -> Task
```

**Security**:
- All MCP tools receive `user_id` from authenticated JWT context
- Tools enforce user isolation at query level
- Tools validate input and return structured errors
- Tools log all operations for audit trail

**Error Handling**:
- Tool not found: Return helpful message listing available tools
- Invalid parameters: Return validation errors with field details
- Task not found: Return 404-equivalent structured error
- Permission denied: Return 404-equivalent (no enumeration)

---

### Conversation Database Architecture (Phase III)

**Schema Additions**:
```python
Conversation:
  - id (UUID, primary key)
  - user_id (UUID, foreign key to User, indexed)
  - created_at (timestamp)
  - updated_at (timestamp)

Message:
  - id (UUID, primary key)
  - user_id (UUID, foreign key to User, indexed)
  - conversation_id (UUID, foreign key to Conversation, indexed)
  - role (enum: 'user', 'assistant')
  - content (text, required)
  - created_at (timestamp)
```

**Query Patterns**:
- Load conversation: `WHERE conversation_id = ? AND user_id = ?`
- Load messages: `WHERE conversation_id = ? ORDER BY created_at ASC`
- User isolation enforced on both Conversation and Message queries

---

## 6. Quality Standards

### Code Quality

**Type Safety**:
- Backend: Pydantic models for all request/response bodies
- Frontend: TypeScript strict mode enabled
- No `any` types without explicit justification

**Formatting**:
- Backend: Black formatter, isort for imports
- Frontend: Prettier with consistent config
- Line length: 88 characters (Python), 100 characters (TypeScript)

**Linting**:
- Backend: pylint, mypy for type checking
- Frontend: ESLint with recommended rules
- No warnings allowed in production builds

### Testing Standards

**Test Coverage** (if tests requested):
- Unit tests for business logic
- Integration tests for API endpoints
- Contract tests for API schemas
- User isolation tests (verify User A cannot access User B's data)
- Agent behavior tests (verify correct tool selection)

**Test Organization**:
- `tests/unit/` - Pure function tests
- `tests/integration/` - Database and API tests
- `tests/contract/` - API schema validation
- `tests/agent/` - AI agent behavior tests (Phase III)

### Documentation Standards

**Code Documentation**:
- Public APIs: Docstrings with parameters, return types, exceptions
- Complex logic: Inline comments explaining "why", not "what"
- No commented-out code in production

**Feature Documentation**:
- `specs/<feature>/spec.md` - Requirements and user stories
- `specs/<feature>/plan.md` - Architecture and decisions
- `specs/<feature>/quickstart.md` - Getting started guide
- `specs/<feature>/tasks.md` - Implementation checklist

**Process Documentation**:
- Prompt History Records (PHRs) in `history/prompts/`
- Architecture Decision Records (ADRs) in `history/adr/`
- `CLAUDE.md` - Agent instructions and project context

---

## 7. Security Requirements

### Authentication Security

**JWT Requirements**:
- Algorithm: RS256 (asymmetric)
- Expiration: 1 hour maximum
- Refresh tokens: 7 days maximum
- JWKS endpoint for public key verification

**Password Security** (managed by Better Auth):
- Minimum 8 characters
- Hashed with bcrypt (cost factor 12+)
- Never logged or exposed in errors

### Data Security

**User Isolation**:
- Every query MUST filter by `user_id` from JWT
- Database-level constraints enforced
- Application-level checks as defense in depth

**Input Validation**:
- All user input validated against schemas
- SQL injection prevention via parameterized queries
- XSS prevention via output encoding

**Secrets Management**:
- Database credentials in environment variables
- JWT signing keys in secure storage
- OpenAI API keys in environment variables (Phase III)
- Never commit secrets to repository
- `.env` files in `.gitignore`

### API Security

**CORS Configuration**:
- Whitelist frontend origin only
- No wildcard origins in production

**Rate Limiting**:
- Per-user rate limits on authenticated endpoints
- Per-IP rate limits on public endpoints
- Chat endpoint rate limiting to prevent abuse (Phase III)

### AI Security (Phase III)

**Prompt Injection Prevention**:
- User messages treated as untrusted input
- Agent instructions separated from user content
- No dynamic prompt construction from user input

**Tool Execution Safety**:
- MCP tools validate all parameters
- User isolation enforced in tool execution
- Destructive actions require confirmation
- All tool calls logged for audit

**Data Leakage Prevention**:
- Agent only accesses authenticated user's data
- Conversation history scoped to user
- No cross-user data exposure via agent responses

---

## 8. Governance

### Constitutional Authority

This constitution supersedes all other development practices, guidelines, or conventions. In case of conflict, constitutional provisions take precedence.

### Amendment Process

**Requirements for Amendment**:
1. **Proposal**: Written amendment proposal with justification
2. **Review**: Architectural review for impact assessment
3. **Approval**: User approval required
4. **Migration**: Migration plan for affected specifications and code
5. **Documentation**: PHR created for constitutional amendment
6. **Version Bump**: MAJOR version increment for breaking changes, MINOR for additions

### Version Semantics

**Version Format**: MAJOR.MINOR.PATCH

- **MAJOR**: Backward-incompatible governance changes (principle removal/redefinition, new phase activation)
- **MINOR**: New principles, sections, or material expansions within current phase
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Review

**PR Requirements**:
- All pull requests MUST verify constitutional compliance
- Reviewers MUST check adherence to phase restrictions
- Complexity MUST be justified against simplicity principles

**Periodic Audits**:
- Constitution alignment reviewed at phase transitions
- Technology drift detected and corrected
- Process improvements proposed via amendments

### Runtime Guidance

For day-to-day development guidance, consult:
- `.specify/memory/constitution.md` (this file) - Principles and rules
- `CLAUDE.md` - Agent-specific instructions and workflows
- `.specify/templates/` - Artifact templates for specs, plans, tasks, PHRs, ADRs

---

**Version**: 3.0.0
**Ratified**: 2026-01-11
**Last Amended**: 2026-01-20
