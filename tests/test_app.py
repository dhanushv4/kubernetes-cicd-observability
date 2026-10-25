
import pytest
from app.app import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "running"
    assert data["version"]


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ready"


def test_metrics_endpoint(client):
    client.get("/")
    response = client.get("/metrics")

    assert response.status_code == 200
    assert b"app_http_requests_total" in response.data
    assert b"app_http_request_duration_seconds" in response.data


def test_unknown_route(client):
    response = client.get("/unknown-route")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Not found"

