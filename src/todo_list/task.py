from __future__ import annotations
from datetime import date
from itertools import count

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


class Task:

    def __init__(self, title, description, deadline, status="todo"):
        self.id = next(_task_ids)
        self.title = title
        self.description = description
        self.deadline = _parse_deadline(deadline)

        s = _norm_status(status)
        if s not in ALLOWED_STATUSES:
            raise ValueError("Error: Task status is invalid.")
        self.status = s

    def change_status(self, new_status):
        s = _norm_status(new_status)
        if s not in ALLOWED_STATUSES:
            return "Error: Invalid status"
        self.status = s
        return f"Task '{self.title}' status changed to '{s}'"

    def edit_task(self,new_title=None,new_description=None,new_deadline=None,new_status=None):
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


        if new_status:
            s = _norm_status(new_status)
            if s not in ALLOWED_STATUSES:
                return "Error: Task status is invalid."
            self.status = s

        return f"Task '{self.title}' updated successfully "

    def __str__(self) -> str:
        dl = self.deadline.isoformat() if self.deadline else "-"
        return f"Task Title: {self.title}, Status: {self.status}, Deadline: {dl}"
