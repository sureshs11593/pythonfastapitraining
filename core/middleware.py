"""Request-ID, structured access logging, and simulated distributed tracing.

Module 3.5 (request tracing), Module 13.2 (structured logs), Module 13.5
(trace propagation). Tracing here is a lightweight simulation of a W3C
`traceparent` header (00-<trace_id>-<span_id>-01) so the causal chain can be
demonstrated live in Swagger UI/response headers without standing up a real
OpenTelemetry collector. Wiring `opentelemetry-instrumentation-fastapi`
against Jaeger/Tempo in production follows the exact same header contract.
"""

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging_config import logger


def _new_trace_id() -> str:
    return uuid.uuid4().hex


def _new_span_id() -> str:
    return uuid.uuid4().hex[:16]


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        incoming = request.headers.get("traceparent")
        if incoming and incoming.count("-") == 3:
            _, trace_id, _parent_span, _flags = incoming.split("-")
        else:
            trace_id = _new_trace_id()
        span_id = _new_span_id()
        request.state.trace_id = trace_id
        request.state.span_id = span_id
        response = await call_next(request)
        response.headers["traceparent"] = f"00-{trace_id}-{span_id}-01"
        return response


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "request_completed",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "trace_id": getattr(request.state, "trace_id", None),
                "route": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        return response
