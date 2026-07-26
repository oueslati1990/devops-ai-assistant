#!/usr/bin/env bash
set -euo pipefail

TAG="latest"

IMAGES=(
  "devops-ai-backend:./backend"
  "devops-ai-mcp:./mcp-server"
)

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

echo ""
echo "Verify with:"
echo "  sudo k3s ctr images ls | grep devops-ai"
