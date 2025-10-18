import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from project_manager import ProjectManager
from task_manager import TaskManager
from project_repository import ProjectRepository
from task_repository import TaskRepository

def print_menu():
    """Display the menu to the user"""
    print("\n===== TO DO LIST APP =====")
    print("1. Create a new project")
    print("2. Show all projects")
    print("3. Add a task to a project")
    print("4. Show all tasks of a project")
    print("5. Edit a project")
    print("6. Delete a project")
    print("7. Exit")

def create_project(project_manager):
    """Create a new project"""
    name = input("Enter project name: ")
    description = input("Enter project description: ")
    result = project_manager.create_project(name, description)
    print(result)

def show_projects(project_manager):
    """Show all projects"""
    projects = project_manager.list_projects()
    if isinstance(projects, str):  # Check if an error message is returned
        print(projects)
    else:
        for p in projects:
            print(f"{p.id}. {p.name} — {p.description}")

def add_task(task_manager):
    """Add a new task to a project"""
    project_id = int(input("Enter project ID: "))
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    deadline = input("Enter task deadline (YYYY-MM-DD): ")
    result = task_manager.create_task(project_id, title, description, deadline)
    print(result)

def show_tasks(task_manager):
    """Show all tasks of a project"""
    project_id = int(input("Enter project ID: "))
    tasks = task_manager.list_tasks(project_id)
    if isinstance(tasks, str):  # Check if an error message is returned
        print(tasks)
    else:
        for t in tasks:
            print(f"{t.id}. {t.title} — {t.status} — Deadline: {t.deadline}")

def edit_project(project_manager):
    """Edit a project"""
    old_name = input("Enter the current project name to edit: ")
    new_name = input("Enter new project name: ")
    new_description = input("Enter new project description: ")
    result = project_manager.edit_project(old_name, new_name, new_description)
    print(result)

def delete_project(project_manager):
    """Delete a project"""
    name = input("Enter the project name to delete: ")
    result = project_manager.delete_project(name)
    print(result)

def main():
    """Main function that runs the program and shows the menu"""
    # Initialize repositories
    project_repo = ProjectRepository()
    task_repo = TaskRepository()

    # Initialize managers
    project_manager = ProjectManager(project_repo)
    task_manager = TaskManager(task_repo)

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            create_project(project_manager)
        elif choice == "2":
            show_projects(project_manager)
        elif choice == "3":
            add_task(task_manager)
        elif choice == "4":
            show_tasks(task_manager)
        elif choice == "5":
            edit_project(project_manager)
        elif choice == "6":
            delete_project(project_manager)
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
