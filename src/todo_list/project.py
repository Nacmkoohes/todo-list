from __future__ import annotations
from todo_list.config import  MAX_NUMBER_OF_TASKS
from datetime import date
from datetime import datetime,timezone
from itertools import count
from todo_list.task import Task


_project_ids = count(1)
_task_ids = count(1)


ALLOWED_STATUSES = {"todo", "doing", "done"}

def _norm_status(s: str) -> str:
    return s.strip().lower()

def _key(name: str) -> str:
    return name.strip().lower()


def _parse_deadline(d):
    if d in (None, "", " ", "null"):
        return None
    if isinstance(d, date):
        return d
    try:
        return date.fromisoformat(str(d).strip())
    except Exception:
        raise ValueError("Error: Deadline must be in YYYY-MM-DD format.")


class Project:

    def __init__(self,name,description):
        self.id = next(_project_ids)
        self.name = name
        self.description = description
        self.tasks :list[Task] = []
        self.created_at = datetime.now(timezone.utc)

    def add_task(self,task):
        if len(self.tasks)>= MAX_NUMBER_OF_TASKS:
            return "Error: Maximum number of tasks reached."
        if len(task.title.split())>30:
            return "Error: Task name is too long."
        if len(task.description.split())>150:
            return "Error: Task description is too long."

        s = _norm_status(task.status)
        if s not in ALLOWED_STATUSES:
            return "Error: Task status is invalid."
        task.status = s

        self.tasks.append(task)
        return f"Task '{task.title}' added successfully to project '{self.name}'"

    def remove_task(self, task_title):
        task = next((t for t in self.tasks if t.title == task_title), None)
        if not task:
            return f"Error: Task '{task_title}' not found in project '{self.name}'"

        self.tasks.remove(task)
        return f"Task '{task_title}' removed successfully from project '{self.name}'"

    def list_tasks(self):
        if not self.tasks:
            return f"Error: No tasks found in project '{self.name}'"
        return [
            f"ID: {t.id} | Title: {t.title}, Status: {t.status}, Deadline: {t.deadline.isoformat() if t.deadline else '-'}"
            for t in self.tasks
        ]

    def get_task_by_id(self, task_id: int):
        return next((t for t in self.tasks if t.id == task_id), None)

    def remove_task_by_id(self, task_id: int):
        task = self.get_task_by_id(task_id)
        if not task:
            return f"Error: Task #{task_id} not found in project '{self.name}'"
        self.tasks.remove(task)
        return f"Task #{task_id} removed successfully from project '{self.name}'"

    def __str__(self):
        tasks_str = ", ".join(
            f"#{t.id} {t.title} ({t.status}, {t.deadline.isoformat() if t.deadline else '-'})"
            for t in self.tasks
        )
        return f"#{self.id}|Project Name: {self.name} | Tasks: [{tasks_str}] | Description: {self.description}"

