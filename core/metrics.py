"""Prometheus-style request/error/duration metrics - Module 13.4."""

import time
from prometheus_client import Counter, Histogram, CONTENT_TYPE_LATEST, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "route", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency in seconds", ["route"]
)
ERROR_COUNT = Counter(
    "http_errors_total", "Total 4xx/5xx responses", ["route", "status"]
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        route = request.url.path
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        REQUEST_LATENCY.labels(route=route).observe(duration)
        REQUEST_COUNT.labels(request.method, route, str(response.status_code)).inc()
        if response.status_code >= 400:
            ERROR_COUNT.labels(route, str(response.status_code)).inc()
        return response


async def metrics_endpoint() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
