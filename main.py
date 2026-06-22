from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI
from modules import discover_routers

import time
from collections import defaultdict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 30):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()
        self.requests[ip] = [t for t in self.requests[ip] if now - t < self.window]
        if len(self.requests[ip]) >= self.max_requests:
            return JSONResponse(status_code=420, content={"detail": "Enhance Your Calm"})
        self.requests[ip].append(now)
        return await call_next(request)

app = FastAPI(
    title="SwissKnife API",
    description="A general purpose API.",
    version="0.1.0",
    docs_url="/docs",
)
app.add_middleware(RateLimitMiddleware)

for router in discover_routers():
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
