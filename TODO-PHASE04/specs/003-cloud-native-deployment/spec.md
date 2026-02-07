# Feature Specification: Cloud Native Deployment

**Feature Branch**: `003-cloud-native-deployment`
**Created**: 2026-02-06
**Status**: Draft
**Input**: User description: "Deploy Phase III Todo Chatbot on local Kubernetes cluster using Minikube and Helm charts with AI-assisted DevOps"

---

## Project Overview

Phase IV containerizes and orchestrates the existing Todo AI Chatbot application (Phase III) on a local Kubernetes cluster. The application's functionality remains unchanged; this phase focuses exclusively on packaging, deploying, and managing the three-tier architecture (frontend, backend, database) as containerized workloads.

The deployment uses Docker for containerization, Minikube for local Kubernetes orchestration, and Helm charts for templated, repeatable deployments. AI-assisted DevOps tools (Docker Gordon, kubectl-ai, kagent) augment the workflow for Dockerfile generation, deployment operations, and cluster health analysis.

**Assumptions**:
<!-- The application (frontend + backend + database) from Phase III is fully functional and will not be modified in this phase -->
<!-- Minikube runs on Windows with Docker Desktop as the driver -->
<!-- No remote container registry is required; images are loaded directly into Minikube -->
<!-- No CI/CD pipeline is in scope; all builds and deployments are manual or AI-assisted -->

---

## Objectives

1. Containerize all three application tiers (frontend, backend, database) as production-grade Docker images
2. Create Helm charts for repeatable, parameterized Kubernetes deployments of each service
3. Deploy the full application stack on a local Minikube cluster with inter-service communication
4. Expose the frontend via ingress at `todo.local` for external browser access
5. Demonstrate AI-assisted DevOps using Docker Gordon, kubectl-ai, and kagent
6. Ensure all deployment artifacts are version-controlled, declarative, and reproducible

---

## Technology Stack

### Container Layer
| Component | Technology | Version |
|-----------|-----------|---------|
| Container Runtime | Docker Desktop | Latest stable |
| Frontend Base Image | node:20-alpine | 20.x |
| Backend Base Image | python:3.12-slim | 3.12.x |
| Database Image | postgres:15-alpine | 15.x |
| AI Image Generation | Docker Gordon | Latest |

### Orchestration Layer
| Component | Technology | Version |
|-----------|-----------|---------|
| Local Cluster | Minikube | Latest stable |
| Package Manager | Helm | 3.x |
| CLI | kubectl | Latest stable |
| AI Deployment | kubectl-ai | Latest |
| AI Cluster Analysis | kagent | Latest |
| Ingress Controller | NGINX Ingress | Minikube addon |

### Application Layer (Unchanged from Phase III)
| Component | Technology |
|-----------|-----------|
| Frontend | Next.js 16+ (TypeScript, Tailwind CSS v4) |
| Backend | FastAPI (Python 3.12+) |
| Database | PostgreSQL (via Neon in app, local PG in cluster) |
| AI Agent | OpenAI Agents SDK + MCP |
| Auth | Better Auth (JWT) |

---

## User Scenarios & Testing

### User Story 1 - Container Image Build (Priority: P1)

As a developer, I want to build Docker images for the frontend and backend services so that the application can run in isolated, reproducible containers.

**Why this priority**: Containerization is the foundational prerequisite for all Kubernetes deployment work. Without working images, no further deployment is possible.

**Independent Test**: Build both images locally and run them with `docker run` to verify the application starts and responds to health check requests.

**Acceptance Scenarios**:

1. **Given** the frontend source code exists in `frontend/`, **When** I run `docker build -t todo-frontend:latest ./frontend`, **Then** a Docker image is produced that is under 500MB in size
2. **Given** the backend source code exists in `backend/`, **When** I run `docker build -t todo-backend:1.0.0 ./backend`, **Then** a Docker image is produced that is under 500MB in size
3. **Given** a built frontend image, **When** I run the container and access port 3000, **Then** the application serves the landing page
4. **Given** a built backend image, **When** I run the container and access the `/health` endpoint on port 8000, **Then** a 200 OK response is returned
5. **Given** any built image, **When** I inspect the container process, **Then** it runs as a non-root user

