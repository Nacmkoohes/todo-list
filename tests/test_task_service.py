from services.task_service import TaskService
from services.project_service import ProjectService


def test_add_task():
    project_service = ProjectService()
    task_service = TaskService()

    project = project_service.create_project("Test Project", "This is a test project.")
    task = task_service.create_task("Test Task", "This is a test task.")

    project.add_task(task)

    assert len(project.tasks) == 1
    assert project.tasks[0].title == "Test Task"


def test_edit_task():
    project_service = ProjectService()
    task_service = TaskService()

    project = project_service.create_project("Test Project", "This is a test project.")
    task = task_service.create_task("Test Task", "This is a test task.")

    project.add_task(task)
    response = task.edit_task(new_title="Updated Task", new_description="Updated description.")

    assert response == "Task 'Updated Task' updated successfully"
    assert task.title == "Updated Task"
    assert task.description == "Updated description."
