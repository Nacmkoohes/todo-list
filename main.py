class Project:
    def __init__(self,name,description):
        self.name = name
        self.description = description
        self.tasks = []
    def add_task(self,task):
        self.tasks.append(task)
    def remove_task(self,task):
        self.tasks.remove(task)
    def __str__(self):
        return f"Project Name: {self.name} Tasks: {self.tasks} Description:{str(self.description)}"


class CreateProject:
    MAX_NUMBER_OF_PROJECTS = 10

    def __init__(self):
        self.projects = []
    def  create_project(self,name,description):
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


class Task:
    def __init__(self,title,description,deadline,status="Todo"):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.status = status
    def change_status(self, new_status):
        if new_status in ["Todo","Doing","Done"]:
            self.status = new_status
        else:
            print("Invalid status")
    def __str__(self):
        return f"Task Title: {self.title}, Status: {self.status}, Deadline: {self.deadline}"


