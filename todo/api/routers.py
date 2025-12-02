from __future__ import annotations

from fastapi import APIRouter, status
from todo.services.app_factory import build_services
from todo.services.task_service import TaskService
from todo.models.task import Task

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
    Closes all overdue open tasks and returns details of closed tasks.
    """

    ts = get_task_service()

    # Step 1: Collect the overdue tasks BEFORE closing them
    overdue_tasks: list[Task] = list(ts.list_overdue_open())

    # Step 2: Actually close them (your existing logic)
    closed_count = ts.autoclose_overdue_tasks()

    # Step 3: Build output list with fields you want
    closed_info = [
        {
            "id": t.id,
            "title": t.title,
            "deadline": t.deadline
        }
        for t in overdue_tasks
    ]

    return {
        "closed": closed_info,
        "count": closed_count
    }
