
# Monitoring Setup

This project uses kube-prometheus-stack to install Prometheus,
Grafana, Alertmanager, and Kubernetes monitoring components.

## Prerequisites

- A working Kubernetes cluster
- kubectl
- Helm
- The application deployed in the monitoring namespace

## 1. Create the namespace

```bash
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
```

## 2. Add the Prometheus Community Helm repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

## 3. Install the monitoring stack

Run from the project root:

```bash
helm upgrade --install kube-prometheus-stack \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  -f monitoring/values.yaml
```

## 4. Deploy the application

Make sure the Docker image name in k8s/deployment.yaml is correct.

```bash
kubectl apply -f k8s/deployment.yaml -n monitoring
kubectl apply -f k8s/service.yaml -n monitoring
kubectl apply -f k8s/servicemonitor.yaml
```

## 5. Access Grafana

```bash
kubectl port-forward svc/kube-prometheus-stack-grafana \
  3000:80 -n monitoring
```

Open http://localhost:3000.

The chart's default admin username is usually `admin`.
Retrieve the generated password with:

```bash
kubectl get secret kube-prometheus-stack-grafana \
  -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 --decode
```

## 6. Access Prometheus

```bash
kubectl port-forward svc/kube-prometheus-stack-prometheus \
  9090:9090 -n monitoring
```

Open http://localhost:9090.

Check the Status > Targets page and verify that the monitoring-api
target is UP.

## 7. Example PromQL queries

Request rate:

```promql
sum(rate(app_http_requests_total[5m]))
```

Requests by status:

```promql
sum by (http_status) (rate(app_http_requests_total[5m]))
```

Average response latency:

```promql
sum(rate(app_http_request_duration_seconds_sum[5m]))
/
sum(rate(app_http_request_duration_seconds_count[5m]))
```

These application metrics are collected by Prometheus. Kubernetes
CPU and memory metrics are collected separately by the monitoring stack.

