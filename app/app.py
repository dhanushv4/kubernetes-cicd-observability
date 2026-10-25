
import os
import logging
from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry, multiprocess, REGISTRY
from time import perf_counter

app = Flask(__name__)

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

REQUEST_COUNT = Counter(
    "app_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "app_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)


@app.before_request
def start_timer():
    from flask import g
    g.start_time = perf_counter()


@app.after_request
def record_metrics(response):
    from flask import request, g

    endpoint = request.endpoint or "unknown"
    elapsed = perf_counter() - getattr(g, "start_time", perf_counter())

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        http_status=str(response.status_code),
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=endpoint,
    ).observe(elapsed)

    return response


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Kubernetes Deployment and Monitoring API",
        "status": "running",
        "version": os.getenv("APP_VERSION", "1.0.0"),
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/ready", methods=["GET"])
def ready():
    return jsonify({"status": "ready"}), 200


@app.route("/metrics", methods=["GET"])
def metrics():
    return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.exception("Internal server error")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=False,
    )

