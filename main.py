from __future__ import annotations

from fastapi import FastAPI

from todo.api.routers import api_router

app = FastAPI(
    title="ToDoList API",
    version="0.3.0",
    description="ToDoList Web API for managing projects and tasks (Phase 3).",
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Simple health-check endpoint."""
    return {"status": "ok"}


# Mount all API routers (v1)
app.include_router(api_router)
