from __future__ import annotations

from todo.repositories.project_repository import SqlAlchemyProjectRepository
from todo.repositories.task_repository import SqlAlchemyTaskRepository
from todo.services.project_service import ProjectService
from todo.services.task_service import TaskService


def build_services() -> tuple[ProjectService, TaskService]:
    """Factory for building application services.

    Used by CLI (legacy) and Web API (FastAPI controllers).
    """
    proj_repo = SqlAlchemyProjectRepository()
    task_repo = SqlAlchemyTaskRepository()
    project_service = ProjectService(proj_repo, task_repo)
    task_service = TaskService(proj_repo, task_repo)
    return project_service, task_service
