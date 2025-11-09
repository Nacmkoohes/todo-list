from __future__ import annotations
from typing import Iterable, Optional
from ..config import MAX_NUMBER_OF_PROJECTS
from ..repositories import Project

class ProjectService:
    def __init__(self, project_store=None) -> None:
        if project_store is None:
            from ..in_memory_store import InMemoryProjectRepo
            project_store = InMemoryProjectRepo()
        self.project_store = project_store

    def _to_int(self, value) -> int:
        if isinstance(value, int):
            return value
        return int(str(value).strip())

    # 1) Create
    def create_project(self, name: str, description: str = "") -> Project:
        if len(list(self.project_store.list())) >= MAX_NUMBER_OF_PROJECTS:
            raise ValueError(f"Error: Maximum number of projects reached (limit={MAX_NUMBER_OF_PROJECTS}).")
        p = Project(name=name.strip(), description=description.strip())
        return self.project_store.add(p)

    # 2) List
    def list_projects(self) -> Iterable[Project]:
        return self.project_store.list()

    def get_project(self, project_id) -> Project:
        return self.project_store.get(self._to_int(project_id))

    # 3) Edit
    def edit_project(self, project_id, *, name: Optional[str] = None, description: Optional[str] = None) -> Project:
        pid = self._to_int(project_id)
        p = self.project_store.get(pid)
        if name is not None:
            p.name = name.strip()
        if description is not None:
            p.description = description.strip()
        self.project_store.save(p)
        return p

    # 4) Delete
    def delete_project(self, project_id) -> None:
        self.project_store.delete(self._to_int(project_id))
