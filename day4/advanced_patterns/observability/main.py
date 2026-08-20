

"""Entry point: wires up the Day 4 observability router (logs, metrics, tracing).

Run from the repo root:
    uvicorn app.day4_advanced_patterns.observability.main:app --reload

Then visit /docs to explore, or try:
  GET /day4/observability/logged-call
  GET /day4/observability/trace-demo
"""

from fastapi import FastAPI

from router import router

app = FastAPI(title="Observability Demo")

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "See /docs for available observability routes."}
