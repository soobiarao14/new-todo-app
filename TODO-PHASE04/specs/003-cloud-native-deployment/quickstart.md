# Quickstart: Cloud Native Deployment

**Feature**: 003-cloud-native-deployment
**Date**: 2026-02-06
**Time to complete**: ~15 minutes

## Prerequisites

Ensure the following are installed on your machine:

- [ ] Docker Desktop (with Docker Engine running)
- [ ] Minikube
- [ ] kubectl
- [ ] Helm 3
- [ ] (Optional) kubectl-ai
- [ ] (Optional) kagent

Verify installations:
```bash
docker --version
minikube version
kubectl version --client
helm version
```

## Steps

### 1. Start Minikube Cluster

```bash
minikube start --driver=docker --memory=4096 --cpus=2
minikube addons enable ingress
```

Verify:
```bash
kubectl get nodes
# Expected: minikube   Ready   control-plane   ...
```

### 2. Build Docker Images

From the project root (`TODO-PHASE04/`):

```bash
# Build frontend image
docker build -t todo-frontend:latest ./frontend

# Build backend image
docker build -t todo-backend:latest ./backend
```

### 3. Load Images into Minikube

```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

Verify:
```bash
minikube image list | grep todo-
```

### 4. Deploy Database

```bash
helm install todo-database ./helm/todo-database
```

Wait for the database pod to be ready:
```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-database --timeout=60s
```

### 5. Deploy Backend

```bash
helm install todo-backend ./helm/todo-backend
```

Wait for backend pods:
```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-backend --timeout=90s
```

### 6. Deploy Frontend

```bash
helm install todo-frontend ./helm/todo-frontend
```

Wait for frontend pods:
```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-frontend --timeout=90s
```

### 7. Configure Local DNS

Get Minikube IP:
```bash
minikube ip
```

Add to your hosts file:

**Windows** (run as Administrator):
```
# Edit C:\Windows\System32\drivers\etc\hosts
# Add this line:
<minikube-ip> todo.local
```

**macOS/Linux**:
```bash
echo "<minikube-ip> todo.local" | sudo tee -a /etc/hosts
```

### 8. Verify Deployment

```bash
# Check all pods are running
kubectl get pods

# Check all services
kubectl get svc

# Check ingress
kubectl get ingress

# Check Helm releases
helm list
```

### 9. Access the Application

Open your browser and navigate to: `http://todo.local`

You should see the Todo application login/signup page.

### 10. (Optional) AI-Assisted Operations

```bash
# kubectl-ai examples
kubectl-ai "show status of all todo services"
kubectl-ai "scale backend to 3 replicas"

# kagent examples
kagent "analyze cluster health"
```

## Cleanup

To stop the cluster (preserves data):
```bash
minikube stop
```

To remove all deployments:
```bash
helm uninstall todo-frontend
helm uninstall todo-backend
helm uninstall todo-database
```

To delete the cluster entirely (destroys all data):
```bash
minikube delete
```

## Troubleshooting

### Pods stuck in ImagePullBackOff
Images were not loaded into Minikube. Re-run Step 3.

### Pods stuck in CrashLoopBackOff
Check logs: `kubectl logs <pod-name>`
Common causes: missing environment variables, database not ready.

### Cannot access todo.local
1. Verify ingress is running: `kubectl get pods -n ingress-nginx`
2. Verify hosts file has correct Minikube IP
3. Try `minikube tunnel` as alternative to hosts file

### Database connection refused
Wait for the database pod to be fully ready before deploying backend.
Check: `kubectl get pod -l app.kubernetes.io/name=todo-database`
