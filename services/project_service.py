# services/project_service.py
import json
from datetime import datetime
from typing import Optional, List
from todo.models.project import Project
from todo.models.task import Task

class ProjectService:

    def __init__(self, file_name: Optional[str] = None):
        self.file_name = file_name
        self.projects: List[Project] = self._load_projects()

    def _load_projects(self) -> List[Project]:
        if not self.file_name:
            return []

        try:
            with open(self.file_name, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        projects: List[Project] = []
        max_seen = 0
        for p in data:
            if "project_id" in p:
                pid = int(p["project_id"])
            elif "id" in p:
                pid = int(p.pop("id"))
                p["project_id"] = pid
            else:
                pid = 0
                p["project_id"] = pid

            created_at = p.get("created_at")
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at)
                except Exception:
                    created_at = None

            raw_tasks = p.get("tasks", [])
            tasks: List[Task] = []
            for item in raw_tasks:
                if isinstance(item, dict) and hasattr(Task, "from_dict"):
                    tasks.append(Task.from_dict(item))
                else:
                    tasks.append(item)

            proj = Project(
                name=p.get("name", ""),
                description=p.get("description", ""),
                project_id=pid if pid > 0 else 0,
                created_at=created_at,
                tasks=tasks,
            )
            projects.append(proj)
            if pid > max_seen:
                max_seen = pid

        # اگر پروژه‌ای بدون id بود بهش id بدهیم
        next_id = max_seen + 1 if max_seen > 0 else 1
        for proj in projects:
            if getattr(proj, "project_id", 0) == 0:
                proj.project_id = next_id
                next_id += 1

        return projects

    def save_projects(self) -> None:
        if not self.file_name:
            return
        with open(self.file_name, "w") as f:
            payload = [p.to_dict() if hasattr(p, "to_dict") else p.__dict__ for p in self.projects]
            for item in payload:
                if isinstance(item.get("created_at"), datetime):
                    item["created_at"] = item["created_at"].isoformat()
            json.dump(payload, f, indent=4)

    # ---------- API ----------
    def create_project(self, name: str, description: str) -> Project:
        next_id = 1 + max((getattr(p, "project_id", 0) for p in self.projects), default=0)
        project = Project(name=name, description=description, project_id=next_id)
        self.projects.append(project)
        self.save_projects()
        return project

    def list_projects(self) -> List[Project]:
        return self.projects

    def get_project_by_name(self, name: str) -> Optional[Project]:
        return next((p for p in self.projects if p.name == name), None)

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        return next((p for p in self.projects if getattr(p, "project_id", None) == project_id), None)

    def edit_project(self, name: str, new_name: Optional[str] = None, new_description: Optional[str] = None) -> str:
        project = self.get_project_by_name(name)
        if not project:
            return f"Project '{name}' not found."
        if new_name:
            project.name = new_name
        if new_description:
            project.description = new_description
        self.save_projects()
        return f"Project '{name}' updated successfully."

    def delete_project(self, name: str) -> str:
        project = self.get_project_by_name(name)
        if not project:
            return f"Project '{name}' not found."
        self.projects.remove(project)
        self.save_projects()
        return f"Project '{name}' deleted successfully."
