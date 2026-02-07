<!--
SYNC IMPACT REPORT:
==================
Version Change: 3.0.0 → 4.0.0 (MAJOR)
Date: 2026-02-06
Rationale: Activation of Phase IV with cloud-native deployment technologies
           (Docker, Kubernetes/Minikube, Helm charts, AI-assisted DevOps).
           This constitutes a major architectural expansion from application
           development to container orchestration and deployment.

Modified Principles:
- Phase Isolation and Technology Discipline: Updated to reflect Phase IV authorization
- Technology Commitments: Phase IV now active, Phase V added as future

Added Sections:
- Section 4.4: Phase IV Technology Stack (Cloud Native Deployment)
- Section 5.7: Container Architecture (Docker)
- Section 5.8: Helm Chart Architecture
- Section 5.9: Kubernetes Deployment Architecture
- Section 5.10: AI-Assisted DevOps Architecture
- Section 7.4: Container and Cluster Security Requirements
- Strict Rules: Rule 8 (Container Image Standards), Rule 9 (Helm Chart Discipline)

Removed Sections:
- None (Phase III rules preserved in full)

Templates Requiring Updates:
✅ plan-template.md - Constitution Check section compatible
✅ spec-template.md - Requirements section compatible
✅ tasks-template.md - Task organization compatible (deployment phases supported)
✅ CLAUDE.md - References constitution correctly

Follow-up TODOs:
- None - all placeholders resolved
-->

# Evolution of Todo – Project Constitution (Phase IV: Cloud Native Deployment)

## 1. Vision

**Phase IV Objective**: Deploy the Phase III Todo AI Chatbot as a cloud-native application on a local Kubernetes cluster using Minikube, Docker containers, and Helm charts. This phase introduces containerization, orchestration, and AI-assisted DevOps workflows.

- **Containerization**: Docker images for frontend (Node.js), backend (Python/FastAPI), and database (PostgreSQL)
- **Orchestration**: Minikube-based local Kubernetes cluster with Helm chart deployments
- **AI-Assisted DevOps**: Docker Gordon for image generation, kubectl-ai for deployment, kagent for cluster intelligence
- **Helm Charts**: Templated, repeatable deployments with configurable values for all services
- **Ingress Routing**: Local domain routing via `todo.local` for frontend access

**Implementation Mandate**: All code MUST be generated exclusively from written specifications using Claude Code and Spec-Kit Plus. Manual code writing is strictly forbidden.

**Evolution Path**: Phase IV builds upon Phase III (AI chatbot) and Phase II (full-stack web app) to demonstrate cloud-native deployment practices. The application remains functionally identical; this phase focuses exclusively on containerization, orchestration, and deployment automation.

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
- Container architecture (base images, multi-stage builds, resource limits) MUST be designed before Dockerfile creation (Phase IV)
- Helm chart structure MUST be planned before chart generation (Phase IV)

**Rationale**: Upfront architecture prevents costly refactoring, ensures scalability, maintains security posture, and enables parallel development of frontend and backend components.

### III. Reusability and Consistency

**Non-Negotiable Rules**:
- All projects MUST include a `CLAUDE.md` file with agent instructions
- Templates in `.specify/templates/` MUST be used for all artifact generation
- Naming conventions MUST be consistent across all features and components
- Shared utilities and patterns MUST be documented and reused
- Helm values MUST be parameterized for environment-specific configuration (Phase IV)

**Rationale**: Consistency reduces cognitive load, accelerates onboarding, prevents duplication, and ensures maintainability across the monorepo.

### IV. Iterative Refinement

**Non-Negotiable Rules**:
- Specifications MUST be refined through clarification questions until unambiguous
- Plans MUST address all edge cases and failure modes identified
- Tasks MUST be validated for completeness and correctness before execution
- Code MUST be clean, type-safe, and production-ready (no placeholders or TODOs)
- Container images MUST be tested locally before Kubernetes deployment (Phase IV)

**Rationale**: Iteration catches issues early when they're cheap to fix. Rushing to implementation creates technical debt that compounds over time.

### V. Phase Isolation and Technology Discipline

**Non-Negotiable Rules**:
- Technologies MUST only be introduced in their designated phase (see Technology Commitments)
- Phase I features (in-memory, console-only) MUST NOT be mixed with Phase II features
- Phase V technologies (cloud providers, CI/CD pipelines, production monitoring) are STRICTLY FORBIDDEN in Phase IV
- Each phase MUST complete fully before advancing to the next