---

### User Story 2 - Helm Chart Deployment (Priority: P1)

As a developer, I want to deploy the full application stack to Minikube using Helm charts so that deployments are repeatable, parameterized, and version-controlled.

**Why this priority**: Helm charts are the primary delivery mechanism. Without them, there is no structured deployment path to Kubernetes.

**Independent Test**: Run `helm install` for each service chart and verify pods reach Running state with `kubectl get pods`.

**Acceptance Scenarios**:

1. **Given** a running Minikube cluster with images loaded, **When** I run `helm install todo-database ./helm/todo-database`, **Then** a PostgreSQL pod starts and becomes Ready within 60 seconds
2. **Given** the database is running, **When** I run `helm install todo-backend ./helm/todo-backend`, **Then** backend pods (2 replicas) start and pass readiness probes within 90 seconds
3. **Given** the backend is running, **When** I run `helm install todo-frontend ./helm/todo-frontend`, **Then** frontend pods (2 replicas) start and pass readiness probes within 90 seconds
4. **Given** all three Helm releases are installed, **When** I run `helm list`, **Then** all three releases show status `deployed`
5. **Given** a deployed chart, **When** I run `helm lint ./helm/todo-<service>`, **Then** no errors are reported

---

### User Story 3 - External Access via Ingress (Priority: P1)

As a user, I want to access the Todo application through my browser at `todo.local` so that the Kubernetes-deployed application is usable like any web application.

**Why this priority**: External access is the user-facing outcome that validates the entire deployment pipeline end-to-end.

**Independent Test**: Open a browser, navigate to `http://todo.local`, and verify the Todo application loads with login/signup capability.

**Acceptance Scenarios**:

1. **Given** the NGINX ingress addon is enabled in Minikube, **When** I navigate to `http://todo.local` in a browser, **Then** the Todo frontend loads
2. **Given** the frontend is accessible, **When** I sign up and create a todo item, **Then** the item persists and appears in the todo list
3. **Given** a frontend request to the backend, **When** the frontend calls an API endpoint, **Then** the request routes through Kubernetes service DNS to the backend pods
4. **Given** the Minikube IP, **When** I add `<minikube-ip> todo.local` to my hosts file, **Then** `todo.local` resolves correctly in the browser

---

### User Story 4 - Parameterized Configuration (Priority: P2)

As a developer, I want to customize deployment parameters (replicas, resource limits, ports, environment variables) through Helm values files so that I can tune the deployment without modifying templates.

**Why this priority**: Parameterization enables environment-specific deployments and demonstrates Helm's value proposition, but the application works with defaults.

**Independent Test**: Override `replicaCount` in a `helm install --set` command and verify the desired number of pods are created.

**Acceptance Scenarios**:

1. **Given** the frontend Helm chart, **When** I deploy with `--set replicaCount=3`, **Then** 3 frontend pods are created
2. **Given** the backend Helm chart, **When** I deploy with custom resource limits (`--set resources.limits.memory=1Gi`), **Then** the pod spec reflects the overridden memory limit
3. **Given** any Helm chart, **When** I provide a custom `values.yaml` file, **Then** all values from the file override defaults without template errors
4. **Given** the database Helm chart, **When** I override environment variables for `POSTGRES_USER` and `POSTGRES_DB`, **Then** the database initializes with the custom credentials

---

### User Story 5 - AI-Assisted DevOps Operations (Priority: P2)

As a developer, I want to use AI-powered tools (Docker Gordon, kubectl-ai, kagent) to assist with Dockerfile generation, Kubernetes operations, and cluster health analysis so that DevOps tasks are more accessible and efficient.

**Why this priority**: AI integration demonstrates the project's AI-assisted DevOps capability and is a hackathon differentiator, but the deployment functions without it.

**Independent Test**: Issue natural language commands through each AI tool and verify the correct Kubernetes/Docker operations are performed.

**Acceptance Scenarios**:

