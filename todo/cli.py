# todo/cli.py
from __future__ import annotations
from typing import List, Tuple
from .services.project_service import ProjectService
from .services.task_service import TaskService
from .config import ALLOWED_STATUSES

# --- Boot services (shared in-memory store)
ps = ProjectService()
ts = TaskService(project_store=ps.project_store)

# ---------- Utils (table + inputs) ----------
def _line(w: int) -> str:
    return "─" * w

def _fmt_row(cols: List[Tuple[str, int]]) -> str:
    parts = []
    for text, w in cols:
        s = str(text)
        if len(s) > w:
            s = s[: w - 1] + "…"
        parts.append(s.ljust(w))
    return "│ " + " │ ".join(parts) + " │"

def print_table(headers: List[Tuple[str, int]], rows: List[List[str]]) -> None:
    total_w = 3 + sum(w + 3 for _, w in headers)
    print("┌" + _line(total_w - 2) + "┐")
    print(_fmt_row(headers))
    print("├" + _line(total_w - 2) + "┤")
    for r in rows:
        print(_fmt_row([(c, headers[i][1]) for i, c in enumerate(r)]))
    print("└" + _line(total_w - 2) + "┘")

def ask(prompt: str, allow_empty: bool = False) -> str:
    while True:
        v = input(prompt).strip()
        if v or allow_empty:
            return v
        print("⚠️  Value cannot be empty.")

def pause():
    input("\n⏎ Press Enter to continue…")

# ---------- Menus ----------
def menu_main():
    print("\n===== ToDo CLI (Layered) =====")
    print(" 1) Create Project")
    print(" 2) List Projects")
    print(" 3) Edit Project")
    print(" 4) Delete Project")
    print(" 5) Add Task")
    print(" 6) List Tasks")
    print(" 7) Change Task Status")
    print(" 8) Edit Task")
    print(" 9) Delete Task")
    print(" 0) Exit")
    return ask("Choose an option: ")

# ---------- Actions (9 user stories) ----------
def create_project():
    name = ask("Project name: ")
    desc = ask("Description (optional): ", allow_empty=True)
    try:
        p = ps.create_project(name, desc)
        print(f"✅ Created: {p.name} ({p.id})")
    except Exception as e:
        print(f"❌ {e}")
    pause()

def list_projects(show_pause=True):
    projects = list(ps.list_projects())
    headers = [("Name", 24), ("Project ID", 36), ("#Tasks", 6)]
    rows = [[p.name, p.id, str(len(p.tasks))] for p in projects]
    print()
    print_table(headers, rows)
    if show_pause:
        pause()

def edit_project():
    list_projects(show_pause=False)
    pid = ask("Project ID: ")
    new_name = ask("New name (empty = no change): ", allow_empty=True)
    new_desc = ask("New description (empty = no change): ", allow_empty=True)
    try:
        kwargs = {}
        if new_name: kwargs["name"] = new_name
        if new_desc: kwargs["description"] = new_desc
        p = ps.edit_project(pid, **kwargs)
        print(f"✏️  Edited: {p.name} ({p.id})")
    except Exception as e:
        print(f"❌ {e}")
    pause()

def delete_project():
    list_projects(show_pause=False)
    pid = ask("Project ID to delete: ")
    try:
        ps.delete_project(pid)
        print(f"🗑️  Project deleted: {pid}")
    except Exception as e:
        print(f"❌ {e}")
    pause()

def add_task():
    list_projects(show_pause=False)
    pid = ask("Project ID: ")
    title = ask("Task title: ")
    desc = ask("Description (optional): ", allow_empty=True)
    try:
        t = ts.add_task(pid, title, desc)
        print(f"➕ Task added: {t.title} ({t.id})")
    except Exception as e:
        print(f"❌ {e}")
    pause()

def list_tasks(show_pause=True):
    list_projects(show_pause=False)
    pid = ask("Project ID: ")
    try:
        tasks = list(ts.list_tasks(pid))
        headers = [("Title", 28), ("Task ID", 36), ("Status", 12)]
        rows = [[t.title, t.id, t.status] for t in tasks]
        print()
        print_table(headers, rows)
    except Exception as e:
        print(f"❌ {e}")
    if show_pause:
        pause()

def change_status():
    list_tasks(show_pause=False)
    pid = ask("Project ID: ")
    tid = ask("Task ID: ")
    print(f"Allowed statuses: {', '.join(ALLOWED_STATUSES)}")
    status = ask("New status: ")
    try:
        t = ts.change_status(pid, tid, status)
        print(f"🔁 {t.title} -> {t.status}")
    except Exception as e:
        print(f"❌ {e}")
    pause()

def edit_task():
    list_tasks(show_pause=False)
    pid = ask("Project ID: ")
    tid = ask("Task ID: ")
    title = ask("New title (empty = no change): ", allow_empty=True)
    desc  = ask("New description (empty = no change): ", allow_empty=True)
    status= ask("New status (empty = no change): ", allow_empty=True)
    try:
        kwargs = {}
        if title: kwargs["title"] = title
        if desc:  kwargs["description"] = desc
        if status: kwargs["status"] = status
        t = ts.edit_task(pid, tid, **kwargs)
        print(f"✏️  Edited task: {t.title} ({t.id}) — {t.status}")
    except Exception as e:
        print(f"❌ {e}")
    pause()

def delete_task():
    list_tasks(show_pause=False)
    pid = ask("Project ID: ")
    tid = ask("Task ID: ")
    try:
        ts.delete_task(pid, tid)
        print(f"🗑️  Task deleted: {tid}")
    except Exception as e:
        print(f"❌ {e}")
    pause()

# ---------- App loop ----------
def main():
    actions = {
        "1": create_project,
        "2": list_projects,
        "3": edit_project,
        "4": delete_project,
        "5": add_task,
        "6": list_tasks,
        "7": change_status,
        "8": edit_task,
        "9": delete_task,
        "0": lambda: None,
    }
    while True:
        choice = menu_main()
        if choice == "0":
            print("Bye! 👋")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("⚠️  Invalid option.")
            pause()

if __name__ == "__main__":
    main()
