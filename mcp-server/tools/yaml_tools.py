import yaml


def generate_yaml(type: str, params: dict) -> str:
    generators = {
        "k8s-deployment": _k8s_deployment,
        "k8s-service": _k8s_service,
        "k8s-ingress": _k8s_ingress,
    }

    if type not in generators:
        return f"Unkown type: {type}. Choose from {", ".join(generators)}"

    manifest = generators[type](params)
    return f"```yaml\n{yaml.dump(manifest, default_flow_style=False)}```"


def _k8s_ingress(params: dict) -> dict:
    name = params.get("name", "my-app")
    host = params.get("host", f"{name}.example.com")
    return {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": name,
            "annotations": {"nginx.ingress.kubernetes.io/rewrite-target": "/"},
        },
        "spec": {
            "ingressClassName": "nginx",
            "rules": [
                {
                    "host": host,
                    "http": {
                        "paths": [
                            {
                                "path": "/",
                                "pathType": "Prefix",
                                "backend": {
                                    "service": {"name": name, "port": {"number": 80}}
                                },
                            }
                        ]
                    },
                }
            ],
        },
    }


def _k8s_service(params: dict) -> dict:
    name = params.get("name", "my-app")
    port = int(params.get("port", 8000))
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": name},
        "spec": {
            "selector": {"app": name},
            "ports": [{"protocol": "TCP", "port": 80, "targetPort": port}],
            "type": params.get("type", "ClusterIP"),
        },
    }


def _k8s_deployment(params: dict) -> dict:
    name = params.get("name", "my-app")
    image = params.get("image", "my-app:latest")
    port = int(params.get("port", 8000))
    replicas = int(params.get("replicas", 2))
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "labels": {"app": name}},
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [
                        {
                            "name": name,
                            "image": image,
                            "ports": [{"containerPort": port}],
                            "resources": {
                                "requests": {"memory": "128Mi", "cpu": "100m"},
                                "limits": {"memory": "512Mi", "cpu": "500m"},
                            },
                            "livenessProbe": {
                                "httpGet": {"path": "/health", "port": port},
                                "initialDelaySeconds": 10,
                                "periodSeconds": 15,
                            },
                        }
                    ]
                },
            },
        },
    }
