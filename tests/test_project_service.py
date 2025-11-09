from services.project_service import ProjectService


def test_create_project():
    project_service = ProjectService()
    project = project_service.create_project("Test Project", "This is a test project.")

    assert project.name == "Test Project"
    assert project.description == "This is a test project."
    assert len(project_service.projects) == 1


def test_edit_project():
    project_service = ProjectService()
    project = project_service.create_project("Test Project", "This is a test project.")

    response = project_service.edit_project("Test Project", new_name="Updated Project",
                                            new_description="Updated description.")

    assert response == "Project 'Test Project' updated successfully."
    assert project.name == "Updated Project"
    assert project.description == "Updated description."


def test_delete_project():
    project_service = ProjectService()
    project = project_service.create_project("Test Project", "This is a test project.")

    response = project_service.delete_project("Test Project")

    assert response == "Project 'Test Project' deleted successfully."
    assert len(project_service.projects) == 0
