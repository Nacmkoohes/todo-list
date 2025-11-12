# todo/app_factory.py
"""
Build and wire services with their repositories (DB-backed).
CLI یا هر لایه‌ی دیگری فقط این تابع رو صدا می‌زند.
"""

from todo.db.session import SessionLocal
from todo.repositories.project_repository import SqlAlchemyProjectRepository
from todo.repositories.task_repository import SqlAlchemyTaskRepository
from todo.services.project_service import ProjectService
from todo.services.task_service import TaskService


def build_services():
    """Return (project_service, task_service) wired to SQLAlchemy repos."""
    project_repo = SqlAlchemyProjectRepository(SessionLocal)
    task_repo = SqlAlchemyTaskRepository(SessionLocal)

    project_service = ProjectService(project_repo)
    task_service = TaskService(task_repo, project_repo)

    return project_service, task_service
