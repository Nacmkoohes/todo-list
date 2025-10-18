# project_repository.py

class ProjectRepository:
    def __init__(self):
        self.projects = []  # برای ذخیره‌سازی پروژه‌ها در حافظه

    def save(self, project):
        self.projects.append(project)

    def get_all(self):
        return self.projects

    def find_by_id(self, project_id):
        return next((project for project in self.projects if project.id == project_id), None)

    def delete(self, project_id):

        self.projects = [project for project in self.projects if project.id != project_id]