1. **Given** Docker Gordon is available, **When** I ask it to "Generate a Dockerfile for the frontend", **Then** it produces a valid multi-stage Dockerfile suitable for the Next.js application
2. **Given** kubectl-ai is installed, **When** I issue "deploy todo frontend with 2 replicas", **Then** the correct Kubernetes deployment is created or updated
3. **Given** kubectl-ai is installed, **When** I issue "scale backend to 3 replicas", **Then** the backend deployment scales to 3 pods
4. **Given** kagent is available, **When** I ask to "analyze cluster health", **Then** it provides a summary of pod states, resource utilization, and any issues detected

---

### User Story 6 - Cluster Health and Pod Lifecycle (Priority: P3)

As a developer, I want to monitor pod health, view logs, and verify that containers recover from failures so that I can trust the deployment's operational readiness.

**Why this priority**: Operational readiness validates the deployment's resilience but is secondary to getting the deployment running.

**Independent Test**: Kill a pod and verify Kubernetes restarts it automatically; check logs for meaningful output.

**Acceptance Scenarios**:

1. **Given** a running backend pod, **When** I delete the pod with `kubectl delete pod`, **Then** Kubernetes automatically creates a replacement pod within 30 seconds
2. **Given** all pods are running, **When** I run `kubectl logs <pod-name>`, **Then** application logs are visible and contain expected startup messages
3. **Given** a pod with a health check endpoint, **When** the health check fails, **Then** Kubernetes marks the pod as NotReady and stops routing traffic to it
4. **Given** the cluster is running, **When** I run `kubectl get pods`, **Then** all pods show status Running with READY counts matching expected container counts

---

### Edge Cases

- What happens when the database pod is not ready before backend pods start? The backend MUST handle database connection retries gracefully with exponential backoff. An initContainer in the backend deployment SHOULD wait for database readiness before starting the application container.
- What happens when the database is freshly initialized with no schema? The backend MUST either run migrations on startup (Alembic) or an init container MUST apply the schema before the backend deployment begins.
- What happens when Minikube runs out of resources? Resource limits on pods MUST prevent any single service from consuming all cluster resources.
- What happens when a Docker image fails to load into Minikube? The `minikube image load` command MUST be verified before Helm install; `imagePullPolicy: Never` ensures Kubernetes does not attempt to pull from a remote registry.
- What happens when the ingress controller is not enabled? Deployment MUST document the prerequisite step of enabling the ingress addon and fail with a clear message if ingress is not available.
- What happens when `todo.local` is not in the hosts file? Documentation MUST include hosts file setup instructions for the developer's operating system.
- What happens when a Helm upgrade conflicts with existing state? Helm rollback MUST be documented as the recovery procedure.

---

## Requirements

### Functional Requirements

#### Container Images

- **FR-001**: System MUST produce a frontend Docker image from `frontend/Dockerfile` that serves the Next.js application on port 3000
- **FR-002**: System MUST produce a backend Docker image from `backend/Dockerfile` that runs the FastAPI application on port 8000
- **FR-003**: System MUST use the official `postgres:15-alpine` image for the database tier without modification
- **FR-004**: Frontend and backend images MUST use multi-stage builds to exclude build tools and development dependencies from the final image
- **FR-005**: All custom images MUST run application processes as a non-root user
- **FR-006**: All custom images MUST expose a health check endpoint (frontend: `/`, backend: `/health`)

#### Helm Charts

- **FR-007**: System MUST provide a Helm chart for the frontend service at `helm/todo-frontend/` with deployment, service, and ingress templates
- **FR-008**: System MUST provide a Helm chart for the backend service at `helm/todo-backend/` with deployment and service templates
- **FR-009**: System MUST provide a Helm chart for the database service at `helm/todo-database/` with deployment, service, and persistent volume claim templates
- **FR-010**: All Helm charts MUST define configurable values for: image repository, image tag, replica count, service type, service port, resource requests, and resource limits
- **FR-011**: The frontend Helm chart MUST include an ingress template with configurable host (default: `todo.local`) and enable/disable toggle
- **FR-012**: All Helm charts MUST include a `NOTES.txt` template that displays post-install instructions to the user
- **FR-013**: All Helm charts MUST pass `helm lint` validation without errors

#### Kubernetes Deployments

