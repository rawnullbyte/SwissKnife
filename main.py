from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI
from modules import discover_routers

app = FastAPI(
    title="SwissKnife API",
    description="A general purpose API.",
    version="0.1.0",
    docs_url="/docs",
)

for router in discover_routers():
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
