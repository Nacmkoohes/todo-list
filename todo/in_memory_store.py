from __future__ import annotations
from typing import Dict, Iterable
from .repositories import Project, Task

class InMemoryProjectRepo:
    def __init__(self) -> None:
        self._projects: Dict[int, Project] = {}
        self._next_project_id: int = 1
        # per-project task counters
        self._task_seq: Dict[int, int] = {}

    def add(self, project: Project) -> Project:
        if project.id is None:
            project.id = self._next_project_id
            self._next_project_id += 1
        self._projects[project.id] = project
        # initialize task counter for this project
        self._task_seq.setdefault(project.id, 1)
        return project

    def get(self, project_id: int) -> Project:
        if project_id not in self._projects:
            raise KeyError(f"Project {project_id} not found")
        return self._projects[project_id]

    def list(self) -> Iterable[Project]:
        return list(self._projects.values())

    def save(self, project: Project) -> None:
        if project.id is None or project.id not in self._projects:
            raise KeyError(f"Project {project.id} not found")
        self._projects[project.id] = project

    def delete(self, project_id: int) -> None:
        if project_id not in self._projects:
            raise KeyError(f"Project {project_id} not found")
        del self._projects[project_id]
        self._task_seq.pop(project_id, None)

class InMemoryTaskRepo:
    def __init__(self, project_repo: InMemoryProjectRepo) -> None:
        self._projects = project_repo

    def _next_task_id(self, project_id: int) -> int:
        p = self._projects.get(project_id)
        seq = self._projects._task_seq.setdefault(project_id, 1)
        self._projects._task_seq[project_id] = seq + 1
        return seq

    def add(self, project_id: int, task: Task) -> Task:
        p = self._projects.get(project_id)
        if task.id is None:
            task.id = self._next_task_id(project_id)
        p.tasks.append(task)
        self._projects.save(p)
        return task

    def get(self, project_id: int, task_id: int) -> Task:
        p = self._projects.get(project_id)
        for t in p.tasks:
            if t.id == task_id:
                return t
        raise KeyError(f"Task {task_id} not found in project {project_id}")

    def list(self, project_id: int) -> Iterable[Task]:
        return list(self._projects.get(project_id).tasks)

    def save(self, project_id: int, task: Task) -> None:
        p = self._projects.get(project_id)
        for i, t in enumerate(p.tasks):
            if t.id == task.id:
                p.tasks[i] = task
                self._projects.save(p)
                return
        raise KeyError(f"Task {task.id} not found in project {project_id}")

    def delete(self, project_id: int, task_id: int) -> None:
        p = self._projects.get(project_id)
        new_tasks = [t for t in p.tasks if t.id != task_id]
        if len(new_tasks) == len(p.tasks):
            raise KeyError(f"Task {task_id} not found in project {project_id}")
        p.tasks = new_tasks
        self._projects.save(p)
