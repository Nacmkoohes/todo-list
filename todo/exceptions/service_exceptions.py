# todo/exceptions/service_exceptions.py
class ProjectAlreadyExists(Exception):
    """Raised when trying to create/rename a project to a duplicate name."""
    pass


class ProjectNotFound(Exception):
    """Raised when the target project doesn't exist."""
    pass


class TaskNotFound(Exception):
    """Raised when the target task doesn't exist."""
    pass


class InvalidStatus(Exception):
    """Raised when a task status isn't within allowed statuses."""
    pass
