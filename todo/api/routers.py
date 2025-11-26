from __future__ import annotations

from fastapi import APIRouter

from todo.api.controllers import project_controller, task_controller

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(project_controller.router)
api_router.include_router(task_controller.router)
