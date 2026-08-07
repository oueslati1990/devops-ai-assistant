# Add the Helm repo
# This will install Prometheus, Grafana, node-exporter (hardware metrics), 
# kube-state-metrics (pod health), and AlertManager in one command.
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install into its own namespace
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace