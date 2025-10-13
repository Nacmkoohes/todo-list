MAX_NUMBER_OF_TASKS = 10


class Project:
    MAX_NUMBER_OF_TASKS = 10
    def __init__(self,name,description):
        self.name = name
        self.description = description
        self.tasks = []
    def add_task(self,task):
        if len(self.tasks)>= self.MAX_NUMBER_OF_TASKS:
            return "Error: Maximum number of tasks reached."
        if len(task.title.split())>30:
            return "Error: Task name is too long."
        if len(task.description.split())>150:
            return "Error: Task description is too long."

        if task.status not in ["Todo","Doing","Done"]:
            return "Error: Task status is invalid."

        self.tasks.append(task)
        return f"Task '{task.title}' added successfully to project '{self.name}'"
    def delete_task(self,task_title):
        task = next((t for t in self.tasks if t.title == task_title), None)
        if not task:
            return f"Error: Task '{task_title}' not found in project '{self.name}'"
        self.tasks.remove(task)
        return f"Task '{task_title}' deleted successfully from project '{self.name}'"

    def __str__(self):
        return f"Project Name: {self.name} Tasks: {self.tasks} Description:{str(self.description)}"


class ManageProject:
    MAX_NUMBER_OF_PROJECTS = 10

    def __init__(self):
        self.projects = []
    def create_project(self,name,description):
        #Number of Projects should be less than the MAX_NUMBER_OF_PROJECTS
        if len(self.projects) >= self.MAX_NUMBER_OF_PROJECTS:
            return "Error:Maximum number of projects reached."
        #Project's name should be less than 30 words
        if len(name.split()) > 30:
            return "Error: Project's name must be <= 30 words."
        if len(description.split()) > 150:
            return "Error: Project's description must be <= 150 words."
        if any(p.name==name for p in self.projects):
            return "Error: Project name already exists."

        new_project = Project(name,description)
        self.projects.append(new_project)
        return f"Project created successfully."
    def edit_project(self,old_name,new_name,new_description):
        project=next((p for p in self.projects if p.name == old_name), None)
        if not project:
            return "Error: Project does not exist."
        if len(new_name.split()) > 30:
            return "Error: Project's name must be <= 30 words."
        if len(new_description.split()) > 150:
            return "Error: Project's description must be <= 150 words."

        if any(p.name==new_name and p!=project for p in self.projects):
            return "Error: Project name already exists."

        project.name = new_name
        project.description = new_description
        return f" Project '{old_name}' updated successfully to '{new_name}'"

    def delete_project(self, name):
        project = next((p for p in self.projects if p.name == name), None)
        if not project:
            return "Error: Project not found."

        self.projects.remove(project)
        #Cascade Delete
        project.tasks.clear()
        return f"Project '{name}' and all it's tasks have been deleted successfully."


class Task:

    def __init__(self,title,description,deadline,status="Todo"):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.status = status
    def change_status(self, new_status):
        if new_status in ["Todo","Doing","Done"]:
            self.status = new_status
            return f"Task '{self.title}'status changed to '{new_status}'"
        else:
            return "Error:Invalid status"

    def edit_task(self,new_title=None,new_description=None,new_deadline=None,new_status=None):
        if new_title:
            if len(new_title.split()) > 30:
                return "Error: Task title must be <= 30 words."
            self.title = new_title
        if new_description:
                if len(new_description.split()) > 150:
                    return "Error: Task description must be <= 150 words."
                self.description = new_description
        if new_deadline:
                self.deadline = new_deadline
        if new_status:
            if new_status not in ["Todo", "Doing", "Done"]:
                return "Error: Task status is invalid."
            self.status = new_status
        return f"Task '{self.title}' updated successfully "


    def __str__(self):
        return f"Task Title: {self.title}, Status: {self.status}, Deadline: {self.deadline}"

