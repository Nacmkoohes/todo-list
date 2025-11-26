from __future__ import annotations

from typing import Iterable, Optional
from datetime import datetime, timezone

from todo.config import MAX_NUMBER_OF_TASKS, ALLOWED_STATUSES
from todo.models.task import Task
from todo.repositories.project_repository import ProjectRepository
from todo.repositories.task_repository import TaskRepository


class TaskService:
    """Application service for managing tasks."""

    def __init__(
        self,
        project_repo: ProjectRepository,
        task_repo: TaskRepository,
    ) -> None:
        self.project_repo = project_repo
        self.task_repo = task_repo

    def _ensure_project_exists(self, project_id: int) -> None:
        if self.project_repo.get_by_id(project_id) is None:
            raise LookupError(f"Project #{project_id} not found")

    def list_tasks(self, project_id: int) -> Iterable[Task]:
        self._ensure_project_exists(project_id)
        return self.task_repo.list_by_project(project_id)

    def create_task(
        self,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        deadline: Optional[datetime] = None,
    ) -> Task:
        self._ensure_project_exists(project_id)

        existing_tasks = list(self.task_repo.list_by_project(project_id))
        if len(existing_tasks) >= MAX_NUMBER_OF_TASKS:
            raise ValueError("Maximum number of tasks for this project reached")

        task = self.task_repo.create(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )
        return task

    def get_task(self, project_id: int, task_id: int) -> Optional[Task]:
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            return None
        if task.project_id != project_id:
            # Do not leak that task exists in a different project
            return None
        return task

    def update_task(self, project_id: int, task_id: int, **fields) -> Task:
        task = self.get_task(project_id, task_id)
        if task is None:
            raise LookupError(f"Task #{task_id} not found in project #{project_id}")

        status = fields.get("status")
        if status is not None and status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {status!r}")

        # Auto-manage closed_at when status changes
        if status is not None:
            now = datetime.now(timezone.utc)
            if status == "done":
                fields.setdefault("closed_at", now)
            else:
                # If moved away from done, clear closed_at
                fields.setdefault("closed_at", None)

        updated = self.task_repo.update(task_id, **fields)
        return updated

    def delete_task(self, project_id: int, task_id: int) -> None:
        # Optional: ensure task belongs to project
        task = self.get_task(project_id, task_id)
        if task is None:
            # idempotent delete: silently ignore
            return
        self.task_repo.delete(task_id)

    def list_overdue_open(self) -> Iterable[Task]:
        """Return all overdue and still open tasks."""
        return self.task_repo.list_overdue_open()

    def autoclose_overdue_tasks(self) -> int:
        """Example method: automatically close overdue tasks."""
        overdue = list(self.task_repo.list_overdue_open())
        count = 0
        now = datetime.now(timezone.utc)
        for t in overdue:
            self.task_repo.update(
                t.id,
                status="done",
                closed_at=now,
            )
            count += 1
        return count