- **FR-014**: Frontend deployment MUST create 2 replicas by default
- **FR-015**: Backend deployment MUST create 2 replicas by default
- **FR-016**: Database deployment MUST create 1 replica (single instance)
- **FR-017**: All deployments MUST define liveness and readiness probes
- **FR-018**: All deployments MUST define CPU and memory resource requests and limits
- **FR-019**: Database deployment MUST use a PersistentVolumeClaim to persist data across pod restarts

#### Networking and Ingress

- **FR-020**: Frontend service MUST be accessible externally via NGINX ingress at hostname `todo.local`
- **FR-021**: Backend service MUST be accessible to frontend pods via Kubernetes ClusterIP service DNS
- **FR-022**: Database service MUST be accessible to backend pods via Kubernetes ClusterIP service DNS
- **FR-023**: All inter-service communication MUST use Kubernetes service names (not pod IPs)

#### Environment and Secrets

- **FR-024**: Database credentials (user, password, database name) MUST be managed via Kubernetes Secrets, not hardcoded in manifests
- **FR-025**: Backend environment variables (database URL, JWT secrets, API keys) MUST be injected via ConfigMaps or Secrets
- **FR-026**: Frontend environment variables (API URL pointing to backend service) MUST be configurable at build time or runtime

#### AI-Assisted Operations

- **FR-027**: Docker Gordon MUST be usable to generate or optimize Dockerfiles for frontend and backend services
- **FR-028**: kubectl-ai MUST be usable to perform deployment, scaling, and troubleshooting operations via natural language commands
- **FR-029**: kagent MUST be usable to analyze cluster health, resource utilization, and provide optimization recommendations

### Key Entities

- **Docker Image**: A container image built from a Dockerfile, identified by name and tag (e.g., `todo-frontend:latest`). Contains the application runtime and dependencies.
- **Helm Chart**: A collection of Kubernetes manifest templates and a values file. Identified by chart name and version. Produces a Helm release when installed.
- **Helm Release**: A running instance of a Helm chart in the cluster. Has a name, namespace, revision number, and status.
- **Kubernetes Deployment**: A controller that manages a set of replica pods. Defines the desired state including image, replicas, resources, and probes.
- **Kubernetes Service**: A stable network endpoint that routes traffic to pods via label selectors. Types: ClusterIP (internal) or NodePort/Ingress (external).
- **Kubernetes Ingress**: A routing rule that maps external hostnames to internal services. Managed by the NGINX ingress controller.
- **PersistentVolumeClaim**: A storage request that binds to a PersistentVolume. Used by the database to retain data across pod restarts.
- **Kubernetes Secret**: An object that stores sensitive data (passwords, tokens, keys) and makes it available to pods as environment variables or mounted files.
- **ConfigMap**: An object that stores non-sensitive configuration data and makes it available to pods as environment variables or mounted files.

---

## Component Specifications

### Frontend Container

| Attribute | Value |
|-----------|-------|
| Image Name | `todo-frontend` |
| Base Image | `node:20-alpine` |
| Build Strategy | Multi-stage (install → build → serve) |
| Exposed Port | 3000 |
| Health Endpoint | `/` (HTTP GET) |
| Default Replicas | 2 |
| User | Non-root (e.g., `node` or custom) |

**Build Stages**:
1. **Dependencies**: Install npm packages with `npm ci`
2. **Build**: Build the Next.js production bundle with `npm run build`
3. **Production**: Copy the standalone build output; run with minimal Node.js image

**Environment Variables** (injected at build or runtime):
- `NEXT_PUBLIC_API_URL`: URL of the backend service. Set to empty string `""` for production since ingress path-based routing handles `/api/*` and `/auth/*` on the same origin (`todo.local`)

### Backend Container

| Attribute | Value |
|-----------|-------|
| Image Name | `todo-backend` |
| Base Image | `python:3.12-slim` |
| Build Strategy | Multi-stage (install deps → copy source) |
| Exposed Port | 8000 |
| Health Endpoint | `/health` (HTTP GET) |
| Default Replicas | 2 |
| User | Non-root (e.g., `appuser`) |

**Build Stages**:
1. **Dependencies**: Install system packages and Python dependencies via `pip install`
2. **Production**: Copy installed packages and source code; run with `uvicorn`

