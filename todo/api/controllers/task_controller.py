from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status
from ..controller_schemas.task_requests import TaskCreate, TaskUpdate
from ..controller_schemas.task_responses import TaskRead
from todo.services.task_service import TaskService
from todo.services.app_factory import build_services

router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["tasks"],
)


def get_task_service() -> TaskService:
    _, ts = build_services()
    return ts


@router.get(
    "/",
    response_model=List[TaskRead],
)
def list_tasks(project_id: int):
    ts = get_task_service()
    try:
        tasks = ts.list_tasks(project_id)
        return [TaskRead.model_validate(t) for t in tasks]
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )


@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(project_id: int, payload: TaskCreate):
    ts = get_task_service()
    try:
        task = ts.create_task(
            project_id=project_id,
            title=payload.title,
            description=payload.description,
            deadline=payload.deadline,
        )
        return TaskRead.model_validate(task)
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{task_id}",
    response_model=TaskRead,
)
def get_task(project_id: int, task_id: int):
    ts = get_task_service()
    task = ts.get_task(project_id, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return TaskRead.model_validate(task)


@router.patch(
    "/{task_id}",
    response_model=TaskRead,
)
def update_task(project_id: int, task_id: int, payload: TaskUpdate):
    ts = get_task_service()
    update_data = payload.model_dump(exclude_unset=True)

    try:
        task = ts.update_task(
            project_id=project_id,
            task_id=task_id,
            **update_data,
        )
        return TaskRead.model_validate(task)
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or project not found",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(project_id: int, task_id: int):
    ts = get_task_service()
    ts.delete_task(project_id, task_id)
    return
