import pytest
from todo_list.project_manager import ProjectManager
from todo_list.project_repository import ProjectRepository

@pytest.fixture
def project_manager():
    """Fixture for ProjectManager"""
    project_repo = ProjectRepository()
    return ProjectManager(project_repo)


def test_create_project(project_manager):
    """Test creating a project"""
    result = project_manager.create_project("Test Project", "This is a test project.")
    assert result == "Project created successfully."
    assert len(project_manager.projects) == 1
    assert project_manager.projects[0].name == "Test Project"


def test_create_project_with_long_name(project_manager):
    """Test creating a project with a name longer than 30 words"""
    long_name = " ".join(["word"] * 31)
    result = project_manager.create_project(long_name, "Description")
    assert result == "Error: Project's name must be <= 30 words."


def test_create_project_with_duplicate_name(project_manager):
    """Test creating a project with a duplicate name"""
    project_manager.create_project("Test Project", "Description")
    result = project_manager.create_project("Test Project", "Another description")
    assert result == "Error: Project name already exists."


def test_edit_project(project_manager):
    """Test editing a project"""
    project_manager.create_project("Old Project", "Description")
    result = project_manager.edit_project("Old Project", "Updated Project", "Updated description")
    assert result == "Project 'Old Project' updated successfully to 'Updated Project'"
    assert project_manager.projects[0].name == "Updated Project"


def test_delete_project(project_manager):
    """Test deleting a project"""
    project_manager.create_project("Test Project", "Description")
    result = project_manager.delete_project("Test Project")
    assert result == "Project 'Test Project' and all its tasks have been deleted successfully."
    assert len(project_manager.projects) == 0
