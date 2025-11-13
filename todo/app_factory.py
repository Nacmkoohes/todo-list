from todo.repositories.project_repository import SqlAlchemyProjectRepository
from todo.repositories.task_repository import SqlAlchemyTaskRepository
from todo.services.project_service import ProjectService
from todo.services.task_service import TaskService

def build_services():
    proj_repo = SqlAlchemyProjectRepository()
    task_repo = SqlAlchemyTaskRepository()
    ps = ProjectService(proj_repo, task_repo)
    ts = TaskService(proj_repo, task_repo)
    return ps, ts
