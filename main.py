import time
import uuid
from typing import Optional

from fastapi import FastAPI, Request, Response

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-k35dkw.example.com"
YOUR_EMAIL = "24f3001667@ds.study.iitm.ac.in"


@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start = time.perf_counter()
    request_id = str(uuid.uuid4())

    response: Response = await call_next(request)

    duration = time.perf_counter() - start
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{duration:.6f}"

    origin = request.headers.get("origin")
    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        response.headers["Vary"] = "Origin"

    return response


@app.options("/stats")
async def options_stats(request: Request):
    response = Response(content="", status_code=200)
    origin = request.headers.get("origin")

    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        response.headers["Access-Control-Allow-Methods"] = "GET"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Vary"] = "Origin"

    return response


@app.get("/stats")
async def get_stats(values: Optional[str] = None):
    numbers = [int(x.strip()) for x in values.split(",")] if values else []

    if not numbers:
        return {
            "email": YOUR_EMAIL,
            "count": 0,
            "sum": 0,
            "min": None,
            "max": None,
            "mean": 0.0,
        }

    total = sum(numbers)
    count = len(numbers)

    return {
        "email": YOUR_EMAIL,
        "count": count,
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / count,
    }