**Environment Variables** (injected via ConfigMap/Secret):
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret
- `OPENAI_API_KEY`: OpenAI API key for the AI agent
- `ALLOWED_ORIGINS`: CORS origins (frontend service URL)

**Local Development Defaults**:
- `DATABASE_URL`: `postgresql://todo_user:todo_pass@todo-database:5432/todo_db`
- `BETTER_AUTH_SECRET`: Any random 32+ character string (e.g., `change-me-in-production-32chars!`)
- `OPENAI_API_KEY`: User must provide their own key; set to `sk-placeholder` if AI chat is not needed
- `ALLOWED_ORIGINS`: `http://todo.local` (matches ingress host; with path-based routing, CORS may not be triggered for same-origin requests)

### Database Container

| Attribute | Value |
|-----------|-------|
| Image Name | `postgres:15-alpine` (official) |
| Custom Dockerfile | None (use official image directly) |
| Exposed Port | 5432 |
| Health Check | TCP socket on port 5432 |
| Default Replicas | 1 |
| Storage | PersistentVolumeClaim |

**Environment Variables** (injected via Secret):
- `POSTGRES_USER`: Database username (default: `todo_user`)
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name (default: `todo_db`)

---

## Helm Chart Specifications

### Common Chart Structure

Each Helm chart follows this directory layout:

```
helm/todo-<service>/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── NOTES.txt
│   └── [additional templates per service]
└── .helmignore
```

### Configurable Parameters (values.yaml)

#### All Services

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | Docker image name | `todo-<service>` |
| `image.tag` | Docker image tag | `1.0.0` (custom images), `15-alpine` (postgres) |
| `image.pullPolicy` | Image pull policy | `Never` (custom images loaded via `minikube image load`), `IfNotPresent` (official images like postgres) |
| `replicaCount` | Number of pod replicas | Service-specific |
| `service.type` | Kubernetes Service type | `ClusterIP` |
| `service.port` | Service port | Service-specific |
| `resources.requests.cpu` | CPU request | `100m` |
| `resources.requests.memory` | Memory request | Service-specific |
| `resources.limits.cpu` | CPU limit | Service-specific |
| `resources.limits.memory` | Memory limit | Service-specific |

#### Frontend-Specific

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress resource | `true` |
| `ingress.host` | Ingress hostname | `todo.local` |
| `ingress.className` | Ingress class | `nginx` |

#### Database-Specific

| Parameter | Description | Default |
|-----------|-------------|---------|
| `persistence.enabled` | Enable persistent storage | `true` |
| `persistence.size` | PVC storage size | `1Gi` |
| `persistence.storageClass` | Storage class | `standard` |

### Resource Allocation Defaults

| Service | Replicas | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|----------|-------------|-----------|----------------|--------------|
| Frontend | 2 | 100m | 250m | 128Mi | 256Mi |
| Backend | 2 | 100m | 500m | 128Mi | 512Mi |
| Database | 1 | 100m | 500m | 256Mi | 512Mi |

---

## Networking, Ingress, and Service Specifications

### Service Topology

```
[Browser] → todo.local → [NGINX Ingress Controller]
                              ↓
                     [todo-frontend Service (ClusterIP:3000)]
                              ↓
                     [todo-frontend Pods (2 replicas)]
                              ↓ (API calls)
                     [todo-backend Service (ClusterIP:8000)]
                              ↓
                     [todo-backend Pods (2 replicas)]
                              ↓ (DB queries)
                     [todo-database Service (ClusterIP:5432)]
                              ↓
                     [todo-database Pod (1 replica)]
                              ↓
                     [PersistentVolume]
```

### DNS Resolution (within cluster)

| Source | Target | DNS Name |
|--------|--------|----------|
| Frontend pods | Backend service | `todo-backend.<namespace>.svc.cluster.local:8000` |
| Backend pods | Database service | `todo-database.<namespace>.svc.cluster.local:5432` |
| External (browser) | Frontend ingress | `todo.local` (via hosts file → Minikube IP) |

### Ingress Configuration

- **Controller**: NGINX Ingress (Minikube addon: `minikube addons enable ingress`)
- **Host**: `todo.local`
- **Path-Based Routing**:
  - `/` → `todo-frontend` service on port 3000 (default backend)
  - `/api` → `todo-backend` service on port 8000 (API endpoints)
  - `/auth` → `todo-backend` service on port 8000 (authentication endpoints)
