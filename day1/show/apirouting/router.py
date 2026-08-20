"""Day 1 - Modules 1-4: basic CRUD, validation, auth, pagination, health.

Demo script:
  GET  /day1/orders                              -> 401 (no token)
  GET  /day1/orders  (viewer-readonly-token)      -> 200, paginated list
  POST /day1/orders  (viewer-readonly-token)      -> 403 (wrong role)
  POST /day1/orders  (trainer-admin-token)        -> 201 created
  GET  /day1/orders/{unknown-id}                  -> 404
  GET  /healthz/live | /healthz/ready             -> liveness/readiness
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from pagination import decode_cursor, encode_cursor
from security import get_current_user, require_role
from schemas import OrderCreate, OrderPage, OrderRead, OrderUpdate
from store import order_store
'''
the tags parameter in an API route is mainly used to group and organize API 
endpoints in the automatically generated Swagger/OpenAPI documentation.

@app.post("/customers", tags=["Customers"])
def create_customer():
    return {"message": "Customer created"}

@app.get("/products", tags=["Products"])
def get_products():
    return {"message": "All products"}
    
in swagger  you will see :
Customers
   POST /customers

Products
   GET  /products
'''

orders_router = APIRouter(prefix="/day1/orders", 
                            tags=["CRUD, Auth, Pagination"])
health_router = APIRouter(tags=["Health Checks"])


@orders_router.get("", response_model=OrderPage)
async def list_orders(
    cursor: str | None = None, #optional query param for pagination
    limit: int = Query(5, le=100, gt=0), #qieru [ara, wotj default 5, max 100 and min >0]
    #user: dict = Depends(get_current_user),#dependency injection (depends on user)
):
    after_id = decode_cursor(cursor)
    rows, has_more = order_store.list(after_id, limit)
    next_cursor = encode_cursor(rows[-1]["id"]) if has_more and rows else None
    return {"data": rows, "page": {"next_cursor": next_cursor, "has_more": has_more, "limit": limit}}


@orders_router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate):# user: dict = Depends(require_role("admin"))):
    return order_store.create(payload.customer_id, payload.quantity, payload.notes)


@orders_router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: str) :#,user: dict = Depends(get_current_user)):
    order = order_store.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return order


@orders_router.patch("/{order_id}", response_model=OrderRead)
async def update_order(order_id: str, payload: OrderUpdate):#,user: dict = Depends(require_role("admin"))):
    order = order_store.update(order_id, **payload.model_dump(exclude_unset=True))
    if not order:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return order


@orders_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str): #, user: dict = Depends(require_role("admin"))):
    if not order_store.delete(order_id):
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@health_router.get("/healthz/live")
async def liveness():
    """Process is up - no dependency checks. Orchestrator restarts on failure."""
    return {"status": "ok"}


@health_router.get("/healthz/ready")
async def readiness():
    """Can the app serve traffic right now? Orchestrator pulls from LB on failure."""
    # In a real app this would ping the DB/cache/downstream deps.
    dependencies_ok = True
    if not dependencies_ok:
        raise HTTPException(status_code=503, detail="NOT_READY")
    return {"status": "ready"}
