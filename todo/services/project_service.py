from __future__ import annotations
from typing import Optional, Iterable
from todo.config import MAX_NUMBER_OF_PROJECTS
from todo.exceptions.service_exceptions import ProjectAlreadyExists, ProjectNotFound
from todo.repositories.project_repository import ProjectRepository
from todo.repositories.task_repository import TaskRepository  # for cascade checks if needed

class ProjectService:
    def __init__(self, project_store: ProjectRepository, task_store: TaskRepository) -> None:
        self.project_store = project_store
        self.task_store = task_store

    # 1) Create Project
    def create_project(self, name: str, description: Optional[str] = None):
        name = (name or "").strip()
        if not name:
            raise ValueError("Project name cannot be empty.")
        if self.project_store.get_by_name(name):
            raise ProjectAlreadyExists(f'Project with name "{name}" already exists.')
        # capacity check (optional business rule)
        if len(list(self.project_store.list_all())) >= MAX_NUMBER_OF_PROJECTS:
            raise ValueError("Maximum number of projects reached.")
        return self.project_store.create(name, description)

    # 2) Edit Project
    def edit_project(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None):
        p = self.project_store.get_by_id(project_id)
        if not p:
            raise ProjectNotFound(f"Project #{project_id} not found.")
        if name:
            name = name.strip()
            if name == "":
                raise ValueError("Project name cannot be empty.")
            other = self.project_store.get_by_name(name)
            if other and other.id != project_id:
                raise ProjectAlreadyExists(f'Project with name "{name}" already exists.')
        updates = {}
        if name is not None:
            updates["name"] = name
        if description is not None:
            updates["description"] = description
        if not updates:
            return p
        return self.project_store.update(project_id, **updates)

    # 3) Delete Project (tasks removed by FK CASCADE)
    def delete_project(self, project_id: int) -> None:
        if not self.project_store.get_by_id(project_id):
            raise ProjectNotFound(f"Project #{project_id} not found.")
        self.project_store.delete(project_id)

    # 4) List Projects
    def list_projects(self) -> Iterable:
        return self.project_store.list_all()
