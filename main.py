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