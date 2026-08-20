"""Entry point: wires up the Day 4 advanced patterns router (idempotency,
async jobs, rate limiting, ETag optimistic concurrency).

Run from the repo root:
    uvicorn app.day4_advanced_patterns.main:app --reload

Then visit /docs to explore, or try:
  POST /day4/payments            (header Idempotency-Key: abc-1)
  POST /day4/reports
  GET  /day4/reports/{job_id}
  GET  /day4/rate-limited-ping
  GET  /day4/orders/{order_id}
  PUT  /day4/orders/{order_id}   (header If-Match: <etag>)
"""

from fastapi import FastAPI

from router import router

app = FastAPI(title="Advanced Patterns Demo")

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "See /docs for available advanced-patterns routes."}
