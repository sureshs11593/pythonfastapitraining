"""Day 4 - Module 14: idempotency keys, async job pattern, rate limit
signaling, ETag optimistic concurrency.

Demo script:
  Idempotency:
    POST /day4/payments  {"amount": 100} with header Idempotency-Key: abc-1
    -> repeat the exact same call with the same key -> identical response,
       charged_count stays at 1 (no double charge).

  Async job:
    POST /day4/reports              -> 202 + job_id + status_url
    GET  /day4/reports/{job_id}     -> "pending" then "done" after ~3s

  Rate limiting:
    GET /day4/rate-limited-ping  x6 quickly -> 6th call returns 429 + Retry-After

  ETag / optimistic concurrency:
    GET /day4/orders/ord_0001            -> note the ETag response header
    PUT /day4/orders/ord_0001 with stale If-Match -> 412 Precondition Failed
"""

import hashlib
import time

from fastapi import APIRouter, Header, HTTPException, Response

from app.day4_advanced_patterns.store import versioned_order_store
from app.day4_advanced_patterns.idempotency_store import idempotency_store
from app.day4_advanced_patterns.job_store import job_store

router = APIRouter(prefix="/day4", tags=["Day 4 - Advanced Patterns (Idempotency, Jobs, Rate Limits, ETags)"])

_payment_charge_counter = {"count": 0}


@router.post("/payments", status_code=201)
async def create_payment(payload: dict, idempotency_key: str = Header(..., alias="Idempotency-Key")):
    existing = idempotency_store.get(idempotency_key)
    if existing:
        return existing  # replay original result - no double charge
    _payment_charge_counter["count"] += 1
    result = {
        "payment_id": f"pay_{idempotency_key}",
        "amount": payload.get("amount"),
        "status": "charged",
        "total_charges_ever_made": _payment_charge_counter["count"],
    }
    idempotency_store.save(idempotency_key, result)
    return result


@router.post("/reports", status_code=202)
async def start_report(payload: dict | None = None):
    job_id = job_store.enqueue(payload or {})
    return {"job_id": job_id, "status_url": f"/day4/reports/{job_id}"}


@router.get("/reports/{job_id}")
async def get_report_status(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return job


_RATE_LIMIT = 5
_RATE_WINDOW_SECONDS = 10
_rate_limit_hits: list[float] = []


@router.get("/rate-limited-ping")
async def rate_limited_ping(response: Response):
    now = time.monotonic()
    while _rate_limit_hits and now - _rate_limit_hits[0] > _RATE_WINDOW_SECONDS:
        _rate_limit_hits.pop(0)
        ''' above code says:
        _rate_limit_hits is a list of timestamps for recent requests
        while _rate_limit_hits and now -..... :  keep removing the oldest timestamp 
        from the front while it is older than the rate-limit window
        this cleans out expired hits so the reate limiter only counts requrests made within
        the last 10 seconds
        '''
        

    remaining = _RATE_LIMIT - len(_rate_limit_hits)
    if remaining <= 0:
        retry_after = int(_RATE_WINDOW_SECONDS - (now - _rate_limit_hits[0]))
        raise HTTPException(
            status_code=429,
            detail="RATE_LIMITED",
            headers={"Retry-After": str(max(retry_after, 1)), "X-RateLimit-Remaining": "0"},
        )

    _rate_limit_hits.append(now)
    response.headers["X-RateLimit-Limit"] = str(_RATE_LIMIT)
    response.headers["X-RateLimit-Remaining"] = str(remaining - 1)
    return {"message": "pong", "requests_remaining_in_window": remaining - 1}


def _etag_for(order: dict) -> str:
    raw = f"{order['id']}-{order['quantity']}-{order['status']}-{order['price']}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


@router.get("/orders/{order_id}")
async def get_order_with_etag(order_id: str, response: Response):
    order = versioned_order_store.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    response.headers["ETag"] = _etag_for(order)
    return order


@router.put("/orders/{order_id}")
async def update_order_with_etag(order_id: str, payload: dict, if_match: str = Header(None, alias="If-Match")):
    order = versioned_order_store.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    current_etag = _etag_for(order)
    if if_match != current_etag:
        raise HTTPException(status_code=412, detail="PRECONDITION_FAILED")
    if "quantity" in payload:
        order["quantity"] = payload["quantity"]
    return order
