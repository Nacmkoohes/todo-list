from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status
from ..controller_schemas.project_requests import ProjectCreate, ProjectUpdate
from ..controller_schemas.project_responses import ProjectRead
from todo.services.project_service import ProjectService
from todo.services.app_factory import build_services

# ❗ بدون prefix و بدون tags
router = APIRouter()


def get_project_service() -> ProjectService:
    ps, _ = build_services()
    return ps


@router.get(
    "/",
    response_model=List[ProjectRead],
)
def list_projects():
    ps = get_project_service()
    projects = ps.list_projects()
    return [ProjectRead.model_validate(p) for p in projects]


@router.post(
    "/",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_project(payload: ProjectCreate):
    ps = get_project_service()
    try:
        project = ps.create_project(
            name=payload.name,
            description=payload.description,
        )
        return ProjectRead.model_validate(project)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
)
def get_project(project_id: int):
    ps = get_project_service()
    project = ps.get_project(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return ProjectRead.model_validate(project)


@router.patch(
    "/{project_id}",
    response_model=ProjectRead,
)
def update_project(project_id: int, payload: ProjectUpdate):
    ps = get_project_service()
    update_data = payload.model_dump(exclude_unset=True)

    try:
        project = ps.update_project(project_id, **update_data)
        return ProjectRead.model_validate(project)
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


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(project_id: int):
    ps = get_project_service()
    ps.delete_project(project_id)
    # 204 → نیازی به بدنه‌ی پاسخ نیست
    return None