**Rationale**: Phase discipline prevents scope creep, maintains focus, ensures proper foundation building, and allows thorough validation at each stage.

### VI. Infrastructure as Code (Phase IV)

**Non-Negotiable Rules**:
- All deployment configurations MUST be declarative (Helm charts, Kubernetes manifests)
- No manual `kubectl` commands for production-equivalent deployments; use Helm releases
- Container images MUST be reproducible from Dockerfiles (no manual image modifications)
- Environment differences MUST be captured in Helm values files, not hardcoded
- All infrastructure artifacts MUST be version-controlled

**Rationale**: Infrastructure as Code ensures reproducibility, auditability, and eliminates configuration drift. Declarative deployments enable rollback and environment parity.

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

**Enforcement**: Project structure MUST follow the established pattern:

```
TODO-PHASE04/
├── frontend/          # Next.js application
│   ├── src/
│   │   ├── app/       # App router pages
│   │   ├── components/
│   │   └── lib/       # API client, utilities
│   ├── Dockerfile     # Frontend container image (Phase IV)
│   └── package.json
├── backend/           # FastAPI application
│   ├── src/
│   │   ├── models/    # SQLModel entities
│   │   ├── routes/    # API endpoints
│   │   ├── services/  # Business logic
│   │   ├── auth/      # JWT verification
│   │   ├── agents/    # AI agent logic (Phase III)
│   │   └── mcp/       # MCP server and tools (Phase III)
│   ├── Dockerfile     # Backend container image (Phase IV)
│   └── pyproject.toml
├── helm/              # Helm charts (Phase IV)
│   ├── todo-frontend/ # Frontend Helm chart
│   ├── todo-backend/  # Backend Helm chart
│   └── todo-database/ # Database Helm chart
├── k8s/               # Raw Kubernetes manifests (Phase IV, optional)
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

### Rule 8: Container Image Standards (Phase IV)

**Enforcement**: All Docker images MUST follow these standards:

**Technical Requirements**:
- MUST use multi-stage builds to minimize final image size
- MUST use Alpine-based or slim base images (e.g., `node:20-alpine`, `python:3.12-slim`)
- MUST NOT include development dependencies in production images
- MUST NOT run containers as root; use non-root users
- MUST NOT embed secrets in images; use environment variables or Kubernetes secrets
- MUST include health check endpoints for liveness and readiness probes
- Images MUST be loadable into Minikube via `minikube image load`

**Rationale**: Small, secure, and reproducible images reduce attack surface, speed up deployments, and prevent secret leakage.

### Rule 9: Helm Chart Discipline (Phase IV)

**Enforcement**: All Kubernetes deployments MUST be managed through Helm charts.

**Technical Requirements**:
- Every service (frontend, backend, database) MUST have its own Helm chart
- All configurable values MUST be in `values.yaml`, not hardcoded in templates
- Resource requests and limits MUST be defined for every container
- Service type, replica count, and image tags MUST be parameterizable
- Charts MUST pass `helm lint` before deployment
- Charts MUST include NOTES.txt with post-install instructions

**Rationale**: Helm charts provide repeatable, version-controlled deployments with environment-specific overrides and easy rollback capability.

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
**Status**: Foundation complete, maintained for Phase III and IV integration

**Backend Stack**:
- **Language**: Python 3.12+
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

### Phase III (Completed)
**Status**: Complete, maintained for Phase IV containerization

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

---

### Phase IV (CURRENT PHASE)
**Status**: Active development, cloud-native deployment technologies authorized

**Container Stack**:
- **Container Runtime**: Docker Desktop
- **AI Image Generation**: Docker Gordon (AI Agent) for Dockerfile generation
- **Frontend Image**: `todo-frontend` based on `node:20-alpine`
  - Container port: 3000
  - Multi-stage build: install → build → serve with Node.js standalone server
- **Backend Image**: `todo-backend` based on `python:3.12-slim`
  - Container port: 8000
  - Multi-stage build: install deps → copy source → run uvicorn
- **Database Image**: `postgres:15-alpine` (official image)
  - Container port: 5432
  - Environment: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`

**Orchestration Stack**:
- **Cluster**: Minikube (local Kubernetes)
- **Package Manager**: Helm 3
- **AI Deployment**: kubectl-ai for natural language Kubernetes operations
- **AI Cluster Analysis**: kagent for cluster health and optimization

