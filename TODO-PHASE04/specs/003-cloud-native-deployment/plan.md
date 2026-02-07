# Implementation Plan: Cloud Native Deployment

**Branch**: `003-cloud-native-deployment` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-cloud-native-deployment/spec.md`

## Summary

Deploy the Phase III Todo AI Chatbot (frontend + backend + database) as containerized workloads on a local Minikube Kubernetes cluster. The approach uses Docker multi-stage builds for image creation, Helm 3 charts for templated deployment, and AI-assisted DevOps tools (Docker Gordon, kubectl-ai, kagent) for augmented operations. The application code remains unmodified except for `next.config.ts` (adding `output: "standalone"` for Docker compatibility) and a `/health` endpoint on the backend.

## Technical Context

**Language/Version**: Python 3.12+ (backend), TypeScript/Node 20 (frontend), SQL (database)
**Primary Dependencies**: Docker Desktop, Minikube, Helm 3, kubectl, NGINX Ingress
**Storage**: PostgreSQL 15 via PersistentVolumeClaim in Kubernetes
**Testing**: `helm lint`, `docker build` verification, `kubectl get pods` health checks, manual browser testing
**Target Platform**: Windows (Docker Desktop driver), Minikube local Kubernetes
**Project Type**: Web application (frontend + backend + database) with deployment layer
**Performance Goals**: All services reach Running state within 3 minutes; pod recovery within 30 seconds
**Constraints**: Local-only (no cloud provider), no CI/CD pipeline, images < 500MB each
**Scale/Scope**: 3 services, 5 pods total (2 frontend + 2 backend + 1 database), single Minikube node

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Principle/Rule | Status | Evidence |
|---|---------------|--------|----------|
| I | Spec-Driven Development | PASS | spec.md written and validated before plan |
| II | Architecture First | PASS | Container architecture, Helm structure, and K8s deployment strategy designed before implementation |
| III | Reusability and Consistency | PASS | Helm values parameterized; consistent chart structure across all 3 services |
| IV | Iterative Refinement | PASS | Spec validated with 16/16 checklist items; plan includes phased approach |
| V | Phase Isolation | PASS | Only Phase IV technologies used (Docker, Minikube, Helm); Phase V forbidden tech excluded |
| VI | Infrastructure as Code | PASS | All deployments via Helm charts; no manual kubectl apply for production workloads |
| R1 | No Manual Code Edits | PASS | All code generated via Claude Code per spec |
| R5 | Monorepo Structure | PASS | `helm/`, `k8s/` directories added per constitution v4.0.0 Rule 5 |
| R8 | Container Image Standards | PASS | Multi-stage builds, Alpine/slim bases, non-root users, no embedded secrets |
| R9 | Helm Chart Discipline | PASS | Per-service charts, values.yaml parameterization, helm lint required |

**Gate Result**: ALL PASS - proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/003-cloud-native-deployment/
├── plan.md              # This file
├── research.md          # Phase 0: Technology research and decisions
├── data-model.md        # Phase 1: Infrastructure entity model
├── quickstart.md        # Phase 1: Developer setup guide
├── contracts/           # Phase 1: Helm values contracts
│   ├── frontend-values.yaml
│   ├── backend-values.yaml
│   └── database-values.yaml
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2: Task breakdown (created by /sp.tasks)
```

### Source Code (repository root)

```text
TODO-PHASE04/
├── frontend/
│   ├── src/              # Existing Next.js source (unchanged)
│   ├── Dockerfile        # NEW: Multi-stage frontend image
│   ├── .dockerignore     # NEW: Exclude node_modules, .next
│   ├── next.config.ts    # MODIFIED: Add output: "standalone"
│   └── package.json      # Existing (unchanged)
├── backend/
│   ├── src/              # Existing FastAPI source (unchanged except health endpoint)
│   ├── Dockerfile        # NEW: Multi-stage backend image
│   ├── .dockerignore     # NEW: Exclude venv, __pycache__
│   └── pyproject.toml    # Existing (unchanged)
├── helm/                 # NEW: Helm charts directory
│   ├── todo-frontend/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   ├── .helmignore
│   │   └── templates/
│   │       ├── _helpers.tpl
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── ingress.yaml
│   │       └── NOTES.txt
│   ├── todo-backend/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   ├── .helmignore
│   │   └── templates/
│   │       ├── _helpers.tpl
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── configmap.yaml
│   │       ├── secret.yaml
│   │       └── NOTES.txt
│   └── todo-database/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── .helmignore
│       └── templates/
│           ├── _helpers.tpl
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── pvc.yaml
│           ├── secret.yaml
│           └── NOTES.txt
├── .specify/             # Existing SpecKit Plus
├── specs/                # Existing feature specs
├── history/              # Existing PHRs and ADRs
└── CLAUDE.md             # Existing agent instructions
```

