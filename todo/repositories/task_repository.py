from __future__ import annotations
from typing import Protocol, Callable, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from todo.models.task import Task

class TaskRepository(Protocol):
    def create(
        self,
        project_id: int,
        title: str,
        description: str = "",
        status: str = "todo",
        deadline: datetime | None = None,
    ) -> Task: ...
    def get(self, task_id: int) -> Optional[Task]: ...
    def list_by_project(self, project_id: int) -> List[Task]: ...
    def update(self, task: Task) -> None: ...
    def delete(self, task_id: int) -> bool: ...

class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def create(
        self,
        project_id: int,
        title: str,
        description: str = "",
        status: str = "todo",
        deadline: datetime | None = None,
    ) -> Task:
        with self._session_factory() as s:
            t = Task(
                project_id=project_id,
                title=title.strip(),
                description=description or "",
                status=status,
                deadline=deadline,
            )
            s.add(t)
            s.commit()
            s.refresh(t)
            return t

    def get(self, task_id: int) -> Optional[Task]:
        with self._session_factory() as s:
            return s.get(Task, task_id)

    def list_by_project(self, project_id: int) -> List[Task]:
        with self._session_factory() as s:
            stmt = select(Task).where(Task.project_id == project_id).order_by(Task.id.asc())
            return list(s.scalars(stmt))

    def update(self, task: Task) -> None:
        with self._session_factory() as s:
            s.merge(task)
            s.commit()

    def delete(self, task_id: int) -> bool:
        with self._session_factory() as s:
            obj = s.get(Task, task_id)
            if not obj:
                return False
            s.delete(obj)
            s.commit()
            return True
