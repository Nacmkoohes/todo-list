# test_repository_pattern.py
def test_repository_pattern():
    project_repo = SqlAlchemyProjectRepository()
    task_repo = SqlAlchemyTaskRepository()

    # ایجاد پروژه و تسک
    project = project_repo.create("Project 1", "Description")
    task = task_repo.create(project.id, "Task 1", "Description")

    # بازیابی پروژه و تسک
    retrieved_project = project_repo.get_by_id(project.id)
    retrieved_task = task_repo.get_by_id(project.id, task.id)

    assert retrieved_project.name == "Project 1"
    assert retrieved_task.title == "Task 1"
