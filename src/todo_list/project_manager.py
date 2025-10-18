# project_manager.py
from todo_list.project import Project
from typing import Optional

MAX_NUMBER_OF_PROJECTS = 5  # Maximum number of projects

# Helper function to normalize project name (convert to lowercase and remove extra spaces)
def _key(name: str) -> str:
    return name.strip().lower()

class ProjectManager:
    def __init__(self, project_repository):
        self.project_repository = project_repository
        self.projects = []
        self._by_name = {}

    def create_project(self, name: str, description: str) -> str:
        name_s = name.strip()
        desc_s = description.strip()

        # Validate project name and description length
        if len(name_s.split()) > 30:
            return "Error: Project's name must be <= 30 words."
        if len(desc_s.split()) > 150:
            return "Error: Project's description must be <= 150 words."

        # Check if the project name already exists
        if _key(name_s) in self._by_name:
            return "Error: Project name already exists."

        # Check if the number of projects exceeds the maximum allowed
        if len(self.projects) >= MAX_NUMBER_OF_PROJECTS:
            return "Error: Maximum number of projects reached."

        # Create a new project
        new_project = Project(name_s, desc_s)
        self.projects.append(new_project)  # Add project to the list
        self._by_name[_key(name_s)] = new_project  # Add project to the dictionary by normalized name

        return "Project created successfully."

    def edit_project(self, old_name: str, new_name: str, new_description: str) -> str:
        # Find the project by its current name
        project = self._by_name.get(_key(old_name))
        if not project:
            return "Error: Project does not exist."

        # Validate new project name and description length
        new_name_s = new_name.strip()
        new_desc_s = new_description.strip()

        if len(new_name_s.split()) > 30:
            return "Error: Project's name must be <= 30 words."
        if len(new_desc_s.split()) > 150:
            return "Error: Project's description must be <= 150 words."

        # Check if new name is taken by another project
        new_key = _key(new_name_s)
        if new_key in self._by_name and self._by_name[new_key] is not project:
            return "Error: Project name already exists."

        # If the project name and description are the same, no changes are made
        if project.name == new_name_s and project.description == new_desc_s:
            return "Error: No changes detected."

        # Update the project
        old = project.name
        project.name = new_name_s
        project.description = new_desc_s

        # Remove the old project name from the dictionary and add the new one
        old_key = _key(old)
        if old_key in self._by_name:
            del self._by_name[old_key]
        self._by_name[new_key] = project

        return f"Project '{old}' updated successfully to '{project.name}'"

    def delete_project(self, name: str) -> str:
        name_s = name.strip()
        project = self._by_name.get(_key(name_s))
        if not project:
            return "Error: Project not found."

        # Remove the project from the list and clear its tasks
        self.projects.remove(project)
        project.tasks.clear()  # Cascade delete tasks
        self._by_name.pop(_key(name_s), None)  # Remove from dictionary

        return f"Project '{name_s}' and all its tasks have been deleted successfully."

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        return next((p for p in self.projects if p.id == project_id), None)

    def get_project_by_name(self, name: str) -> Optional[Project]:
        """Get project by name"""
        return self._by_name.get(_key(name))

    def delete_project_by_id(self, project_id: int) -> str:
        """Delete project by ID"""
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found."

        # Remove the project and cascade delete tasks
        self.projects.remove(project)
        project.tasks.clear()  # Cascade delete tasks
        self._by_name.pop(_key(project.name), None)

        return f"Project #{project_id} and all its tasks have been deleted successfully."

    def list_tasks_by_project_id(self, project_id: int) -> list[str] | str:
        """List tasks of a project by project ID"""
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found."
        return project.list_tasks()

    def list_projects(self) -> list[str] | str:
        """List all projects"""
        if not self.projects:
            return "Error: No projects found."
        sorted_projects = sorted(self.projects, key=lambda p: p.created_at, reverse=True)
        return [str(p) for p in sorted_projects]
