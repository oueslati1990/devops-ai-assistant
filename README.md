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

This builds both Docker images and imports them into k3s's containerd store. Re-run after every code change.

### 4. Deploy

```bash
./scripts/deploy.sh
```

Watch pods come up:

```bash
kubectl get pods -n devops-ai --watch
```

### 5. Access the backend

```bash
kubectl port-forward svc/backend 8080:80 -n devops-ai
```

Open http://localhost:8080