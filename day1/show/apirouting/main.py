from fastapi import FastAPI

from router import health_router, orders_router

app = FastAPI()

app.include_router(orders_router)
app.include_router(health_router)
