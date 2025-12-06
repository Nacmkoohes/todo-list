from __future__ import annotations

from typing import Any, Iterable, Optional, Protocol, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from todo.db.session import SessionLocal
from todo.models.project import Project


class ProjectRepository(Protocol):
    """Abstraction for project persistence layer."""

    def create(self, name: str, description: Optional[str] = None) -> Project: ...
    def update(self, project_id: int, **fields: Any) -> Project: ...
    def delete(self, project_id: int) -> None: ...
    def get_by_id(self, project_id: int) -> Optional[Project]: ...
    def get_by_name(self, name: str) -> Optional[Project]: ...
    def list_all(self) -> Iterable[Project]: ...


class SqlAlchemyProjectRepository(ProjectRepository):
    """SQLAlchemy implementation of ProjectRepository."""

    def __init__(self, session_factory=SessionLocal) -> None:
        self.session_factory = session_factory

    def create(self, name: str, description: Optional[str] = None) -> Project:
        with self.session_factory() as s:  # type: Session
            project = Project(name=name, description=description)
            s.add(project)
            s.commit()
            s.refresh(project)
            return project

    def update(self, project_id: int, **fields: Any) -> Project:
        with self.session_factory() as s:
            project: Project | None = s.get(Project, project_id)
            if project is None:
                raise LookupError(f"Project #{project_id} not found")

            for key, value in fields.items():
                if value is not None:
                    setattr(project, key, value)

            s.commit()
            s.refresh(project)
            return project

    def delete(self, project_id: int) -> None:
        with self.session_factory() as s:
            project = s.get(Project, project_id)
            if project is None:
                return
            s.delete(project)
            s.commit()

    def get_by_id(self, project_id: int) -> Optional[Project]:
        with self.session_factory() as s:
            return s.get(Project, project_id)

    def get_by_name(self, name: str) -> Optional[Project]:
        with self.session_factory() as s:
            row = (
                s.execute(
                    select(Project)
                    .where(Project.name == name)
                    .limit(1)
                )
                .scalars()
                .first()
            )
            return row

    def list_all(self) -> Iterable[Project]:
        with self.session_factory() as s:
            rows: List[Project] = (
                s.execute(
                    select(Project).order_by(Project.id.asc())
                )
                .scalars()
                .all()
            )
            return rows
