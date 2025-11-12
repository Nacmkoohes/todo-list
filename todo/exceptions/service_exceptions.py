# todo/exceptions/service_exceptions.py
class ServiceError(Exception):
    """Base class for service-level errors."""

class ProjectAlreadyExists(ServiceError):
    def __init__(self, name: str):
        super().__init__(f"Project with name '{name}' already exists.")

class ProjectNotFound(ServiceError):
    def __init__(self, project_id: int):
        super().__init__(f"Project with id={project_id} not found.")

class TaskNotFound(ServiceError):
    def __init__(self, task_id: int):
        super().__init__(f"Task with id={task_id} not found.")

class InvalidStatus(ServiceError):
    def __init__(self, value: str, allowed: list[str]):
        super().__init__(f"Invalid status '{value}'. Allowed: {allowed}")