**Helm Charts**:
- **todo-frontend** (chart version 0.1.0):
  - Templates: deployment.yaml, service.yaml, ingress.yaml
  - Default replicas: 2
  - Service type: ClusterIP, port 3000
  - Ingress host: `todo.local`
- **todo-backend** (chart version 0.1.0):
  - Templates: deployment.yaml, service.yaml
  - Default replicas: 2
  - Service type: ClusterIP, port 8000
- **todo-database** (chart version 0.1.0):
  - Templates: deployment.yaml, service.yaml, pvc.yaml
  - Default replicas: 1
  - Service type: ClusterIP, port 5432
  - Persistent volume for data durability

**Kubernetes Resources**:
- Deployments: frontend (2 replicas), backend (2 replicas), database (1 replica)
- Services: ClusterIP for all internal communication
- Ingress: NGINX ingress controller for `todo.local` routing
- ConfigMaps: Application configuration
- Secrets: Database credentials, JWT signing keys, API keys
- PersistentVolumeClaims: Database storage

**Authorization Matrix**:
✅ **Allowed**: Docker, Minikube, Helm 3, kubectl, Docker Gordon, kubectl-ai, kagent, NGINX Ingress
✅ **Reused from Phase III**: OpenAI Agents SDK, MCP SDK, ChatKit UI, conversation/message tables
✅ **Reused from Phase II**: Better Auth, JWT, REST endpoints, tasks table, user isolation
❌ **Forbidden**: Cloud providers (AWS/Azure/GCP), CI/CD pipelines (GitHub Actions, ArgoCD), production monitoring (Prometheus/Grafana), service mesh (Istio), event streaming (Kafka)

---

### Phase V and Later (FUTURE)
**Status**: Not yet authorized, planning only

**Planned Technologies** (requires constitutional amendment to activate):
- Cloud infrastructure (AWS/Azure/GCP)
- CI/CD pipelines (GitHub Actions, ArgoCD)
- Production monitoring and observability (Prometheus, Grafana, Loki)
- Service mesh (Istio)
- Event streaming (Kafka/RabbitMQ)
- Advanced ML models for task prediction
- Multi-cluster deployment

**Current Prohibition**: These technologies MUST NOT be introduced until Phase V constitutional amendment is ratified.

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

### AI Chatbot Architecture (Phase III - Maintained)

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

### MCP Server Architecture (Phase III - Maintained)

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

### Conversation Database Architecture (Phase III - Maintained)

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

### Container Architecture (Phase IV)

**Frontend Dockerfile** (`frontend/Dockerfile`):
```dockerfile
# Conceptual multi-stage build
Stage 1 (build): node:20-alpine
  - Install dependencies (npm ci)
  - Build Next.js application (npm run build)

Stage 2 (production): node:20-alpine
  - Copy built artifacts (standalone output)
  - Run as non-root user
  - Expose port 3000
  - CMD: node server.js (Next.js standalone server)
  - Health check on /
```

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
# Conceptual multi-stage build
Stage 1 (build): python:3.12-slim
  - Install system dependencies
  - Install Python dependencies (pip install)

Stage 2 (production): python:3.12-slim
  - Copy installed packages and source
  - Run as non-root user
  - Expose port 8000
  - Health check on /health
