from __future__ import annotations
from todo.app_factory import build_services
from todo.exceptions.service_exceptions import ProjectAlreadyExists, ProjectNotFound, TaskNotFound, InvalidStatus
from todo.config import ALLOWED_STATUSES

ps, ts = build_services()

def _select_project_id() -> int | None:
    projects = list(ps.list_projects())
    if not projects:
        print("ℹ️ No projects.")
        return None
    print("\nProjects:")
    for i, p in enumerate(projects, start=1):
        print(f"{i}) #{p.id}  {p.name}")
    raw = input("Pick project (number / ID / exact name / partial): ").strip()
    if not raw:
        return None
    if raw.isdigit():
        idx = int(raw)
        if 1 <= idx <= len(projects):
            return projects[idx - 1].id
    if raw.isdigit():
        return int(raw)
    for p in projects:
        if p.name.lower() == raw.lower():
            return p.id
    matches = [p for p in projects if raw.lower() in p.name.lower()]
    if len(matches) == 1:
        return matches[0].id
    elif len(matches) > 1:
        print("Multiple matches:")
        for p in matches:
            print(f"- #{p.id}  {p.name}")
        return None
    print("❌ Not found.")
    return None

def _select_task_id(project_id: int) -> int | None:
    tasks = list(ts.list_tasks_by_project(project_id))
    if not tasks:
        print("ℹ️ No tasks for this project.")
        return None
    print("\nTasks:")
    for i, t in enumerate(tasks, start=1):
        d = t.deadline.date().isoformat() if getattr(t, "deadline", None) else "-"
        print(f"{i}) #{t.id}  {t.title}  [{t.status}]  (deadline={d})")
    raw = input("Pick task (number / ID / exact title / partial): ").strip()
    if not raw:
        return None
    if raw.isdigit():
        idx = int(raw)
        if 1 <= idx <= len(tasks):
            return tasks[idx - 1].id
    if raw.isdigit():
        return int(raw)
    for t in tasks:
        if t.title.lower() == raw.lower():
            return t.id
    matches = [t for t in tasks if raw.lower() in t.title.lower()]
    if len(matches) == 1:
        return matches[0].id
    elif len(matches) > 1:
        print("Multiple matches:")
        for t in matches:
            print(f"- #{t.id}  {t.title}")
        return None
    print("❌ Not found.")
    return None

# Handlers (9 user stories)
def create_project():
    name = input("Project name: ").strip()
    desc = input("Description (optional): ").strip() or None
    try:
        p = ps.create_project(name, desc)
        print(f"✅ Project created: #{p.id} – {p.name}")
    except ProjectAlreadyExists as e:
        print(f"❌ {e}")
    except ValueError as e:
        print(f"❌ {e}")

def edit_project():
    pid = _select_project_id()
    if not pid: return
    new_name = input("New name (leave empty to keep): ").strip() or None
    new_desc = input("New desc (leave empty to keep): ").strip() or None
    try:
        p = ps.edit_project(pid, name=new_name, description=new_desc)
        print(f"✅ Project updated: #{p.id} – {p.name}")
    except (ProjectNotFound, ProjectAlreadyExists, ValueError) as e:
        print(f"❌ {e}")

def delete_project():
    pid = _select_project_id()
    if not pid: return
    try:
        ps.delete_project(pid)
        print("✅ Project deleted.")
    except ProjectNotFound as e:
        print(f"❌ {e}")

def list_projects():
    projects = list(ps.list_projects())
    if not projects:
        print("ℹ️ No projects.")
        return
    print("\nID | Name                | Description")
    print("-- | ------------------- | -----------")
    for p in projects:
        print(f"{p.id:>2} | {p.name:<19} | {p.description or ''}")
    print()

def add_task():
    pid = _select_project_id()
    if not pid: return
    title = input("Task title: ").strip()
    desc = input("Task description (optional): ").strip() or None
    deadline = input("Deadline (YYYY-MM-DD or empty): ").strip() or None
    try:
        t = ts.add_task(pid, title, description=desc, deadline=deadline)
        print(f"✅ Task created: #{t.id} – {t.title}")
    except (ProjectNotFound, ValueError) as e:
        print(f"❌ {e}")

def edit_task():
    pid = _select_project_id()
    if not pid: return
    tid = _select_task_id(pid)
    if not tid: return
    new_title = input("New title (empty = keep): ").strip() or None
    new_desc = input("New desc (empty = keep): ").strip() or None
    new_deadline = input("New deadline YYYY-MM-DD (empty = keep): ").strip() or None
    try:
        t = ts.edit_task(tid, title=new_title, description=new_desc, deadline=new_deadline)
        print(f"✅ Task updated: #{t.id} – {t.title}")
    except (TaskNotFound, ValueError) as e:
        print(f"❌ {e}")

def delete_task():
    pid = _select_project_id()
    if not pid: return
    tid = _select_task_id(pid)
    if not tid: return
    try:
        ts.delete_task(tid)
        print("✅ Task deleted.")
    except TaskNotFound as e:
        print(f"❌ {e}")

def list_tasks_by_project():
    pid = _select_project_id()
    if not pid: return
    tasks = list(ts.list_tasks_by_project(pid))
    if not tasks:
        print("ℹ️ No tasks for this project.")
        return
    print("\nID | Title               | Status | Deadline")
    print("-- | ------------------- | ------ | --------")
    for t in tasks:
        d = t.deadline.date().isoformat() if getattr(t, "deadline", None) else "-"
        print(f"{t.id:>2} | {t.title:<19} | {t.status:<6} | {d}")
    print()

def change_task_status():
    pid = _select_project_id()
    if not pid: return
    tid = _select_task_id(pid)
    if not tid: return
    print(f"Allowed: {', '.join(ALLOWED_STATUSES)}")
    st = input("New status: ").strip().lower()
    try:
        t = ts.change_task_status(tid, st)
        print(f"✅ Status changed: #{t.id} → {t.status}")
    except (TaskNotFound, InvalidStatus) as e:
        print(f"❌ {e}")

def main():
    MENU = {
        "1": ("Create Project", create_project),
        "2": ("Edit Project", edit_project),
        "3": ("Delete Project", delete_project),
        "4": ("List Projects", list_projects),
        "5": ("Add Task", add_task),
        "6": ("Edit Task", edit_task),
        "7": ("Delete Task", delete_task),
        "8": ("List Tasks by Project", list_tasks_by_project),
        "9": ("Change Task Status", change_task_status),
        "0": ("Exit", None),
    }
    while True:
        print("\n=== ToDo CLI ===")
        for k, (label, _) in MENU.items():
            print(f"{k}) {label}")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Bye!")
            break
        action = MENU.get(choice)
        if not action:
            print("❌ Invalid option.")
            continue
        action[1]()

if __name__ == "__main__":
    main()
