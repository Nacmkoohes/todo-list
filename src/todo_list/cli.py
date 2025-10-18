from main import ManageProject, Task
import argparse


def main():
    manager = ManageProject()

    parser = argparse.ArgumentParser(description="Manage your To-Do List Projects and Tasks")

    parser.add_argument('--create_project', nargs=2, metavar=('name', 'description'), help="Create a new project")
    parser.add_argument('--edit_project', nargs=3, metavar=('old_name', 'new_name', 'new_description'),
                        help="Edit an existing project")
    parser.add_argument('--delete_project', metavar='name', help="Delete a project")
    parser.add_argument('--list_projects', action='store_true', help="List all projects")

    parser.add_argument('--add_task', nargs=4, metavar=('project_name', 'task_title', 'task_description', 'deadline'),
                        help="Add a task to a project")
    parser.add_argument('--remove_task', nargs=2, metavar=('project_name', 'task_title'),
                        help="Remove a task from a project")
    parser.add_argument('--list_tasks', metavar='project_name', help="List tasks in a project")

    args = parser.parse_args()

    if args.create_project:
        name, description = args.create_project
        print(manager.create_project(name, description))

    elif args.edit_project:
        old_name, new_name, new_description = args.edit_project
        print(manager.edit_project(old_name, new_name, new_description))

    elif args.delete_project:
        project_name = args.delete_project
        print(manager.delete_project(project_name))

    elif args.list_projects:
        projects = manager.list_projects()
        if isinstance(projects, list):
            for project in projects:
                print(project)
        else:
            print(projects)

    elif args.add_task:
        project_name, task_title, task_description, deadline = args.add_task
        task = Task(task_title, task_description, deadline)
        project = manager.get_project_by_name(project_name)
        if project:
            print(project.add_task(task))
        else:
            print(f"Project '{project_name}' not found.")

    elif args.remove_task:
        project_name, task_title = args.remove_task
        project = manager.get_project_by_name(project_name)
        if project:
            print(project.remove_task(task_title))
        else:
            print(f"Project '{project_name}' not found.")

    elif args.list_tasks:
        project_name = args.list_tasks
        project = manager.get_project_by_name(project_name)
        if project:
            tasks = project.list_tasks()
            if isinstance(tasks, list):
                for task in tasks:
                    print(task)
            else:
                print(tasks)
        else:
            print(f"Project '{project_name}' not found.")


if __name__ == "__main__":
    main()
