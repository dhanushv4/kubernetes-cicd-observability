
IMAGE ?= YOUR_DOCKERHUB_USERNAME/kubernetes-monitoring-api
TAG ?= latest
NAMESPACE ?= monitoring

.PHONY: install test run build push deploy status logs port-forward clean

install:
	python -m pip install -r requirements-dev.txt

test:
	python -m pytest -v

run:
	cd app && python app.py

build:
	docker build -t $(IMAGE):$(TAG) .

push:
	docker push $(IMAGE):$(TAG)

deploy:
	kubectl create namespace $(NAMESPACE) --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -n $(NAMESPACE) -f k8s/deployment.yaml
	kubectl apply -n $(NAMESPACE) -f k8s/service.yaml
	kubectl apply -f k8s/servicemonitor.yaml
	kubectl rollout status deployment/monitoring-api -n $(NAMESPACE)

status:
	kubectl get pods,deployments,services -n $(NAMESPACE)

logs:
	kubectl logs deployment/monitoring-api -n $(NAMESPACE) --follow

port-forward:
	kubectl port-forward service/monitoring-api 8080:80 -n $(NAMESPACE)

clean:
	kubectl delete -f k8s/servicemonitor.yaml --ignore-not-found
	kubectl delete -n $(NAMESPACE) -f k8s/service.yaml --ignore-not-found
	kubectl delete -n $(NAMESPACE) -f k8s/deployment.yaml --ignore-not-found

