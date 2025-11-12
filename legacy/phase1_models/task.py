from datetime import date
from typing import Optional
from config import ALLOWED_STATUSES

def _norm_status(s: str) -> str:
    return (s or "").strip().lower()

def _parse_deadline(d):
    if d in (None, "", " ", "null"):
        return None
    if isinstance(d, date):
            return d
    try:
        return date.fromisoformat(str(d).strip())
    except Exception:
        raise ValueError("Error: Deadline must be in YYYY-MM-DD format.")

class Task:
    _next_id = 1

    @classmethod
    def _sync_next_id(cls, seen_id: int):
        if seen_id >= cls._next_id:
            cls._next_id = seen_id + 1

    def __init__(
        self,
        title: str,
        description: str,
        deadline: Optional[date] = None,
        status: str = "todo",
        id: Optional[int] = None,
        task_id: Optional[int] = None
    ):
        self.id = id if id is not None else (task_id if task_id is not None else Task._next_id)
        Task._sync_next_id(self.id)
        self.title = title
        self.description = description
        self.deadline = _parse_deadline(deadline)
        s = _norm_status(status)
        self.status = s if s in ALLOWED_STATUSES else "todo"

    def change_status(self, new_status: str):
        s = _norm_status(new_status)
        if s not in ALLOWED_STATUSES:
            return "Error: Task status is invalid."
        self.status = s
        return f"Task '{self.title}' status changed to '{s}'."

    def edit_task(self, new_title=None, new_description=None, new_deadline=None, new_status=None):
        if new_title:
            if len(new_title.split()) > 30:
                return "Error: Task title must be <= 30 words."
            self.title = new_title
        if new_description:
            if len(new_description.split()) > 150:
                return "Error: Task description must be <= 150 words."
            self.description = new_description
        if new_deadline is not None:
            try:
                self.deadline = _parse_deadline(new_deadline)
            except ValueError as e:
                return str(e)
        if new_status is not None:
            s = _norm_status(new_status)
            if s not in ALLOWED_STATUSES:
                return "Error: Task status is invalid."
            self.status = s
        return f"Task '{self.title}' updated successfully"

    # Serialization
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        return cls(
            title=d.get("title", ""),
            description=d.get("description", ""),
            deadline=d.get("deadline"),
            status=d.get("status", "todo"),
            id=d.get("id"),
            task_id=d.get("task_id"),
        )
