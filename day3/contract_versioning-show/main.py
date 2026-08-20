"""Entry point: wires up v1 (deprecated) and v2 (current) order routers.

Run:
    uvicorn main:app --reload

Then visit /docs to explore both versions, or try:
  GET  /v1/orders/ord_0001
  GET  /v2/orders
  GET  /v2/orders/ord_0001
  GET  /v2/orders/ord_0001/items
  POST /v2/orders/ord_0001/cancel
"""

from fastapi import FastAPI

from router_v1 import router as router_v1
from router_v2 import router as router_v2

app = FastAPI(title="Contract Versioning Demo")

app.include_router(router_v1)
app.include_router(router_v2)


@app.get("/")
async def root():
    return {"message": "See /docs for available v1 and v2 order routes."}
