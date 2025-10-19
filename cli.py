import argparse
from services.project_service import ProjectService
from services.task_service import TaskService
from config import ALLOWED_STATUSES
# Create instances of the services
project_service = ProjectService('projects.json')
task_service = TaskService()


class CLIApp:
    def __init__(self):
        self.project_service = ProjectService()
        self.task_service = TaskService()

    # Function to print the main menu
    def print_menu(self):
        print("\n===== TO DO LIST APP =====")
        print("1. Create a new project")
        print("2. Show all projects")
        print("3. Add a task to a project")
        print("4. Show all tasks of a project")
        print("5. Edit a project")
        print("6. Delete a project")
        print("7. Change task status")
        print("8. Exit")

    # Function to create a project
    def create_project(self):
        name = input("Enter project name: ")
        description = input("Enter project description: ")
        project = self.project_service.create_project(name, description)
        print(f"Project '{project.name}' created successfully.")

    # Function to show all projects
    def show_projects(self):
        projects = self.project_service.list_projects()
        if not projects:
            print("No projects found.")
            return
        for project in projects:
            print(f"ID: {project.project_id} | Name: {project.name} | Description: {project.description}")

    # Function to add a task to a project
    def add_task(self):
        self.show_projects()
        try:
            project_id = int(input("Enter project ID to add task: ").strip())
        except ValueError:
            print("Invalid project ID. Please enter a number.")
            return

        title = input("Enter task title: ").strip()
        description = input("Enter task description: ").strip()
        status = input("Enter task status (todo, doing, done): ").strip().lower()

        if status not in ALLOWED_STATUSES:
            print(f"Error: Task status is invalid. Allowed: {', '.join(sorted(ALLOWED_STATUSES))}")
            return

        project = self.project_service.get_project_by_id(project_id)
        if not project:
            print("Project not found.")
            return

        task = self.task_service.create_task(title, description, status=status)
        if isinstance(task, str) and task.startswith("Error"):
            print(task)
            return

        result = project.add_task(task)
        print(result)
        if not result.lower().startswith("error"):
            self.project_service.save_projects()

    # Function to show all tasks of a project
    def show_tasks(self):
        self.show_projects()  # Display all projects
        project_id = int(input("Enter project ID to show tasks: "))
        project = self.project_service.get_project_by_id(project_id)
        if project:
            tasks = project.list_tasks()
            if tasks:
                for task in tasks:
                    print(f"ID: {task.id} | Title: {task.title} | Status: {task.status}")
            else:
                print("No tasks in this project.")
        else:
            print("Project not found.")

    # Function to edit a project
    def edit_project(self):
        self.show_projects()
        project_id = int(input("Enter project ID to edit: "))
        new_name = input("Enter new project name: ")
        new_description = input("Enter new project description: ")
        updated = self.project_service.edit_project(project_id, new_name, new_description)
        print(f"Project updated: {updated}")

    # Function to delete a project
    def delete_project(self):
        self.show_projects()
        project_id = int(input("Enter project ID to delete: "))  # Use the correct project ID for deletion
        deleted = self.project_service.delete_project(project_id)
        print(f"Project deleted: {deleted}")

    def change_task_status(self):
        self.show_projects()
        try:
            project_id = int(input("Enter project ID of the task: ").strip())
        except ValueError:
            print("Invalid project ID. Please enter a number.")
            return

        project = self.project_service.get_project_by_id(project_id)
        if not project:
            print("Project not found.")
            return

        try:
            task_id = int(input("Enter task ID to change status: ").strip())
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        task = next((t for t in project.tasks if getattr(t, "id", None) == task_id), None)
        if not task:
            print("Task not found.")
            return

        new_status = input("Enter new status (todo, doing, done): ").strip().lower()
        if new_status not in ALLOWED_STATUSES:
            print(f"Error: Task status is invalid. Allowed: {', '.join(sorted(ALLOWED_STATUSES))}")
            return

        msg = task.change_status(new_status)
        print(msg)
        if not msg.lower().startswith("error"):
            self.project_service.save_projects()

    # Main function that runs the menu
    def main(self):
        while True:
            self.print_menu()  # Print the menu
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.create_project()
            elif choice == "2":
                self.show_projects()
            elif choice == "3":
                self.add_task()
            elif choice == "4":
                self.show_tasks()
            elif choice == "5":
                self.edit_project()
            elif choice == "6":
                self.delete_project()
            elif choice == "7":
                self.change_task_status()
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid option!")


# Entry point for the CLI program
if __name__ == "__main__":
    app = CLIApp()  # Create an instance of the CLIApp
    app.main()  # Run the main function
