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
