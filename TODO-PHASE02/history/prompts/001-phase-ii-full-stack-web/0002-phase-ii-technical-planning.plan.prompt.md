---
id: 0002
title: Phase II Technical Planning
stage: plan
date: 2026-01-11
surface: agent
model: claude-sonnet-4-5
feature: 001-phase-ii-full-stack-web
branch: 001-phase-ii-full-stack-web
user: Since Tech
command: /sp.plan
labels: ["planning", "architecture", "phase-ii", "full-stack-web", "fastapi", "nextjs"]
links:
  spec: C:/Users/Since Tech/specs/001-phase-ii-full-stack-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - C:/Users/Since Tech/specs/001-phase-ii-full-stack-web/plan.md
 - C:/Users/Since Tech/specs/001-phase-ii-full-stack-web/research.md
 - C:/Users/Since Tech/specs/001-phase-ii-full-stack-web/data-model.md
 - C:/Users/Since Tech/specs/001-phase-ii-full-stack-web/contracts/auth-api.md
 - C:/Users/Since Tech/specs/001-phase-ii-full-stack-web/contracts/tasks-api.md
 - C:/Users/Since Tech/specs/001-phase-ii-full-stack-web/contracts/schemas.md
 - C:/Users/Since Tech/specs/001-phase-ii-full-stack-web/quickstart.md
tests:
 - none
---

## Prompt

Create the Phase II technical plan for the "Evolution of Todo" project.

This plan MUST be strictly derived from:
- The approved Phase II specification
- The global Constitution.md

The plan explains HOW Phase II will be built at a technical and architectural level.
It must not introduce new features, future-phase ideas, or implementation code.

[User provided detailed planning requirements including Backend Plan, Frontend Plan, Database Plan, Integration Plan, and Plan Constraints]

## Response snapshot

Successfully created comprehensive Phase II technical plan with complete Phase 0 research and Phase 1 design artifacts.

**Artifacts Generated**:

1. **plan.md**: Technical architecture defining HOW Phase II will be built
   - Technical context (Python 3.11+, TypeScript, FastAPI, Next.js, Neon, Better Auth)
   - Constitution check (all Phase II technologies authorized, Phase III prohibited)
   - Backend architecture (REST API, JWT verification, user isolation)
   - Frontend architecture (Next.js App Router, responsive UI, auth state)
   - Database architecture (User/Todo models, relationships, query patterns)
   - Integration architecture (token flow, local development)
   - Security architecture (JWT verification, user isolation enforcement)
   - Performance, testing, deployment, risk mitigation strategies

2. **research.md** (Phase 0): Technology integration research
   - Better Auth + FastAPI integration pattern (JWKS verification)
   - Neon PostgreSQL connection patterns (SSL, pooling, SQLModel)
   - SQLModel best practices (entity modeling, query scoping)
   - Next.js App Router patterns (Server Components, auth middleware)
   - **JWT Storage Decision**: httpOnly cookies (XSS protection, CSRF mitigation)
   - User isolation implementation (database-level filtering)
   - Frontend state management (React Context, no global library)
   - API response schemas (Pydantic models, OpenAPI docs)
   - CORS configuration (credentials support)
   - Error response format (consistent JSON structure)

3. **data-model.md** (Phase 1): Entity schemas and relationships
   - **User Entity**: Better Auth managed, read-only for app (id, email, password_hash, timestamps)
   - **Todo Entity**: App-managed (id, user_id FK, title, description, completed, timestamps)
   - One-to-many relationship (User → Todos)
   - Validation rules (title required/max 200, description optional/max 2000)
   - Query patterns with user_id filtering
   - SQLModel class definitions
   - Database schema (SQL)

4. **contracts/** (Phase 1): API endpoint contracts
   - **auth-api.md**: Better Auth endpoints (POST /auth/signup, POST /auth/signin, POST /auth/signout, GET /auth/session)
   - **tasks-api.md**: Todo CRUD endpoints (GET /api/tasks, POST /api/tasks, GET /api/tasks/{id}, PUT /api/tasks/{id}, PATCH /api/tasks/{id}/complete, DELETE /api/tasks/{id})
   - **schemas.md**: Request/response schemas (Pydantic backend, TypeScript frontend) with validation rules

5. **quickstart.md** (Phase 1): Local development setup guide
   - Prerequisites (Python 3.11+, Node.js 18+, Neon account, Better Auth)
   - Database setup (Neon connection, schema initialization)
   - Backend setup (venv, dependencies, .env configuration, start server)
   - Frontend setup (npm install, .env.local configuration, start dev server)
   - Running application (both services, testing flows)
   - User isolation testing (two-user scenarios)
   - Troubleshooting (common issues and solutions)
   - Environment variables reference

**Key Design Decisions**:

1. **JWT Storage**: httpOnly cookies selected for XSS protection over localStorage
2. **User Isolation**: Enforced at database query level with automatic user_id filtering in service layer
3. **Error Responses**: 404 (not 403) for unauthorized access to prevent enumeration
4. **Authentication Flow**: Better Auth handles all user management, FastAPI verifies JWTs via JWKS
5. **State Management**: React Context for auth state, no global state library (Phase II simplicity)
6. **Database Schema**: SQLModel declarative models with foreign key enforcement

**Architecture Layers**:

- **Backend**: 3-layer (routes → services → models) with middleware for JWT verification
- **Frontend**: Next.js App Router with page components (data fetching) and reusable UI components
- **Database**: Neon PostgreSQL with user_id foreign key and indexes for query performance

**Security Measures**:

- JWT verification on all protected routes via JWKS
- User isolation at database query level
- httpOnly cookies for token storage
- No user_id accepted from client input
- Bcrypt password hashing (Better Auth)
- CORS whitelisting
- Generic error messages (prevent enumeration)

**Constitutional Compliance**: ✅ All Phase II technologies authorized, no Phase III features, strict user isolation enforced, spec-driven development followed

## Outcome

- ✅ Impact: Complete technical architecture and design artifacts for Phase II full-stack web application
- 🧪 Tests: No tests required (planning phase)
- 📁 Files: Created 7 planning artifacts (plan, research, data-model, 3 contracts, quickstart)
- 🔁 Next prompts: `/sp.tasks` to generate implementation task list from plan
- 🧠 Reflection: Planning phase successfully completed with all technical unknowns resolved through research. Key decisions documented (JWT storage, user isolation strategy, state management). All artifacts ready for task generation and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - all planning artifacts generated successfully with constitutional compliance
- Graders run and results (PASS/FAIL): PASS - Constitution check verified all Phase II technologies, no Phase III features introduced
- Prompt variant (if applicable): Standard /sp.plan prompt with user-provided architectural structure
- Next experiment (smallest change to try): Proceed to `/sp.tasks` to validate that plan provides sufficient detail for task breakdown without ambiguity. Verify user story mapping to tasks.
