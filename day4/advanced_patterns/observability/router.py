"""Day 4 - Module 13: logging, metrics, tracing demonstrations.

Demo script:
  1. Open a terminal tailing the uvicorn stdout (structured JSON logs live there).
  2. GET /day4/observability/logged-call  -> watch a JSON log line appear.
  3. GET /day4/observability/trace-demo   -> shows a simulated multi-span
     trace (all spans share one trace_id) - the same header contract a real
     OpenTelemetry + Jaeger/Tempo setup would use.
  4. GET /metrics                        -> raw Prometheus exposition format;
     point out http_requests_total / http_request_duration_seconds / http_errors_total.
"""

import time
import uuid

from fastapi import APIRouter, Request

from logging_config import logger

router = APIRouter(prefix="/day4/observability", tags=["Observability (Logs, Metrics, Tracing)"])


@router.get("/logged-call")
async def logged_call(request: Request):
    """Emits an explicit structured log line beyond the automatic access log,
    so the class can see request_id/trace_id correlate log lines together."""
    logger.info(
        "business_event_processed",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "trace_id": getattr(request.state, "trace_id", None),
            "route": request.url.path,
        },
    )
    return {
        "message": "Check your terminal - a structured JSON log line was just emitted.",
        "request_id": getattr(request.state, "request_id", None),
        "trace_id": getattr(request.state, "trace_id", None),
    }


def _child_span(name: str, trace_id: str, parent_span: str) -> dict:
    span_id = uuid.uuid4().hex[:16]
    start = time.perf_counter()
    time.sleep(0.01)  # simulate work
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    return {"span_name": name, "trace_id": trace_id, "span_id": span_id, "parent_span_id": parent_span, "duration_ms": duration_ms}


@router.get("/trace-demo")
async def trace_demo(request: Request):
    """Simulates a 3-hop call chain (API -> inventory -> payments) that all
    share one trace_id, mirroring Module 13.5's distributed tracing diagram."""
    trace_id = getattr(request.state, "trace_id", uuid.uuid4().hex)
    root_span = getattr(request.state, "span_id", uuid.uuid4().hex[:16])
    spans = [
        _child_span("check_inventory", trace_id, root_span),
        _child_span("charge_payment", trace_id, root_span),
        _child_span("write_order_confirmation", trace_id, root_span),
    ]
    return {"trace_id": trace_id, "root_span_id": root_span, "spans": spans}
