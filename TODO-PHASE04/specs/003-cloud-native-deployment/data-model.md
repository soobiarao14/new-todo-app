# Infrastructure Entity Model: Cloud Native Deployment

**Feature**: 003-cloud-native-deployment
**Date**: 2026-02-06

## Overview

This document models the infrastructure entities for the Phase IV deployment. Unlike Phase II/III which model application data (Users, Tasks, Conversations), Phase IV models deployment artifacts and their relationships.

## Entities

### Docker Image

| Field | Type | Description |
|-------|------|-------------|
| name | string | Image name (e.g., `todo-frontend`) |
| tag | string | Image version tag (e.g., `latest`, `1.0.0`) |
| base_image | string | Base image used in Dockerfile |
| size | integer (MB) | Final image size |
| ports | list[integer] | Exposed container ports |
| user | string | Non-root user the process runs as |
| build_context | string | Dockerfile directory path |

**Relationships**: Referenced by Kubernetes Deployment via `image.repository:image.tag`

---

### Helm Chart

| Field | Type | Description |
|-------|------|-------------|
| name | string | Chart name (e.g., `todo-frontend`) |
| version | semver | Chart version (e.g., `0.1.0`) |
| app_version | string | Application version |
| path | string | Chart directory path (e.g., `helm/todo-frontend/`) |
| values | object | Default values.yaml content |

**Relationships**: Produces Helm Release when installed. Contains template references to Deployment, Service, Ingress, PVC, Secret, ConfigMap.

---

### Helm Release

| Field | Type | Description |
|-------|------|-------------|
| name | string | Release name (e.g., `todo-frontend`) |
| namespace | string | Kubernetes namespace (default: `default`) |
| chart | string | Source chart reference |
| revision | integer | Release revision number |
| status | enum | `deployed`, `failed`, `uninstalling`, `pending-install` |

**Relationships**: One-to-one with Helm Chart. Creates Kubernetes resources (Deployment, Service, etc.)

---

### Kubernetes Deployment

| Field | Type | Description |
|-------|------|-------------|
| name | string | Deployment name |
| namespace | string | Kubernetes namespace |
| replicas | integer | Desired pod count |
| image | string | Container image reference |
| ports | list[integer] | Container ports |
| resources | object | CPU/memory requests and limits |
| probes | object | Liveness and readiness probe configs |
| env | list[object] | Environment variables (from ConfigMap/Secret) |

**Relationships**: Manages Pods. References Docker Image. Reads from Secret and ConfigMap.

---

### Kubernetes Service

| Field | Type | Description |
|-------|------|-------------|
| name | string | Service name (DNS-resolvable) |
| namespace | string | Kubernetes namespace |
| type | enum | `ClusterIP`, `NodePort`, `LoadBalancer` |
| port | integer | Service port |
| target_port | integer | Container port |
| selector | object | Label selector matching Deployment pods |

**Relationships**: Routes traffic to Deployment pods. Referenced by Ingress (frontend) and other Deployments (backend → database).

---

### Kubernetes Ingress

| Field | Type | Description |
|-------|------|-------------|
| name | string | Ingress name |
| namespace | string | Kubernetes namespace |
| class_name | string | Ingress controller class (e.g., `nginx`) |
| host | string | External hostname (e.g., `todo.local`) |
| rules | list[object] | Path-to-service routing rules |
| tls | object | TLS configuration (disabled for local) |

**Relationships**: Routes external traffic to Services based on host and path rules.

---

### PersistentVolumeClaim

| Field | Type | Description |
|-------|------|-------------|
| name | string | PVC name |
| namespace | string | Kubernetes namespace |
| storage_class | string | Storage class (e.g., `standard`) |
| size | string | Storage size (e.g., `1Gi`) |
| access_modes | list[string] | Access modes (e.g., `ReadWriteOnce`) |

**Relationships**: Bound to PersistentVolume (auto-provisioned by Minikube). Mounted by Database Deployment.

---

### Kubernetes Secret

| Field | Type | Description |
|-------|------|-------------|
| name | string | Secret name |
| namespace | string | Kubernetes namespace |
| type | enum | `Opaque` (default) |
| data | map[string, base64] | Key-value pairs (base64 encoded) |

**Instances**:
1. `todo-database-secret`: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
2. `todo-backend-secret`: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `OPENAI_API_KEY`

**Relationships**: Referenced by Deployment env vars via `secretKeyRef`.

---

### ConfigMap

| Field | Type | Description |
|-------|------|-------------|
| name | string | ConfigMap name |
| namespace | string | Kubernetes namespace |
| data | map[string, string] | Key-value pairs (plaintext) |

**Instances**:
1. `todo-backend-config`: `ALLOWED_ORIGINS`, `ENVIRONMENT`

**Relationships**: Referenced by Deployment env vars via `configMapKeyRef`.

---

## Dependency Graph

```
[PVC: todo-database-pvc]
      ↑ (mount)
[Secret: todo-database-secret] → [Deployment: todo-database] → [Service: todo-database]
                                                                        ↑ (DB_URL)
[Secret: todo-backend-secret] → [Deployment: todo-backend] → [Service: todo-backend]
[ConfigMap: todo-backend-config] ↗                                      ↑ (API routing)
                                                              [Ingress: todo-ingress]
                                   [Deployment: todo-frontend] → [Service: todo-frontend] ↗
```

## Deployment Order

1. PVC + Database Secret + Database Deployment + Database Service
2. Backend Secret + Backend ConfigMap + Backend Deployment + Backend Service
3. Frontend Deployment + Frontend Service + Ingress
