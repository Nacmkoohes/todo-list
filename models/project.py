from datetime import datetime, timezone
from typing import Optional, List, Any
from models.task import Task  # برای type و serialization

class Project:
    def __init__(self, name: str, description: str, project_id: int, created_at: Optional[datetime] = None, tasks: Optional[List[Any]] = None):
        self.project_id = int(project_id)
        self.name = name
        self.description = description
        if isinstance(created_at, str):
            self.created_at = datetime.fromisoformat(created_at)
        else:
            self.created_at = created_at or datetime.now(timezone.utc)
        # ممکنه لیستِ dict یا Task بیاد؛ همونجا normalize نکنیم، در Service انجام می‌دیم.
        self.tasks: List[Any] = tasks or []

    def list_tasks(self):
        return self.tasks

    def add_task(self, task: Task):
        # اعتبارسنجی وضعیت و بقیه قوانین قبلاً داری
        self.tasks.append(task)
        return f"Task '{task.title}' added successfully to project '{self.name}'"

    def remove_task(self, task_title: str):
        t = next((x for x in self.tasks if getattr(x, "title", None) == task_title), None)
        if not t:
            return f"Error: Task '{task_title}' not found in project '{self.name}'"
        self.tasks.remove(t)
        return f"Task '{task_title}' removed successfully from project '{self.name}'"

    def to_dict(self) -> dict:
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            # 👇 تبدیل هر Task به dict
            "tasks": [t.to_dict() if hasattr(t, "to_dict") else t for t in self.tasks],
        }
