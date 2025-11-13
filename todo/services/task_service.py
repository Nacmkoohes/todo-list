# todo/services/task_service.py
from __future__ import annotations

from typing import Optional
from datetime import datetime, timezone

from todo.config import ALLOWED_STATUSES
from todo.exceptions.service_exceptions import (
    ProjectNotFound,
    TaskNotFound,
    InvalidStatus,
)
from todo.repositories.project_repository import ProjectRepository
from todo.repositories.task_repository import TaskRepository


def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Accepts 'YYYY-MM-DD' (or empty/None) and returns tz-aware datetime at 00:00 UTC."""
    if not date_str:
        return None
    try:
        # allow YYYY-MM-DD or full ISO; normalize to UTC midnight if only date
        if len(date_str) == 10:
            dt = datetime.fromisoformat(date_str)  # naive date
            return dt.replace(tzinfo=timezone.utc)
        dt = datetime.fromisoformat(date_str)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        raise ValueError("Invalid deadline format. Use YYYY-MM-DD (e.g., 2025-12-01).")


class TaskService:
    """
    Business logic for Task use-cases.
    Note: repositories are injected (DI) — no SQLAlchemy/session here.
    """

    def __init__(self, project_store: ProjectRepository, task_store: TaskRepository) -> None:
        self.project_store = project_store
        self.task_store = task_store

    # --- Use case 5: Add Task ---
    def add_task(
        self,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        deadline: Optional[str] = None,  # CLI passes string; we'll parse
        status: Optional[str] = None,     # optional; default "todo"
    ):
        # 1) project must exist
        if not self.project_store.get_by_id(project_id):
            raise ProjectNotFound(f"Project #{project_id} not found.")

        # 2) title validation
        title = (title or "").strip()
        if not title:
            raise ValueError("Title cannot be empty.")

        # 3) status normalize/validate
        st = (status or "todo").strip().lower()
        if st not in ALLOWED_STATUSES:
            raise InvalidStatus(f"Status must be one of: {', '.join(ALLOWED_STATUSES)}")

        # 4) parse deadline
        deadline_dt = _parse_date(deadline)

        # 5) create task (repo.create doesn't take status → model default = 'todo')
        t = self.task_store.create(project_id, title, description, deadline_dt)

        # 6) if desired status != default, update it
        if st != "todo":
            t = self.task_store.update(t.id, status=st)

        return t

    # --- Use case 6: Edit Task ---
    def edit_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[str] = None,
    ):
        t = self.task_store.get_by_id(task_id)
        if not t:
            raise TaskNotFound(f"Task #{task_id} not found.")

        updates = {}
        if title is not None:
            title = title.strip()
            if title == "":
                raise ValueError("Title cannot be empty.")
            updates["title"] = title
        if description is not None:
            updates["description"] = description or None
        if deadline is not None:
            updates["deadline"] = _parse_date(deadline)

        if not updates:
            return t
        return self.task_store.update(task_id, **updates)

    # --- Use case 7: Delete Task ---
    def delete_task(self, task_id: int) -> None:
        t = self.task_store.get_by_id(task_id)
        if not t:
            raise TaskNotFound(f"Task #{task_id} not found.")
        self.task_store.delete(task_id)

    # --- Use case 8: List Tasks by Project ---
    def list_tasks_by_project(self, project_id: int):
        if not self.project_store.get_by_id(project_id):
            raise ProjectNotFound(f"Project #{project_id} not found.")
        return self.task_store.list_by_project(project_id)

    # --- Use case 9: Change Task Status ---
    def change_task_status(self, task_id: int, new_status: str):
        t = self.task_store.get_by_id(task_id)
        if not t:
            raise TaskNotFound(f"Task #{task_id} not found.")
        st = (new_status or "").strip().lower()
        if st not in ALLOWED_STATUSES:
            raise InvalidStatus(f"Status must be one of: {', '.join(ALLOWED_STATUSES)}")
        return self.task_store.update(task_id, status=st)

    # --- Command: Autoclose overdue (used by scheduled job) ---
    def autoclose_overdue(self, now: Optional[datetime] = None) -> int:
        """Set status=done and closed_at=now for overdue tasks that are not done."""
        now = now or datetime.now(timezone.utc)
        count = 0
        for t in self.task_store.list_overdue_open():
            self.task_store.update(t.id, status="done", closed_at=now)
            count += 1
        return count
