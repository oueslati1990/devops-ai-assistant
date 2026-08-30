# devops-ai-assistant
An LLM powered devops assistant

## Services
- `backend/` — FastAPI + LLM integration
- `mcp-server/` — MCP Server with DevOps tools

## Kubernetes Setup (k3s)

### 1. Install k3s

```bash
curl -sfL https://get.k3s.io | sh -
```

### 2. Fix kubeconfig permissions

k3s installs `kubectl` as a symlink to its own binary, which reads `/etc/rancher/k3s/k3s.yaml` directly. Make it readable without sudo:

```bash
sudo chmod 644 /etc/rancher/k3s/k3s.yaml
```

Verify the cluster is up:

```bash
kubectl get nodes
```

### 3. Build and import images

```bash
./scripts/build-and-import.sh
```

### 4. Deploy

```bash
./scripts/deploy.sh
```

### 5. Wait for pods to be ready

```bash
kubectl get pods -n devops-ai --watch
```

### 6. Access the app

```bash
kubectl port-forward svc/backend 8080:80 -n devops-ai
```

Open http://localhost:8080

## After a code change

```bash
./scripts/build-and-import.sh
kubectl rollout restart deployment/backend -n devops-ai
kubectl rollout restart deployment/mcp-server -n devops-ai  # if mcp-server changed
```