**Structure Decision**: Web application structure (Option 2) extended with `helm/` directory at root. Each service gets its own Helm chart subdirectory. Dockerfiles placed alongside their respective service source code (`frontend/Dockerfile`, `backend/Dockerfile`). No `k8s/` directory needed since all manifests are managed via Helm templates.

## Complexity Tracking

> No constitution violations detected. No justifications needed.

---

## Phase 0: Research & Decisions

*Full details in [research.md](./research.md)*

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Next.js Docker strategy | Standalone output mode | Produces self-contained build; no need for full `node_modules` in production image |
| Frontend serving | Node.js standalone server (built-in) | Simpler than nginx for Next.js; handles SSR, API routes, and static assets natively |
| Backend entry point | `uvicorn src.main:app` | Already used in development; production-ready ASGI server |
| Database in K8s vs external | In-cluster PostgreSQL | Self-contained deployment for hackathon; no external dependency needed |
| Image pull policy | `Never` (Minikube) | Images loaded via `minikube image load`; prevents attempted pulls from Docker Hub |
| Ingress class | nginx (Minikube addon) | Built into Minikube; zero additional setup |
| Namespace | `default` | Single-developer local cluster; namespace isolation not needed |
| Secrets approach | Helm-managed K8s Secrets (base64) | Simple for local dev; no external secret manager needed |
| Health check: frontend | HTTP GET `/` on port 3000 | Next.js serves the landing page; 200 response indicates healthy |
| Health check: backend | HTTP GET `/health` on port 8000 | Dedicated lightweight endpoint; needs to be added if missing |
| PVC storage class | `standard` (Minikube default) | Minikube provisions PVs automatically with `standard` storageClass |
| `NEXT_PUBLIC_API_URL` | Build-time env via Docker ARG | Next.js inlines `NEXT_PUBLIC_*` at build time; must be set during `docker build` |

---

## Phase 1: Design & Contracts

### Infrastructure Entity Model

*Full details in [data-model.md](./data-model.md)*

**Entities**: Docker Images (2 custom + 1 official), Helm Charts (3), Helm Releases (3), Kubernetes Deployments (3), Services (3), Ingress (1), PVC (1), Secrets (2), ConfigMap (1)

**Dependency Graph**:
```
PVC ← Database Deployment ← Database Service
                                    ↑
                          Backend Deployment ← Backend Service
                          (needs DB_URL)            ↑
                                          Frontend Deployment ← Frontend Service ← Ingress
                                          (needs API_URL)
```

### Helm Values Contracts

*Full contracts in [contracts/](./contracts/)*

Each service's `values.yaml` defines the complete parameterization surface. Key patterns:
- `image.repository` + `image.tag` for image references
- `replicaCount` for horizontal scaling
- `resources.requests/limits` for resource budgeting
- `service.type` + `service.port` for networking
- `env` sections for environment variable injection
- Service-specific: `ingress.*` (frontend), `persistence.*` (database)

### Quickstart Guide

*Full guide in [quickstart.md](./quickstart.md)*

10-step developer workflow from `minikube start` to `todo.local` in browser.

---

## Execution Plan: Agentic DevOps Workflow

### Step 0: Environment Preparation

| Attribute | Detail |
|-----------|--------|
| **Objective** | Install and verify all required tools on the developer machine |
| **Responsible Agent** | Claude Code (guidance) + Developer (manual installs) |
| **Tools Required** | Windows package manager (winget/choco) or manual installers |
| **Expected Output** | All tools installed and verified: Docker Desktop, Minikube, kubectl, Helm, kubectl-ai, kagent |
| **Dependencies** | None (first step) |

**Sub-steps**:
1. Install Docker Desktop and verify with `docker --version`
2. Enable Docker Gordon (Docker Desktop Settings → Features → Docker AI)
3. Install Minikube and verify with `minikube version`
4. Install kubectl and verify with `kubectl version --client`
5. Install Helm 3 and verify with `helm version`
6. Install kubectl-ai (optional) and verify
7. Install kagent (optional) and verify

---

### Step 1: Containerization - Frontend Dockerfile

