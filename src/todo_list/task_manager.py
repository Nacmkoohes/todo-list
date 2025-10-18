from __future__ import annotations
from todo_list.config import  MAX_NUMBER_OF_TASKS
from todo_list.task import Task

from exceptions import TaskNotFoundError, InvalidStatusError, TaskLimitReachedError,ProjectNotFoundError


class TaskManager:
    def __init__(self, repository):
        self.repository = repository

    def create_task(self, project_id, title, description, deadline, status="todo"):
        if len(self.repository.get_by_project(project_id)) >= MAX_NUMBER_OF_TASKS:
            raise TaskLimitReachedError()  # استفاده از استثنا

        new_task = Task(title, description, deadline, status)
        project = self.repository.find_by_id(project_id)

        if not project:
            raise ProjectNotFoundError()

        project.add_task(new_task)
        self.repository.save(new_task)
        return new_task

    def update_task_status(self, task_id, new_status):
        valid_statuses = ["todo", "doing", "done"]
        if new_status not in valid_statuses:
            raise InvalidStatusError()

        task = self.repository.find_by_id(task_id)
        if not task:
            raise TaskNotFoundError()

        task.change_status(new_status)
        return task

    def edit_task(self, task_id, new_title=None, new_description=None, new_deadline=None, new_status=None):
        task = self.repository.find_by_id(task_id)
        if task:
            task.edit_task(new_title, new_description, new_deadline, new_status)
            return task
        return None

    def delete_task(self, task_id):
        task = self.repository.find_by_id(task_id)
        if task:
            self.repository.delete(task_id)
            return task
        return None

    def list_tasks(self, project_id):

        project = self.repository.find_by_id(project_id)
        if project:
            return project.list_tasks()
        return []

