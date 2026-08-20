from fastapi import FastAPI
from routers.v1 import router as v1_router
from routers.v2 import router as v2_router

app=FastAPI(
       title="Products API",
       description="Versioned FastAPI contracts by Murthy",
       version="2.0.1"
)

app.include_router(v1_router)
app.include_router(v2_router)

@app.get("/",tags={"Products API"})
def home():
    return { "message": "Products with Versioning", "versions": ['Deprecated(V1)', 'V2']}