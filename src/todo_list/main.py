from __future__ import annotations
from todo_list.config import MAX_NUMBER_OF_PROJECTS, MAX_NUMBER_OF_TASKS
from datetime import date
from datetime import datetime,timezone
from itertools import count
from typing import Optional

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


class ManageProject:


    def __init__(self)->None:
        self.projects : list[Project]=[]
        self._by_name: dict[str, Project] = {}

    def create_project(self, name: str, description: str) -> str:
        name_s = name.strip()
        desc_s = description.strip()

        if len(name_s.split()) > 30:
            return "Error: Project's name must be <= 30 words."
        if len(desc_s.split()) > 150:
            return "Error: Project's description must be <= 150 words."

        if _key(name_s) in self._by_name:
            return "Error: Project name already exists."

        if len(self.projects) >= MAX_NUMBER_OF_PROJECTS:
            return "Error: Maximum number of projects reached."

        new_project = Project(name_s, desc_s)
        self.projects.append(new_project)
        self._by_name[_key(name_s)] = new_project
        return "Project created successfully."

    def edit_project(self, old_name: str, new_name: str, new_description: str) -> str:
        project = self._by_name.get(_key(old_name))
        if not project:
            return "Error: Project does not exist."

        new_name_s = new_name.strip()
        new_desc_s = new_description.strip()

        if len(new_name_s.split()) > 30:
            return "Error: Project's name must be <= 30 words."
        if len(new_desc_s.split()) > 150:
            return "Error: Project's description must be <= 150 words."

        new_key = _key(new_name_s)
        if new_key in self._by_name and self._by_name[new_key] is not project:
            return "Error: Project name already exists."

        if project.name == new_name_s and project.description == new_desc_s:
            return "Error: No changes detected."

        old = project.name
        project.name = new_name_s
        project.description = new_desc_s
        old_key = _key(old)
        if old_key  in self._by_name:
            del self._by_name[old_key]
        self._by_name[new_key] = project
        return f"Project '{old}' updated successfully to '{project.name}'"

    def delete_project(self, name: str) -> str:
        name_s = name.strip()
        project = next((p for p in self.projects if p.name.strip() == name_s), None)
        if not project:
            return "Error: Project not found."

        self.projects.remove(project)
        #Cascade Delete
        project.tasks.clear()
        return f"Project '{name}' and all it's tasks have been deleted successfully."

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return next((p for p in self.projects if p.id == project_id), None)

    def delete_project_by_id(self, project_id: int) -> str:
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found."
        self.projects.remove(project)
        project.tasks.clear()  # cascade
        return f"Project #{project_id} and all it's tasks have been deleted successfully."

    def list_tasks_by_project_id(self, project_id: int)->list[str]|str:
        p = self.get_project_by_id(project_id)
        if not p:
            return "Error: Project not found."
        return p.list_tasks()
    def list_projects(self) -> list[str] | str:
        if not self.projects:
            return "Error: No projects found."
        sorted_projects = sorted(self.projects, key=lambda p: p.created_at, reverse=True)
        return [str(p) for p in sorted_projects]


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