- **TLS**: Not required for local development
- **Hosts file entry**: `<minikube-ip> todo.local` must be added manually
- **Rationale**: Path-based routing eliminates CORS issues. The browser calls `http://todo.local/api/*` which the ingress routes to the backend, allowing the frontend to use relative URLs.

---

## AI-Assisted Operations Specifications

### Docker Gordon (AI Image Generation)

| Capability | Input | Expected Output |
|-----------|-------|-----------------|
| Generate frontend Dockerfile | `docker ai "Generate Dockerfile for React/Next.js frontend"` | Multi-stage Dockerfile with node:20-alpine |
| Generate backend Dockerfile | `docker ai "Generate Dockerfile for Python FastAPI backend"` | Multi-stage Dockerfile with python:3.12-slim |
| Optimize image | `docker ai "Analyze and optimize this Dockerfile"` | Suggestions for size reduction and security |

**Assumption**: Docker Gordon is an optional enhancement. If unavailable, Dockerfiles are created manually through Claude Code.

### kubectl-ai (AI Deployment)

| Capability | Natural Language Input | Expected K8s Operation |
|-----------|----------------------|----------------------|
| Deploy service | "deploy todo frontend with 2 replicas" | Creates/updates Deployment |
| Scale service | "scale backend to 3 replicas" | Patches Deployment replicas |
| Troubleshoot | "check why pods are failing" | Describes pods, shows events and logs |
| Status check | "show status of all todo services" | Lists pods, services, ingress |

**Assumption**: kubectl-ai requires a running cluster and configured `kubectl` context.

### kagent (Cluster Intelligence)

| Capability | Input | Expected Output |
|-----------|-------|-----------------|
| Health analysis | "analyze cluster health" | Pod states, node resources, events summary |
| Resource optimization | "optimize resource allocation" | Recommendations for CPU/memory adjustments |
| Scaling strategy | "recommend scaling strategies" | Auto-scaling suggestions based on utilization |

**Assumption**: kagent requires a running cluster with metrics available.

---

## Deployment Steps (Ordered)

**Prerequisites**: Docker Desktop installed and running, Minikube installed, Helm 3 installed, kubectl installed

1. **Start Minikube cluster**: Initialize local Kubernetes cluster
2. **Enable ingress addon**: Activate NGINX ingress controller in Minikube
3. **Build Docker images**: Build `todo-frontend` and `todo-backend` images locally
4. **Load images into Minikube**: Transfer locally-built images into Minikube's image store
5. **Deploy database**: Install `todo-database` Helm chart (wait for Ready)
6. **Deploy backend**: Install `todo-backend` Helm chart (wait for Ready)
7. **Deploy frontend**: Install `todo-frontend` Helm chart (wait for Ready)
8. **Configure DNS**: Add `todo.local` to system hosts file pointing to Minikube IP
9. **Verify deployment**: Access `todo.local` in browser and test application functionality
10. **Run AI-assisted operations** (optional): Demonstrate kubectl-ai and kagent commands

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: All three services (frontend, backend, database) reach Running state within 3 minutes of deployment
- **SC-002**: The application is accessible via `todo.local` in a browser and a user can sign up, sign in, and manage todo items
- **SC-003**: Frontend and backend Docker images are each under 500MB in size
- **SC-004**: Pod auto-recovery occurs within 30 seconds when a pod is manually deleted
- **SC-005**: Helm charts for all three services pass `helm lint` without errors
- **SC-006**: Deployment can be fully reproduced from scratch (clean Minikube cluster) using only the Helm charts and built images within 5 minutes
- **SC-007**: All pods run as non-root users as verified by `kubectl exec` inspection
- **SC-008**: At least one AI-assisted DevOps operation (Docker Gordon, kubectl-ai, or kagent) is successfully demonstrated
- **SC-009**: Scaling a service to a different replica count via `helm upgrade --set replicaCount=N` takes effect within 60 seconds
- **SC-010**: Database data persists across pod restarts (delete database pod, verify data remains after restart)
