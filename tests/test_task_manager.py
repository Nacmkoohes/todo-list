# tests/test_task_manager.py
import pytest
from todo_list.task_manager import TaskManager
from todo_list.task_repository import TaskRepository
from todo_list.project_manager import ProjectManager
from todo_list.project_repository import ProjectRepository


@pytest.fixture
def task_manager():
    """Fixture for TaskManager"""
    task_repo = TaskRepository()
    return TaskManager(task_repo)


@pytest.fixture
def project_manager():
    """Fixture for ProjectManager"""
    project_repo = ProjectRepository()
    return ProjectManager(project_repo)


def test_create_task(task_manager, project_manager):
    """Test creating a task for a project"""
    project_manager.create_project("Test Project", "This is a test project.")
    project = project_manager.projects[0]
    result = task_manager.create_task(project.id, "Test Task", "Task description", "2023-12-31")
    assert result == "Task added: Task: Test Task, Status: todo, Deadline: 2023-12-31"
    assert len(project.tasks) == 1


def test_update_task_status(task_manager, project_manager):
    """Test updating the status of a task"""
    project_manager.create_project("Test Project", "This is a test project.")
    project = project_manager.projects[0]
    task_manager.create_task(project.id, "Test Task", "Task description", "2023-12-31")
    task = project.tasks[0]
    result = task_manager.update_task_status(task.id, "doing")
    assert task.status == "doing"
    assert result == f"Task: {task.title} status updated to 'doing'"


def test_delete_task(task_manager, project_manager):
    """Test deleting a task"""
    project_manager.create_project("Test Project", "This is a test project.")
    project = project_manager.projects[0]
    task_manager.create_task(project.id, "Test Task", "Task description", "2023-12-31")
    task = project.tasks[0]
    result = task_manager.delete_task(task.id)
    assert result == f"Task: {task.title} deleted successfully"
    assert len(project.tasks) == 0
