""" v1 (Deprecated): 

Demo script:
  GET /v1/orders/ord_0001 -> 200, but note the response headers:
      Deprecation: true
      Sunset: Wed, 31 Dec 2026 23:59:59 GMT
      Link: <.../migration/v2>; rel="deprecation"
"""

from fastapi import APIRouter, HTTPException, Response

from schemas import OrderReadV1
from store import versioned_order_store

router = APIRouter(prefix="/v1/orders", tags=["Orders v1 (Deprecated)"])

DEPRECATION_HEADERS = {
    "Deprecation": "true",
    "Sunset": "Wed, 31 Dec 2026 23:59:59 GMT",
    "Link": '<https://api.example.com/docs/migration/v2>; rel="deprecation"',
}


@router.get("/{order_id}", response_model=OrderReadV1)
async def get_order_v1(order_id: str, response: Response):
    order = versioned_order_store.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    response.headers.update(DEPRECATION_HEADERS)
    return order
