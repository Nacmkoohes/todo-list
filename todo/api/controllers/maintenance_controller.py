from __future__ import annotations

from fastapi import APIRouter, status
from todo.services.app_factory import build_services
from todo.services.task_service import TaskService

router = APIRouter()


def get_task_service() -> TaskService:
    _, ts = build_services()
    return ts


@router.post(
    "/autoclose-overdue-tasks",
    status_code=status.HTTP_200_OK,
    summary="Auto-close all overdue tasks",
)
def autoclose_overdue_tasks():
    """
    Closes all overdue open tasks and returns how many were updated.
    """
    ts = get_task_service()
    closed_count = ts.autoclose_overdue_tasks()
    return {"closed_tasks": closed_count}