| Attribute | Detail |
|-----------|--------|
| **Objective** | Create a production-grade Docker image for the Next.js frontend |
| **Responsible Agent** | Docker Gordon (primary) / Claude Code (fallback) |
| **Tools Required** | Docker Desktop, Docker Gordon |
| **Expected Output** | `frontend/Dockerfile`, `frontend/.dockerignore`, modified `frontend/next.config.ts` |
| **Dependencies** | Step 0 (Docker installed) |

**Technical Details**:
- Modify `next.config.ts` to add `output: "standalone"` for self-contained builds
- Multi-stage build: `node:20-alpine` base for both build and production stages
- Stage 1 (deps): `npm ci` to install dependencies
- Stage 2 (build): `npm run build` to produce standalone output
- Stage 3 (production): Copy `.next/standalone` + `.next/static` + `public/`, run as non-root user `nextjs`
- Build ARG: `NEXT_PUBLIC_API_URL` injected at build time
- Exposed port: 3000
- CMD: `node server.js` (from standalone output)

**AI Agent Command (Gordon)**:
```
docker ai "Generate a production Dockerfile for a Next.js 16 frontend app using node:20-alpine with multi-stage build, standalone output, non-root user, and build-time API_URL argument"
```

---

### Step 2: Containerization - Backend Dockerfile

| Attribute | Detail |
|-----------|--------|
| **Objective** | Create a production-grade Docker image for the FastAPI backend |
| **Responsible Agent** | Docker Gordon (primary) / Claude Code (fallback) |
| **Tools Required** | Docker Desktop, Docker Gordon |
| **Expected Output** | `backend/Dockerfile`, `backend/.dockerignore` |
| **Dependencies** | Step 0 (Docker installed) |

**Technical Details**:
- Multi-stage build: `python:3.12-slim` base
- Stage 1 (build): Install system deps (`libpq-dev`, `gcc`), `pip install` from `pyproject.toml`
- Stage 2 (production): Copy installed packages from build stage, copy `src/`, run as non-root user `appuser`
- Add `/health` endpoint to `src/main.py` if missing
- Exposed port: 8000
- CMD: `uvicorn src.main:app --host 0.0.0.0 --port 8000`
- Environment variables injected at runtime (not baked in)

**AI Agent Command (Gordon)**:
```
docker ai "Generate a production Dockerfile for a Python FastAPI backend using python:3.12-slim with multi-stage build, pyproject.toml dependencies, non-root user, and uvicorn entry point on port 8000"
```

---

### Step 3: Build and Verify Docker Images

| Attribute | Detail |
|-----------|--------|
| **Objective** | Build both images locally and verify they start correctly |
| **Responsible Agent** | Claude Code |
| **Tools Required** | Docker Desktop |
| **Expected Output** | `todo-frontend:1.0.0` and `todo-backend:1.0.0` images built and verified |
| **Dependencies** | Steps 1 and 2 (Dockerfiles created) |

**Verification**:
1. `docker build -t todo-frontend:1.0.0 --build-arg NEXT_PUBLIC_API_URL="" ./frontend`
2. `docker build -t todo-backend:1.0.0 ./backend`
3. `docker images | grep todo-` → verify images exist and size < 500MB
4. `docker run --rm -p 3000:3000 todo-frontend:1.0.0` → verify port 3000 responds
5. `docker run --rm -p 8000:8000 todo-backend:1.0.0` → verify `/health` returns 200

---

### Step 4: Helm Chart Generation - Database

| Attribute | Detail |
|-----------|--------|
| **Objective** | Create Helm chart for PostgreSQL database with persistent storage |
| **Responsible Agent** | Claude Code (helm-chart-generator agent) |
| **Tools Required** | Helm 3 |
| **Expected Output** | `helm/todo-database/` chart with Chart.yaml, values.yaml, and templates |
| **Dependencies** | None (independent of Docker images) |

