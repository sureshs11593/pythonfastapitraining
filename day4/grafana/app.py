from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import random

app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.get("/")
def home():
    return {"message": "Welcome"}

@app.get("/users")
def users():
    return {
        "users": random.randint(10,100)
    }

@app.get("/orders")
def orders():
    return {
        "orders": random.randint(100,500)
    }

#uvicorn app:app --reload