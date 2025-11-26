from __future__ import annotations

from typing import Any, Iterable, Optional, Protocol
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from todo.db.session import SessionLocal
from todo.models.task import Task


class TaskRepository(Protocol):
    """Abstraction for task persistence layer."""

    def create(
        self,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        deadline: Optional[datetime] = None,
    ) -> Task: ...

    def update(self, task_id: int, **fields: Any) -> Task: ...
    def delete(self, task_id: int) -> None: ...
    def get_by_id(self, task_id: int) -> Optional[Task]: ...
    def list_by_project(self, project_id: int) -> Iterable[Task]: ...
    def list_overdue_open(self) -> Iterable[Task]: ...


class SqlAlchemyTaskRepository(TaskRepository):
    """SQLAlchemy implementation of TaskRepository."""

    def __init__(self, session_factory=SessionLocal) -> None:
        self.session_factory = session_factory

    def create(
        self,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        deadline: Optional[datetime] = None,
    ) -> Task:
        with self.session_factory() as s:  # type: Session
            task = Task(
                project_id=project_id,
                title=title,
                description=description,
                deadline=deadline,
            )
            s.add(task)
            s.commit()
            s.refresh(task)
            return task

    def update(self, task_id: int, **fields: Any) -> Task:
        with self.session_factory() as s:
            task = s.get(Task, task_id)
            if task is None:
                raise LookupError(f"Task #{task_id} not found")

            for key, value in fields.items():
                if value is not None:
                    setattr(task, key, value)

            s.commit()
            s.refresh(task)
            return task

    def delete(self, task_id: int) -> None:
        with self.session_factory() as s:
            task = s.get(Task, task_id)
            if task is None:
                return
            s.delete(task)
            s.commit()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        with self.session_factory() as s:
            return s.get(Task, task_id)

    def list_by_project(self, project_id: int) -> Iterable[Task]:
        with self.session_factory() as s:
            rows = (
                s.execute(
                    select(Task)
                    .where(Task.project_id == project_id)
                    .order_by(Task.id.asc())
                )
                .scalars()
                .all()
            )
            return rows

    def list_overdue_open(self) -> Iterable[Task]:
        now = datetime.now(timezone.utc)
        with self.session_factory() as s:
            rows = (
                s.execute(
                    select(Task)
                    .where(Task.deadline != None)  # noqa: E711
                    .where(Task.deadline < now)
                    .where(Task.status != "done")
                    .order_by(Task.deadline.asc())
                )
                .scalars()
                .all()
            )
            return rows
