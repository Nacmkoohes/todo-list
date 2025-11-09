from __future__ import annotations
from typing import Iterable, Optional
from ..config import MAX_NUMBER_OF_TASKS, ALLOWED_STATUSES
from ..repositories import Task

class TaskService:
    def __init__(self, task_store=None, project_store=None) -> None:
        if task_store is None:
            from ..in_memory_store import InMemoryProjectRepo, InMemoryTaskRepo
            if project_store is None:
                project_store = InMemoryProjectRepo()
            task_store = InMemoryTaskRepo(project_store)
        self.task_store = task_store

    def _to_int(self, value) -> int:
        if isinstance(value, int):
            return value
        return int(str(value).strip())

    # 5) Add Task
    def add_task(self, project_id, title: str, description: str = "") -> Task:
        pid = self._to_int(project_id)
        if len(list(self.task_store.list(pid))) >= MAX_NUMBER_OF_TASKS:
            raise ValueError(f"Error: Maximum number of tasks reached (limit={MAX_NUMBER_OF_TASKS}).")
        return self.task_store.add(pid, Task(title=title.strip(), description=description.strip()))

    # 6) List Tasks
    def list_tasks(self, project_id) -> Iterable[Task]:
        return self.task_store.list(self._to_int(project_id))

    # 7) Change Status
    def change_status(self, project_id, task_id, new_status: str) -> Task:
        pid, tid = self._to_int(project_id), self._to_int(task_id)
        if new_status not in ALLOWED_STATUSES:
            raise ValueError(f"Error: status must be one of {ALLOWED_STATUSES}")
        t = self.task_store.get(pid, tid)
        t.status = new_status
        self.task_store.save(pid, t)
        return t

    # 8) Edit Task
    def edit_task(self, project_id, task_id, *,
                  title: Optional[str] = None,
                  description: Optional[str] = None,
                  status: Optional[str] = None) -> Task:
        pid, tid = self._to_int(project_id), self._to_int(task_id)
        t = self.task_store.get(pid, tid)
        if title is not None:
            t.title = title.strip()
        if description is not None:
            t.description = description.strip()
        if status is not None:
            if status not in ALLOWED_STATUSES:
                raise ValueError(f"Error: status must be one of {ALLOWED_STATUSES}")
            t.status = status
        self.task_store.save(pid, t)
        return t

    # 9) Delete Task
    def delete_task(self, project_id, task_id) -> None:
        pid, tid = self._to_int(project_id), self._to_int(task_id)
        self.task_store.delete(pid, tid)