**Key Templates**:
- `deployment.yaml`: Single replica, `postgres:15-alpine`, env from Secret, volume mount for `/var/lib/postgresql/data`
- `service.yaml`: ClusterIP on port 5432
- `pvc.yaml`: 1Gi PersistentVolumeClaim with `standard` storageClass
- `secret.yaml`: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` as base64 values
- `NOTES.txt`: Connection info and verification commands

**Values Contract**: See `contracts/database-values.yaml`

---

### Step 5: Helm Chart Generation - Backend

| Attribute | Detail |
|-----------|--------|
| **Objective** | Create Helm chart for FastAPI backend with ConfigMap and Secret |
| **Responsible Agent** | Claude Code (helm-chart-generator agent) |
| **Tools Required** | Helm 3 |
| **Expected Output** | `helm/todo-backend/` chart with Chart.yaml, values.yaml, and templates |
| **Dependencies** | Step 4 design (needs database service name for DB_URL) |

**Key Templates**:
- `deployment.yaml`: 2 replicas, `todo-backend:latest`, env from ConfigMap + Secret, liveness/readiness probes on `/health:8000`
- `service.yaml`: ClusterIP on port 8000
- `configmap.yaml`: `ALLOWED_ORIGINS`, non-sensitive config
- `secret.yaml`: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `OPENAI_API_KEY`
- `NOTES.txt`: Service URL and verification commands

**Values Contract**: See `contracts/backend-values.yaml`

---

### Step 6: Helm Chart Generation - Frontend

| Attribute | Detail |
|-----------|--------|
| **Objective** | Create Helm chart for Next.js frontend with Ingress |
| **Responsible Agent** | Claude Code (helm-chart-generator agent) |
| **Tools Required** | Helm 3 |
| **Expected Output** | `helm/todo-frontend/` chart with Chart.yaml, values.yaml, and templates |
| **Dependencies** | Step 5 design (needs backend service name for API URL) |

**Key Templates**:
- `deployment.yaml`: 2 replicas, `todo-frontend:latest`, liveness/readiness probes on `/:3000`
- `service.yaml`: ClusterIP on port 3000
- `ingress.yaml`: NGINX ingress class, host `todo.local`, path `/` → service port 3000
- `NOTES.txt`: Access URL and hosts file instructions

**Values Contract**: See `contracts/frontend-values.yaml`

---

### Step 7: Helm Lint Validation

| Attribute | Detail |
|-----------|--------|
| **Objective** | Validate all Helm charts pass linting |
| **Responsible Agent** | Claude Code |
| **Tools Required** | Helm 3 |
| **Expected Output** | All 3 charts pass `helm lint` with no errors |
| **Dependencies** | Steps 4, 5, 6 (charts created) |

**Commands**:
```
helm lint ./helm/todo-database
helm lint ./helm/todo-backend
helm lint ./helm/todo-frontend
```

---

### Step 8: Kubernetes Deployment - Cluster Setup

| Attribute | Detail |
|-----------|--------|
| **Objective** | Start Minikube and prepare the cluster for deployment |
| **Responsible Agent** | Claude Code / kubectl-ai |
| **Tools Required** | Minikube, kubectl |
| **Expected Output** | Running Minikube cluster with ingress addon enabled |
| **Dependencies** | Step 0 (tools installed) |

**Commands**:
```
minikube start --driver=docker --memory=4096 --cpus=2
minikube addons enable ingress
kubectl get nodes  # verify Ready
```

---

### Step 9: Kubernetes Deployment - Load Images

| Attribute | Detail |
|-----------|--------|
| **Objective** | Load locally-built Docker images into Minikube's image store |
| **Responsible Agent** | Claude Code |
| **Tools Required** | Minikube, Docker |
| **Expected Output** | Both custom images available inside Minikube |
| **Dependencies** | Steps 3 (images built) and 8 (cluster running) |

**Commands**:
```
minikube image load todo-frontend:1.0.0
minikube image load todo-backend:1.0.0
minikube image list | grep todo-  # verify loaded
```

---

### Step 10: Kubernetes Deployment - Deploy Stack

| Attribute | Detail |
|-----------|--------|
| **Objective** | Deploy all three services to Minikube using Helm |
| **Responsible Agent** | kubectl-ai (primary) / Claude Code (fallback) |
| **Tools Required** | Helm 3, kubectl |
| **Expected Output** | 3 Helm releases deployed; 5 pods Running (2+2+1) |
| **Dependencies** | Steps 7 (charts validated) and 9 (images loaded) |

**Deploy Order** (respects dependency chain):
1. `helm install todo-database ./helm/todo-database` → wait for Ready
2. `helm install todo-backend ./helm/todo-backend` → wait for Ready
3. `helm install todo-frontend ./helm/todo-frontend` → wait for Ready

**kubectl-ai Commands**:
```
"deploy todo database with 1 replica using postgres:15-alpine"
"deploy todo backend with 2 replicas"
"deploy todo frontend with 2 replicas and ingress on todo.local"
```

**Verification**:
```
kubectl get pods          # all Running
kubectl get svc           # all services listed
kubectl get ingress       # todo.local rule present
helm list                 # all 3 releases deployed
```

---

### Step 11: DNS Configuration and End-to-End Verification

| Attribute | Detail |
|-----------|--------|
| **Objective** | Configure local DNS and verify the application works end-to-end |
| **Responsible Agent** | Claude Code (guidance) + Developer (hosts file edit) |
| **Tools Required** | Text editor (admin), browser |
| **Expected Output** | `todo.local` accessible in browser; full CRUD + AI chat functional |
| **Dependencies** | Step 10 (stack deployed) |

**Sub-steps**:
1. Get Minikube IP: `minikube ip`
2. Edit `C:\Windows\System32\drivers\etc\hosts` (as admin): add `<minikube-ip> todo.local`
3. Open browser → `http://todo.local`
4. Verify: signup → signin → create todo → list todos → AI chat (if OpenAI key configured)

