from services.project_service import ProjectService
from services.task_service import TaskService


def test_full_project_flow():
    # 1. ایجاد پروژه
    project_service = ProjectService()
    task_service = TaskService()

    project = project_service.create_project("Test Project", "This is a test project.")

    assert project.name == "Test Project"
    assert project.description == "This is a test project."
    assert len(project_service.projects) == 1  # فقط یک پروژه باید باشد

    # 2. ایجاد تسک
    task = task_service.create_task("Test Task", "This is a test task.", status="todo")
    project.add_task(task)

    # بررسی افزودن تسک
    assert len(project.tasks) == 1  # پروژه باید یک تسک داشته باشد
    assert project.tasks[0].title == "Test Task"  # عنوان تسک باید درست باشد

    # 3. ویرایش پروژه
    response = project_service.edit_project("Test Project", new_name="Updated Project",
                                            new_description="Updated description.")
    assert response == "Project 'Test Project' updated successfully."
    assert project.name == "Updated Project"
    assert project.description == "Updated description."

    # 4. ویرایش تسک
    response = task.edit_task(new_title="Updated Task", new_description="Updated description for task.")
    assert response == "Task 'Updated Task' updated successfully"
    assert task.title == "Updated Task"
    assert task.description == "Updated description for task."

    # 5. تغییر وضعیت تسک
    response = task.change_status("doing")
    assert response == "Task 'Updated Task' status changed to 'doing'."
    assert task.status == "doing"

    # 6. حذف تسک
    project.remove_task("Updated Task")
    assert len(project.tasks) == 0  # تسک باید حذف شده باشد

    # 7. حذف پروژه
    response = project_service.delete_project("Updated Project")
    assert response == "Project 'Updated Project' deleted successfully."
    assert len(project_service.projects) == 0  # پروژه باید حذف شده باشد

    # 8. بررسی اگر پروژه و تسک حذف شدند
    project = project_service.get_project_by_name("Updated Project")
    assert project is None  # پروژه نباید وجود داشته باشد
