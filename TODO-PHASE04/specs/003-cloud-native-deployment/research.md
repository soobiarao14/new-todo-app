# Research: Cloud Native Deployment

**Feature**: 003-cloud-native-deployment
**Date**: 2026-02-06
**Status**: Complete

## Research Topics

### 1. Next.js Docker Strategy

**Decision**: Use `output: "standalone"` in `next.config.ts`

**Rationale**: Next.js standalone output produces a self-contained `server.js` and only the necessary `node_modules` files needed at runtime. This reduces the Docker image size significantly compared to copying the full `node_modules/` and `.next/` directories.

**Alternatives Considered**:
- **Full `node_modules` copy**: Simpler but produces images 800MB+ in size. Rejected due to constitution Rule 8 (image size constraint).
- **nginx + static export**: Only works for static sites. Next.js uses Server-Side Rendering (SSR) and API routes, which require a Node.js runtime. Rejected.
- **Custom server (Express)**: Adds unnecessary complexity. Next.js standalone already includes a production server. Rejected.

**Impact**: Requires modifying `frontend/next.config.ts` to add `output: "standalone"`. This is a one-line additive change with no functional side effects on the existing application.

---

### 2. Backend Health Endpoint

**Decision**: Add `GET /health` endpoint to `backend/src/main.py`

**Rationale**: Kubernetes liveness and readiness probes require an HTTP endpoint that returns 200 when the application is healthy. A dedicated `/health` endpoint is lightweight and does not require authentication.

**Alternatives Considered**:
- **Use existing `/docs` endpoint**: Works but heavier (renders Swagger UI). Not semantically correct for health checks. Rejected.
- **TCP socket check**: Simpler but cannot verify application-level health (e.g., the FastAPI process is listening but the ASGI app failed to initialize). Rejected.

**Impact**: Minimal. A 3-line route addition to `main.py`. Excluded from JWT middleware. Returns `{"status": "ok"}`.

---

### 3. Database Deployment Strategy

**Decision**: In-cluster PostgreSQL via official `postgres:15-alpine` image

**Rationale**: Self-contained deployment requires no external services. The hackathon evaluation expects everything to run locally from `minikube start` to working application. Using PersistentVolumeClaim ensures data survives pod restarts.

**Alternatives Considered**:
- **External Neon PostgreSQL** (Phase II/III approach): Requires internet connectivity and API key management. Defeats the purpose of local Kubernetes deployment. Rejected for local demo.
- **SQLite in-cluster**: Simpler but cannot handle concurrent connections from 2 backend replicas safely. Rejected.
- **StatefulSet instead of Deployment**: More appropriate for production databases but adds complexity. For single-replica local development, a Deployment with PVC is sufficient. Rejected for simplicity.

**Impact**: Backend `DATABASE_URL` changes from Neon connection string to local PostgreSQL format: `postgresql://todo_user:todo_pass@todo-database:5432/todo_db`

---

### 4. Image Pull Policy

**Decision**: `imagePullPolicy: Never` for custom images, `IfNotPresent` for official images

**Rationale**: Custom images (`todo-frontend`, `todo-backend`) are loaded into Minikube via `minikube image load` and do not exist on any remote registry. Setting `Never` prevents Kubernetes from attempting to pull from Docker Hub (which would fail with ErrImagePull).

**Alternatives Considered**:
- **Local registry**: Run a Docker registry inside Minikube and push images there. Adds unnecessary complexity for local development. Rejected.
- **`eval $(minikube docker-env)`**: Build images directly in Minikube's Docker daemon. Works but requires running the build inside Minikube's context, which can be confusing. Rejected for clarity.

---

### 5. Secrets Management

**Decision**: Helm-managed Kubernetes Secrets with base64-encoded values in `values.yaml`

**Rationale**: For local development, Helm-generated Secrets are sufficient. Values are defined in `values.yaml` (which is git-tracked with defaults) and can be overridden at install time with `--set` or `-f custom-values.yaml`. This avoids the need for external secret managers.

**Alternatives Considered**:
- **External Secrets Operator**: Overkill for local development. Requires an external secret store. Rejected.
- **Sealed Secrets**: Useful for git-tracked secrets in production but adds tooling complexity. Rejected.
- **Environment variables directly in Deployment**: Violates constitution Rule 9 (values must be parameterizable in values.yaml). Rejected.

**Caution**: The `values.yaml` defaults include placeholder passwords. For any non-local use, these MUST be overridden.

---

### 6. Frontend-Backend Communication in Kubernetes

**Decision**: Frontend calls backend via Kubernetes service DNS: `http://todo-backend:8000`

**Rationale**: Within a Kubernetes cluster, services are discoverable via DNS. However, since client-side (browser) API calls cannot resolve cluster-internal DNS, ingress path-based routing is used instead. `NEXT_PUBLIC_API_URL` is set to empty string `""` at build time, and the ingress routes `/api/*` and `/auth/*` paths to the backend service.

**Challenge**: For client-side (browser) API calls, the browser cannot resolve `todo-backend` DNS. Two approaches:
1. **API route proxy**: Next.js API routes (`/api/*`) proxy requests to the backend. The server-side Next.js process resolves `todo-backend` internally.
2. **Ingress path routing**: Configure the ingress to route `/api/*` to the backend service and `/` to the frontend service.

**Decision**: Use ingress path routing as the primary approach. The ingress routes:
- `todo.local/` → `todo-frontend:3000` (frontend)
- `todo.local/api/*` → `todo-backend:8000` (backend API)
- `todo.local/auth/*` → `todo-backend:8000` (auth endpoints)

This allows the browser to call `http://todo.local/api/tasks` which the ingress routes to the backend, avoiding cross-origin issues entirely.

---

### 7. Minikube Resource Allocation

**Decision**: Start Minikube with `--memory=4096 --cpus=2`

**Rationale**: The total resource requirements across all pods:
- Frontend: 2 × (100m CPU, 128Mi memory) = 200m CPU, 256Mi memory
- Backend: 2 × (100m CPU, 128Mi memory) = 200m CPU, 256Mi memory
- Database: 1 × (100m CPU, 256Mi memory) = 100m CPU, 256Mi memory
- System pods (ingress, coredns, etc.): ~500m CPU, 512Mi memory
- Total: ~1000m CPU, ~1.3Gi memory
- Headroom for scheduling: 4096Mi memory, 2 CPUs provides comfortable margin.

---

### 8. NGINX Ingress Path Routing

**Decision**: Configure ingress with path-based routing to both frontend and backend

**Rationale**: Single `todo.local` hostname with path differentiation eliminates CORS issues and simplifies the developer experience.

**Ingress Rules**:
```
Host: todo.local
  /api/*    → todo-backend:8000
  /auth/*   → todo-backend:8000
  /health   → todo-backend:8000
  /         → todo-frontend:3000 (default backend)
```

This means `NEXT_PUBLIC_API_URL` can be set to empty string or `/` since API calls from the browser go to the same origin (`todo.local`) and are path-routed by the ingress controller.