---

### Step 12: AI-Assisted Operations Demo

| Attribute | Detail |
|-----------|--------|
| **Objective** | Demonstrate AI-assisted DevOps using kubectl-ai and kagent |
| **Responsible Agent** | kubectl-ai, kagent |
| **Tools Required** | kubectl-ai, kagent, running cluster |
| **Expected Output** | Successful execution of natural language DevOps commands |
| **Dependencies** | Step 10 (stack deployed) |

**kubectl-ai Demos**:
- `"scale backend to 3 replicas"` → verify 3 backend pods
- `"check why pods are failing"` (intentionally break a pod first)
- `"show status of all todo services"`

**kagent Demos**:
- `"analyze cluster health"` → health summary
- `"optimize resource allocation"` → recommendations
- `"recommend scaling strategies"` → scaling advice

---

### Step 13: Scaling, Debugging, and Optimization

| Attribute | Detail |
|-----------|--------|
| **Objective** | Verify scaling, pod recovery, and resource management |
| **Responsible Agent** | kagent (analysis) / Claude Code (operations) |
| **Tools Required** | kubectl, Helm, kagent |
| **Expected Output** | Validated scaling, recovery, and persistence behaviors |
| **Dependencies** | Step 10 (stack deployed) |

**Scaling Tests**:
- `helm upgrade todo-frontend ./helm/todo-frontend --set replicaCount=3` → verify 3 pods
- `helm upgrade todo-backend ./helm/todo-backend --set resources.limits.memory=1Gi` → verify new limits

**Recovery Tests**:
- `kubectl delete pod <backend-pod>` → verify auto-restart within 30s
- `kubectl delete pod <database-pod>` → verify data persists after restart

**Optimization**:
- `kubectl top pods` (if metrics-server enabled) → resource utilization
- kagent: `"analyze cluster health"` → actionable recommendations

---

## Post-Design Constitution Re-check

| # | Principle/Rule | Status | Notes |
|---|---------------|--------|-------|
| I | Spec-Driven Development | PASS | Spec → Plan → Tasks flow maintained |
| II | Architecture First | PASS | Container, Helm, and K8s architecture fully designed |
| III | Reusability | PASS | Charts parameterized; shared `_helpers.tpl` pattern |
| V | Phase Isolation | PASS | No AWS/GCP/CI-CD/Prometheus/Istio/Kafka used |
| VI | Infrastructure as Code | PASS | All deployments via Helm; Dockerfiles in VCS |
| R8 | Container Standards | PASS | Multi-stage, Alpine/slim, non-root, no secrets in image |
| R9 | Helm Discipline | PASS | 3 charts, all parameterized, lint required |

**Re-check Result**: ALL PASS

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| `next.config.ts` change breaks existing app | Blocked build | Test `npm run build` locally before Docker build; `standalone` output is additive |
| Minikube resource exhaustion on Windows | Pods evicted | Allocate 4GB RAM + 2 CPUs to Minikube; resource limits on all pods |
| Docker Gordon unavailable | Cannot generate Dockerfiles via AI | Claude Code generates Dockerfiles directly (documented fallback) |
| `NEXT_PUBLIC_API_URL` wrong at build time | Frontend cannot reach backend | Document exact value (`http://todo-backend:8000`); rebuilds required if changed |
| Database PVC loss on `minikube delete` | Data wiped | Document that `minikube delete` destroys PVCs; use `minikube stop` for pause |

---

## Follow-ups

- `/sp.tasks` to generate the task breakdown from this plan
- Consider ADR for "Standalone Next.js output for Docker" decision if team needs traceability
- Consider ADR for "In-cluster PostgreSQL vs external DB" decision
