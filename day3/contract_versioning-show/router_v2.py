"""v2: current version. Demonstrates resource modeling (Module 8),
sub-resources, controller actions, cache-control, and pagination.

Demo script:
  GET  /v2/orders                       -> paginated list (new envelope)
  GET  /v2/orders/ord_0001               -> nested `amount` object (breaking vs v1)
  GET  /v2/orders/ord_0001/items         -> sub-resource collection
  POST /v2/orders/ord_0001/cancel        -> controller action (not a CRUD verb)
"""

from fastapi import APIRouter, HTTPException, Query, Response

from pagination import decode_cursor, encode_cursor
from schemas import OrderItemV2, OrderPageV2, OrderReadV2
from store import versioned_order_store

router = APIRouter(prefix="/v2/orders", tags=["Orders v2 (Current)"])


def _to_v2(order: dict) -> dict:
    return {
        "id": order["id"],
        "customer_id": order["customer_id"],
        "quantity": order["quantity"],
        "amount": {"amount": order["price"], "currency": "USD"},
        "created_at": order["created_at"],
    }


@router.get("", response_model=OrderPageV2)
async def list_orders_v2(cursor: str | None = None, limit: int = Query(5, le=100, gt=0)):
    after_id = decode_cursor(cursor)
    rows, has_more = versioned_order_store.list(after_id, limit)
    next_cursor = encode_cursor(rows[-1]["id"]) if has_more and rows else None
    return {
        "data": [_to_v2(o) for o in rows],
        "page": {"next_cursor": next_cursor, "has_more": has_more, "limit": limit},
    }


@router.get("/{order_id}", response_model=OrderReadV2)
async def get_order_v2(order_id: str, response: Response):
    order = versioned_order_store.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    # Order data is customer-specific -> never let a shared proxy cache it (Module 10.5)
    response.headers["Cache-Control"] = "no-store, private"
    return _to_v2(order)


@router.get("/{order_id}/items", response_model=list[OrderItemV2])
async def list_order_items(order_id: str):
    order = versioned_order_store.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return order["items"]


@router.post("/{order_id}/cancel", response_model=OrderReadV2)
async def cancel_order(order_id: str):
    order = versioned_order_store.cancel(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return _to_v2(order)
