
# End-to-End Kubernetes Deployment & Monitoring with CI/CD

A DevOps portfolio project that deploys a Python Flask API to
Kubernetes, builds a Docker image, runs automated tests, and monitors
application metrics with Prometheus and Grafana.

## Technology Stack

- Python and Flask
- Docker
- Kubernetes
- Prometheus
- Grafana
- Helm
- GitHub Actions
- Pytest

## Features

- REST API with health and readiness endpoints
- Prometheus request counters and latency metrics
- Containerized application running as a non-root user
- Kubernetes Deployment with two replicas
- Resource requests and limits
- Liveness, readiness, and startup probes
- Prometheus ServiceMonitor
- Automated CI/CD pipeline
- Grafana dashboard support

## Architecture

GitHub -> GitHub Actions -> Pytest -> Docker Build -> Docker Hub
-> Kubernetes -> Prometheus -> Grafana

## Prerequisites

Install:

- Python 3.12 or later
- Docker
- kubectl
- Helm
- Minikube or another Kubernetes cluster

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd kubernetes-monitoring-cicd
```

## 2. Install dependencies and test

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install and run tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

## 3. Run locally

```bash
cd app
python app.py
```

Test these endpoints:

- http://localhost:5000/
- http://localhost:5000/health
- http://localhost:5000/ready
- http://localhost:5000/metrics

## 4. Build the Docker image

Replace YOUR_DOCKERHUB_USERNAME with your Docker Hub username.

```bash
docker build -t YOUR_DOCKERHUB_USERNAME/kubernetes-monitoring-api:latest .
docker run --rm -p 5000:5000 YOUR_DOCKERHUB_USERNAME/kubernetes-monitoring-api:latest
```

## 5. Start Kubernetes

For Minikube:

```bash
minikube start
kubectl get nodes
```

Build the image and make it available to Minikube using either:

```bash
minikube image build -t YOUR_DOCKERHUB_USERNAME/kubernetes-monitoring-api:latest .
```

Or push it to Docker Hub and let Kubernetes pull it.

## 6. Install monitoring

Follow monitoring/README.md to install kube-prometheus-stack.

## 7. Deploy the application

Update the image in k8s/deployment.yaml, then run:

```bash
make deploy
make status
make port-forward
```

Open http://localhost:8080.

## 8. Verify the deployment

```bash
kubectl get pods -n monitoring
kubectl rollout status deployment/monitoring-api -n monitoring
kubectl logs deployment/monitoring-api -n monitoring
```

## 9. Verify monitoring

Open Grafana at http://localhost:3000 and Prometheus at
http://localhost:9090 using the port-forward commands in
monitoring/README.md.

In Prometheus, query:

```promql
app_http_requests_total
```

Generate requests to the application and check that the metric changes.

## Troubleshooting

ImagePullBackOff:
- Check the image name and registry access.
- Verify the image exists in Docker Hub.

Pods not ready:
- Run kubectl describe pod and kubectl logs.
- Check that the probes and container port match the application.

ServiceMonitor target missing:
- Confirm the Service and ServiceMonitor labels.
- Check the Prometheus selector and namespace configuration.
- Confirm that the Service exposes a port named http.

## Security Notes

- Do not commit Docker Hub credentials or kubeconfig files.
- Use GitHub Actions secrets for CI/CD credentials.
- For production, use a managed secret solution, persistent monitoring
  storage, TLS, network policies, and least-privilege RBAC.

## Future Enhancements

- Add application alert rules
- Add a custom Grafana dashboard
- Deploy with Argo CD
- Add Trivy image scanning
- Add ingress and TLS
- Add Helm charts for the application

## Portfolio Outcome

Demonstrates containerization, CI/CD, Kubernetes orchestration,
health checks, observability, and infrastructure troubleshooting.

