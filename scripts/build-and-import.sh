#!/usr/bin/env bash
set -euo pipefail

TAG="latest"

IMAGES=(
  "devops-ai-backend:./backend"
  "devops-ai-mcp:./mcp-server"
)

OLLAMA_IMAGE="ollama/ollama:latest"

for entry in "${IMAGES[@]}"; do
  name="${entry%%:*}"
  context="${entry#*:}"
  full="${name}:${TAG}"

  echo "==> Building ${full} from ${context}"
  docker build -t "${full}" "${context}"

  echo "==> Importing ${full} into k3s"
  docker save "${full}" | sudo k3s ctr images import -

  echo "==> Done: ${full}"
done

echo "==> Pulling ${OLLAMA_IMAGE}"
docker pull "${OLLAMA_IMAGE}"
echo "==> Importing ${OLLAMA_IMAGE} into k3s"
docker save "${OLLAMA_IMAGE}" | sudo k3s ctr images import -
echo "==> Done: ${OLLAMA_IMAGE}"

echo ""
echo "Verify with:"
echo "  sudo k3s ctr images ls | grep -E 'devops-ai|ollama'"
