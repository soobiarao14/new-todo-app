---
id: 0001
title: Phase II Constitution Ratification
stage: constitution
date: 2026-01-11
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: Since Tech
command: /sp.constitution
labels: ["constitution", "governance", "phase-ii", "full-stack-web"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - history/prompts/constitution/0001-phase-ii-constitution-ratification.constitution.prompt.md
tests:
 - none
---

## Prompt

```text

Amend and establish the global Project Constitution for the "Evolution of Todo" hackathon project.

Create a new Markdown file at the root of the monorepo named `Constitution.md`.

This document is the authoritative governing constitution for Phase II and must preserve strict phase isolation across the project lifecycle.

====================
PROJECT CONSTITUTION
====================

Title:
# Project Constitution – Evolution of Todo (Phase II: Full-Stack Web Application)

--------------------
1. Vision
--------------------
Define Phase II as a modern, multi-user Todo full-stack web application with:

- Persistent storage using Neon Serverless PostgreSQL
- User authentication via Better Auth with stateless JWT
- Full CRUD operations on todos
- Strict user isolation

All implementation MUST be generated exclusively from written specifications using Claude Code and Spec-Kit Plus.
Manual code writing is strictly forbidden.

Clarify that Phase II evolves Phase I (in-memory console app) into a production-ready web system and lays the foundation for later AI and cloud-native phases.

--------------------
2. Core Principles
--------------------
Include and enforce:

- Spec-Driven Development Only (everything starts in /specs/)
- Architecture First thinking
- Reusability and consistency with CLAUDE.md files
- Iterative refinement until correct, clean, production-quality output

--------------------
3. Strict Rules
--------------------
Define hard rules:

- No manual code edits
- All frontend API calls require Authorization: Bearer <JWT>
- Backend must verify JWT on every protected route
- All data access must be filtered by authenticated user_id from JWT
- Absolute user isolation (no cross-user access)
- Monorepo structure must exactly follow hackathon rules

--------------------
4. Technology Commitments (Phase Matrix)
--------------------
Define a clear phase-based technology policy:

Phase I:
- In-memory console application only
- No authentication
- No database
- No web frontend

Phase II (CURRENT PHASE):
- Backend: Python REST API (FastAPI)
- Database: Neon Serverless PostgreSQL
- ORM/Data Layer: SQLModel or equivalent
- Frontend: Next.js (React, TypeScript)
- Authentication: Better Auth (signup/signin, JWT)
- Architecture: Full-stack web application

Phase III and Later:
- Advanced cloud infrastructure
- AI systems
- Agent frameworks
- Orchestration and automation

Explicit Rules:
- Authentication allowed starting Phase II
- Web frontend allowed starting Phase II
- Neon PostgreSQL allowed starting Phase II
- AI, agents, and orchestration are strictly forbidden until later phases

--------------------
5. Architecture Guidelines
--------------------
Specify:

- Monorepo with /frontend and /backend
- REST endpoints under /api/tasks
- No user_id in URLs (derived only from JWT)
- Stateless auth with JWKS verification
- users table managed by Better Auth
- tasks table with user_id foreign key
- Proper HTTP errors and security practices

--------------------
6. Quality Standards
--------------------
Enforce:

- Clean, type-safe code
- Testing standards (when tests requested)
- Documentation requirements
- Security best practices
```

## Response snapshot

Constitution successfully created at `.specify/memory/constitution.md` with the following key sections:

**Version**: 2.0.0 (MAJOR - complete governance establishment for Phase II)

**Established Principles**:
1. Spec-Driven Development Only - All features must start with written specifications
2. Architecture First - System design must precede implementation
3. Reusability and Consistency - CLAUDE.md files and templates mandatory
4. Iterative Refinement - Specifications refined through clarification until unambiguous
5. Phase Isolation and Technology Discipline - Technologies only introduced in designated phases

**Strict Rules Enforced**:
- No manual code edits (all code generated from specifications)
- JWT authentication required on all frontend API calls
- Backend JWT verification on every protected route
- User isolation enforcement (data filtered by JWT user_id)
- Monorepo structure compliance (frontend/, backend/, .specify/, specs/, history/)

**Technology Phase Matrix**:
- Phase I: Console-only, in-memory, no auth (completed, reference only)
- Phase II: FastAPI + Next.js + Neon PostgreSQL + Better Auth (current, authorized)
- Phase III+: AI/agents/orchestration (future, currently forbidden)

**Architecture Guidelines**:
- REST API at `/api/tasks` with full CRUD operations
- Stateless JWT authentication with JWKS verification
- User/Task data model with proper foreign keys
- Security: 404 for unauthorized access (not 403 to prevent enumeration)

**Quality Standards**:
- Type safety: Pydantic (backend), TypeScript strict mode (frontend)
- Code formatting: Black (Python), Prettier (TypeScript)
- Testing: Unit, integration, contract, user isolation tests (when requested)
- Documentation: Specs, plans, tasks, PHRs, ADRs mandatory

**Governance**:
- Constitutional authority supersedes all other practices
- Amendment process requires proposal, review, approval, migration, documentation
- Semantic versioning for constitution (MAJOR.MINOR.PATCH)
- Compliance review in all PRs and at phase transitions

## Outcome

- ✅ Impact: Project constitution established as authoritative governance document for Phase II full-stack web application development
- 🧪 Tests: No tests required (governance document)
- 📁 Files: Created `.specify/memory/constitution.md` (486 lines), created PHR in `history/prompts/constitution/`
- 🔁 Next prompts: `/sp.specify <feature-name>` to create first Phase II feature specification following constitutional principles
- 🧠 Reflection: Constitution provides clear phase isolation, technology commitments, security requirements (JWT + user isolation), and spec-driven development mandate. All templates already aligned with constitutional requirements.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution successfully generated with all placeholders resolved
- Graders run and results (PASS/FAIL): N/A (governance document, no automated grading applicable)
- Prompt variant (if applicable): Standard constitutional amendment prompt with detailed Phase II requirements
- Next experiment (smallest change to try): Validate constitutional compliance by creating first Phase II feature specification (`/sp.specify full-stack-web-app` or similar) to ensure all principles are practically enforceable
