from __future__ import annotations
from typing import Protocol, Callable, Iterable, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from todo.models.project import Project

class ProjectRepository(Protocol):
    def create(self, name: str, description: str = "") -> Project: ...
    def get(self, project_id: int) -> Optional[Project]: ...
    def get_by_name(self, name: str) -> Optional[Project]: ...
    def list(self) -> List[Project]: ...
    def update(self, project: Project) -> None: ...
    def delete(self, project_id: int) -> bool: ...

class SqlAlchemyProjectRepository(ProjectRepository):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def create(self, name: str, description: str = "") -> Project:
        with self._session_factory() as s:
            p = Project(name=name.strip(), description=description or "")
            s.add(p)
            s.commit()
            s.refresh(p)
            return p

    def get(self, project_id: int) -> Optional[Project]:
        with self._session_factory() as s:
            return s.get(Project, project_id)

    def get_by_name(self, name: str) -> Optional[Project]:
        with self._session_factory() as s:
            stmt = select(Project).where(func.lower(Project.name) == name.strip().lower())
            return s.scalar(stmt)

    def list(self) -> List[Project]:
        with self._session_factory() as s:
            stmt = select(Project).order_by(Project.id.asc())
            return list(s.scalars(stmt))

    def update(self, project: Project) -> None:
        # فرض: نمونهٔ project از قبل با session جدا ساخته شده؛ merge می‌کنیم
        with self._session_factory() as s:
            s.merge(project)
            s.commit()

    def delete(self, project_id: int) -> bool:
        with self._session_factory() as s:
            obj = s.get(Project, project_id)
            if not obj:
                return False
            s.delete(obj)   # به‌خاطر cascade، Taskها هم orphan می‌شن و حذف می‌شن
            s.commit()
            return True
