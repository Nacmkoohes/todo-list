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
        """Ensures that the project exists in the repository."""
        if self.project_repo.get_by_id(project_id) is None:
            raise LookupError(f"Project #{project_id} not found")

    def list_tasks(self, project_id: int) -> Iterable[Task]:
        """Returns a list of tasks for a given project."""
        self._ensure_project_exists(project_id)
        return self.task_repo.list_by_project(project_id)

    def create_task(
        self,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        deadline: Optional[datetime] = None,
    ) -> Task:
        """Creates a task for the given project."""
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
        """Retrieves a task by its ID and ensures it's from the correct project."""
        task = self.task_repo.get_by_id(task_id)
        if task is None or task.project_id != project_id:
            return None
        return task

    def update_task(self, project_id: int, task_id: int, **fields) -> Task:
        """Updates a task's attributes."""
        task = self.get_task(project_id, task_id)
        if task is None:
            raise LookupError(f"Task #{task_id} not found in project #{project_id}")

        status = fields.get("status")
        if status is not None and status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {status!r}")

        # Auto-manage closed_at when status changes
        if status == "done" and "closed_at" not in fields:
            fields["closed_at"] = datetime.now(timezone.utc)

        updated_task = self.task_repo.update(task_id, **fields)
        return updated_task

    def delete_task(self, project_id: int, task_id: int) -> None:
        """Deletes a task from the project."""
        task = self.get_task(project_id, task_id)
        if task is None:
            return  # Task does not exist, no need to delete
        self.task_repo.delete(task_id)

    def list_overdue_open(self) -> Iterable[Task]:
        """Returns all overdue and still open tasks."""
        return self.task_repo.list_overdue_open()

    def autoclose_overdue_tasks(self) -> int:
        """Automatically closes overdue tasks."""
        overdue = list(self.task_repo.list_overdue_open())
        count = 0
        now = datetime.now(timezone.utc)
        for t in overdue:
            # Ensure status is set to "done" and closed_at is set
            self.update_task(
                project_id=t.project_id,
                task_id=t.id,
                status="done",
                closed_at=now,
            )
            count += 1
        return count

    def update_task_status(self, task_id: int, status: str, closed_at: Optional[datetime] = None) -> Task:
        """Updates the status of a task."""
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise LookupError(f"Task #{task_id} not found")

        if status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status: {status!r}")

        # Auto-manage closed_at when status changes
        if status == "done" and closed_at is None:
            closed_at = datetime.now(timezone.utc)

        updated_task = self.task_repo.update(
            task_id=task.id,
            status=status,
            closed_at=closed_at
        )
        return updated_task
