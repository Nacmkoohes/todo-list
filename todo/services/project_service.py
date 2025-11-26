from __future__ import annotations

from typing import Iterable, Optional

from todo.config import MAX_NUMBER_OF_PROJECTS
from todo.models.project import Project
from todo.repositories.project_repository import ProjectRepository
from todo.repositories.task_repository import TaskRepository


class ProjectService:
    """Application service for managing projects."""

    def __init__(
        self,
        project_repo: ProjectRepository,
        task_repo: TaskRepository,
    ) -> None:
        self.project_repo = project_repo
        self.task_repo = task_repo

    def list_projects(self) -> Iterable[Project]:
        return self.project_repo.list_all()

    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
    ) -> Project:
        existing_projects = list(self.project_repo.list_all())
        if len(existing_projects) >= MAX_NUMBER_OF_PROJECTS:
            raise ValueError("Maximum number of projects reached")

        # Optional: check duplicate name
        existing = self.project_repo.get_by_name(name)
        if existing is not None:
            raise ValueError("Project with this name already exists")

        return self.project_repo.create(name=name, description=description)

    def get_project(self, project_id: int) -> Optional[Project]:
        return self.project_repo.get_by_id(project_id)

    def update_project(self, project_id: int, **fields) -> Project:
        # Could enforce domain rules here if needed
        project = self.project_repo.update(project_id, **fields)
        return project

    def delete_project(self, project_id: int) -> None:
        # Deleting project cascades tasks by DB foreign key
        self.project_repo.delete(project_id)
