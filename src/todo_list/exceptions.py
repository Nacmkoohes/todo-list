# exceptions.py

class ProjectNotFoundError(Exception):
    """Raised when a project is not found."""
    def __init__(self, message="Project not found"):
        self.message = message
        super().__init__(self.message)

class TaskNotFoundError(Exception):
    """Raised when a task is not found."""
    def __init__(self, message="Task not found"):
        self.message = message
        super().__init__(self.message)

class InvalidStatusError(Exception):
    """Raised when a task's status is invalid."""
    def __init__(self, message="Invalid task status provided"):
        self.message = message
        super().__init__(self.message)

class TaskLimitReachedError(Exception):
    """Raised when the maximum number of tasks for a project is reached."""
    def __init__(self, message="Cannot add more tasks, limit reached"):
        self.message = message
        super().__init__(self.message)
