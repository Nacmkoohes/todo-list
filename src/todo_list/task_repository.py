# task_repository.py

class TaskRepository:
    def __init__(self):
        self.tasks = []  # برای ذخیره‌سازی تسک‌ها در حافظه

    def save(self, task):
        self.tasks.append(task)

    def get_by_project(self, project_id):
        return [task for task in self.tasks if task.project_id == project_id]

    def find_by_id(self, task_id):
        return next((task for task in self.tasks if task.id == task_id), None)

    def delete(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
