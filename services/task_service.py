from todo.models.task import Task
from typing import Optional
from datetime import date
from todo.config import ALLOWED_STATUSES
def _norm_status(s: str) -> str:
    return s.strip().lower()

class TaskService:
    def __init__(self):
        self.tasks = []

    def create_task(self, title: str, description: str, deadline: Optional[date] = None, status: str = "todo"):
        s = _norm_status(status)
        if s not in ALLOWED_STATUSES:
            return "Error: Task status is invalid."
        return Task(title, description, deadline=deadline, status=s)
    def list_tasks(self):
        return [task.title for task in self.tasks]

    def delete_task(self, title: str):
        task = next((t for t in self.tasks if t.title == title), None)
        if task:
            self.tasks.remove(task)
            return f"Task '{title}' deleted successfully."
        return f"Task '{title}' not found."