```

**Image Naming Convention**:
- `todo-frontend:latest` / `todo-frontend:<version>`
- `todo-backend:latest` / `todo-backend:<version>`
- `postgres:15-alpine` (official, unmodified)

**Image Loading**:
- Build images locally with Docker
- Load into Minikube: `minikube image load <image>`
- No remote registry required for local development

---

### Helm Chart Architecture (Phase IV)

**Chart Structure** (per service):
```
helm/todo-<service>/
├── Chart.yaml           # Chart metadata and version
├── values.yaml          # Default configuration values
├── templates/
│   ├── deployment.yaml  # Kubernetes Deployment
│   ├── service.yaml     # Kubernetes Service
│   ├── ingress.yaml     # Ingress (frontend only)
│   ├── pvc.yaml         # PersistentVolumeClaim (database only)
│   ├── configmap.yaml   # Configuration (optional)
│   ├── secret.yaml      # Secrets (optional)
│   ├── _helpers.tpl     # Template helpers
│   └── NOTES.txt        # Post-install instructions
└── .helmignore          # Files to exclude
```

**Values Strategy**:
- `image.repository`: Image name
- `image.tag`: Image version (default: `latest`)
- `image.pullPolicy`: Pull policy (default: `Never` for custom images loaded via `minikube image load`; `IfNotPresent` for official images like postgres)
- `replicaCount`: Number of replicas
- `service.type`: Service type (default: `ClusterIP`)
- `service.port`: Service port
- `resources.requests`: CPU/memory requests
- `resources.limits`: CPU/memory limits
- `ingress.enabled`: Enable ingress (frontend only)
- `ingress.host`: Ingress hostname

**Inter-Service Communication**:
- Frontend → Backend: Via Kubernetes Service DNS (`todo-backend.<namespace>.svc.cluster.local:8000`)
- Backend → Database: Via Kubernetes Service DNS (`todo-database.<namespace>.svc.cluster.local:5432`)
- External → Frontend: Via Ingress on `todo.local`

---

### Kubernetes Deployment Architecture (Phase IV)

**Cluster Setup**:
- Minikube with default driver (Docker or Hyper-V on Windows)
- NGINX Ingress Controller enabled: `minikube addons enable ingress`
- DNS resolution: Add `todo.local` to hosts file pointing to Minikube IP

**Deployment Strategy**:
1. Start Minikube cluster
2. Enable ingress addon
3. Build Docker images locally
4. Load images into Minikube
5. Deploy database first (dependency)
6. Deploy backend (depends on database)
7. Deploy frontend (depends on backend)
8. Verify all pods running and healthy

**Resource Allocation**:
| Service | Replicas | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|----------|-------------|-----------|----------------|--------------|
| Frontend | 2 | 100m | 250m | 128Mi | 256Mi |
| Backend | 2 | 100m | 500m | 128Mi | 512Mi |
| Database | 1 | 100m | 500m | 256Mi | 512Mi |

**Health Checks**:
- Frontend: HTTP GET `/` (liveness), HTTP GET `/` (readiness)
- Backend: HTTP GET `/health` (liveness), HTTP GET `/health` (readiness)
- Database: TCP check on port 5432

---

### AI-Assisted DevOps Architecture (Phase IV)

**Docker Gordon (AI Image Generation)**:
- Generate optimized Dockerfiles for frontend and backend
- Suggest multi-stage build patterns
- Analyze image size and recommend optimizations
- Commands: `docker ai "Generate Dockerfile for frontend"`

**kubectl-ai (AI Deployment)**:
- Natural language Kubernetes operations
- Deploy services: `"deploy todo frontend with 2 replicas"`
- Scale operations: `"scale backend to 3 replicas"`
- Troubleshoot: `"check why pods are failing"`

**kagent (Cluster Intelligence)**:
- Analyze cluster health and resource utilization
- Identify bottlenecks and optimization opportunities
- Recommend scaling strategies
- Commands: `"analyze cluster health"`, `"optimize resource allocation"`

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
- Helm charts: `helm lint` MUST pass (Phase IV)
- Dockerfiles: Follow hadolint recommendations (Phase IV)

### Testing Standards

**Test Coverage** (if tests requested):
- Unit tests for business logic
- Integration tests for API endpoints
- Contract tests for API schemas
- User isolation tests (verify User A cannot access User B's data)
- Agent behavior tests (verify correct tool selection)
- Container build tests (verify images build successfully) (Phase IV)
- Helm chart validation (verify charts render correctly) (Phase IV)

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
- Kubernetes Secrets for sensitive values in cluster (Phase IV)
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

### AI Security (Phase III - Maintained)

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

### Container and Cluster Security (Phase IV)

**Container Security**:
- Containers MUST run as non-root users
- Read-only root filesystem where possible
- No privileged containers
- Minimal base images to reduce attack surface
- No secrets baked into images

**Kubernetes Security**:
- Kubernetes Secrets for all sensitive configuration
- Network policies to restrict inter-pod communication (if supported by Minikube CNI)
- Resource limits enforced to prevent resource exhaustion
- Service accounts with minimal permissions

**Image Security**:
- Use specific image tags (not `latest` in production). Local Minikube development MAY use `latest` when images are loaded via `minikube image load`
- Verify base image provenance (official images only)
- Scan images for known vulnerabilities when tooling available

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

**Version**: 4.0.0
**Ratified**: 2026-01-11
**Last Amended**: 2026-02-06
