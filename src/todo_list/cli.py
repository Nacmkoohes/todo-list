import argparse
import json
from pathlib import Path
from datetime import datetime
from itertools import count

from todo_list.main import ManageProject, Task, Project  # type: ignore
import todo_list.main as domain

STATE_DIR = Path.home() / ".todo_list"
STATE_FILE = STATE_DIR / "state.json"


def _ensure_storage():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        STATE_FILE.write_text(json.dumps({"projects": []}, ensure_ascii=False, indent=2))


def _project_to_dict(p: Project) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "created_at": p.created_at.isoformat(),
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "deadline": t.deadline.isoformat() if t.deadline else None,
                "status": t.status,
            }
            for t in p.tasks
        ],
    }


def _load_state(manager: ManageProject):
    _ensure_storage()
    data = json.loads(STATE_FILE.read_text() or '{"projects": []}')
    max_pid = 0
    max_tid = 0
    for p in data.get("projects", []):
        proj = Project(p["name"], p.get("description", ""))
        proj.id = int(p["id"])
        try:
            proj.created_at = datetime.fromisoformat(p["created_at"])
        except ValueError as e:
            pass
        for td in p.get("tasks", []):
            t = Task(td["title"], td.get("description", ""), td.get("deadline"), td.get("status", "todo"))
            t.id = int(td["id"])
            proj.tasks.append(t)
            if t.id > max_tid:
                max_tid = t.id
        manager.projects.append(proj)
        manager._by_name[proj.name.strip().lower()] = proj
        if proj.id > max_pid:
            max_pid = proj.id
    domain._project_ids = count(max_pid + 1)
    domain._task_ids = count(max_tid + 1)


def _save_state(manager: ManageProject):
    _ensure_storage()
    payload = {"projects": [_project_to_dict(p) for p in manager.projects]}
    STATE_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def _print_msg(msg: str, as_json: bool):
    if as_json:
        print(json.dumps({"message": msg}, ensure_ascii=False))
    else:
        print(msg)


def _print_list_str(items: list[str], as_json: bool, key="items"):
    if as_json:
        print(json.dumps({key: items}, ensure_ascii=False, indent=2))
    else:
        for it in items:
            print(it)


def _print_projects(manager: ManageProject, as_json: bool):
    projs = manager.list_projects()
    if isinstance(projs, str):
        _print_msg(projs, as_json)
        return
    if as_json:
        print(json.dumps([_project_to_dict(p) for p in manager.projects], ensure_ascii=False, indent=2))
    else:
        for p in projs:
            print(p)


def _print_tasks_of_project(p: Project, as_json: bool):
    if as_json:
        print(json.dumps(_project_to_dict(p)["tasks"], ensure_ascii=False, indent=2))
    else:
        out = p.list_tasks()
        if isinstance(out, str):
            print(out)
        else:
            for line in out:
                print(line)


def main():
    manager = ManageProject()
    _load_state(manager)

    parser = argparse.ArgumentParser(description="Manage your To-Do List (persistent, script-friendly)")
    parser.add_argument("--json", action="store_true", help="Print output as JSON")
    parser.add_argument("--create_project", nargs=2, metavar=("name", "description"))
    parser.add_argument("--edit_project", nargs=3, metavar=("old_name", "new_name", "new_description"))
    parser.add_argument("--delete_project", metavar="name")
    parser.add_argument("--list_projects", action="store_true")
    parser.add_argument("--delete_project_id", metavar="project_id", type=int)
    parser.add_argument("--list_tasks_by_project_id", metavar="project_id", type=int)
    parser.add_argument("--add_task", nargs=4, metavar=("project_name", "task_title", "task_description", "deadline"))
    parser.add_argument("--remove_task", nargs=2, metavar=("project_name", "task_title"))
    parser.add_argument("--remove_task_id", nargs=2, metavar=("project_name", "task_id"))
    parser.add_argument("--change_status", nargs=3, metavar=("project_name", "task_id", "new_status"))
    parser.add_argument(
        "--edit_task",
        nargs="+",
        help="Usage: --edit_task <project_name> <task_id> [--title T] [--desc D] [--deadline YYYY-MM-DD|empty] [--status S]",
    )
    parser.add_argument("--list_tasks", metavar="project_name")

    args, unknown = parser.parse_known_args()
    j = args.json
    any_action = False

    if args.create_project:
        any_action = True
        name, description = args.create_project
        _print_msg(manager.create_project(name, description), j)

    if args.edit_project:
        any_action = True
        old_name, new_name, new_description = args.edit_project
        _print_msg(manager.edit_project(old_name, new_name, new_description), j)

    if args.delete_project:
        any_action = True
        _print_msg(manager.delete_project(args.delete_project), j)

    if args.list_projects:
        any_action = True
        _print_projects(manager, j)

    if args.delete_project_id is not None:
        any_action = True
        _print_msg(manager.delete_project_by_id(int(args.delete_project_id)), j)

    if args.list_tasks_by_project_id is not None:
        any_action = True
        pid = int(args.list_tasks_by_project_id)
        p = manager.get_project_by_id(pid)
        if not p:
            _print_msg("Error: Project not found.", j)
        else:
            _print_tasks_of_project(p, j)

    if args.add_task:
        any_action = True
        project_name, task_title, task_description, deadline = args.add_task
        deadline = None if (deadline is None or str(deadline).strip() == "") else deadline
        p = manager.get_project_by_name(project_name)
        if not p:
            _print_msg(f"Project '{project_name}' not found.", j)
        else:
            t = Task(task_title, task_description, deadline)
            _print_msg(p.add_task(t), j)

    if args.remove_task:
        any_action = True
        project_name, task_title = args.remove_task
        p = manager.get_project_by_name(project_name)
        if not p:
            _print_msg(f"Project '{project_name}' not found.", j)
        else:
            _print_msg(p.remove_task(task_title), j)

    if args.remove_task_id:
        any_action = True
        project_name, task_id_str = args.remove_task_id
        p = manager.get_project_by_name(project_name)
        if not p:
            _print_msg(f"Project '{project_name}' not found.", j)
        else:
            try:
                tid = int(task_id_str)
            except ValueError:
                _print_msg("Error: task_id must be an integer.", j)
            else:
                _print_msg(p.remove_task_by_id(tid), j)

    if args.change_status:
        any_action = True
        project_name, task_id_str, new_status = args.change_status
        p = manager.get_project_by_name(project_name)
        if not p:
            _print_msg(f"Project '{project_name}' not found.", j)
        else:
            try:
                tid = int(task_id_str)
            except ValueError:
                _print_msg("Error: task_id must be an integer.", j)
            else:
                t = p.get_task_by_id(tid)
                if not t:
                    _print_msg(f"Error: Task #{tid} not found in project '{project_name}'", j)
                else:
                    _print_msg(t.change_status(new_status), j)

    if args.edit_task:
        any_action = True
        tokens = args.edit_task
        if len(tokens) < 2:
            _print_msg(
                "Error: Usage -> --edit_task <project_name> <task_id> [--title T] [--desc D] [--deadline YYYY-MM-DD|empty] [--status S]",
                j,
            )
        else:
            project_name = tokens[0]
            try:
                tid = int(tokens[1])
            except ValueError:
                _print_msg("Error: task_id must be an integer.", j)
                tid = None

            if tid is not None:
                new_title = None
                new_desc = None
                new_deadline = None
                new_status = None

                i = 2
                while i < len(tokens):
                    tk = tokens[i]
                    if tk == "--title" and i + 1 < len(tokens):
                        new_title = tokens[i + 1]
                        i += 2
                    elif tk == "--desc" and i + 1 < len(tokens):
                        new_desc = tokens[i + 1]
                        i += 2
                    elif tk == "--deadline" and i + 1 < len(tokens):
                        val = tokens[i + 1]
                        new_deadline = None if (val is None or str(val).strip() == "") else val
                        i += 2
                    elif tk == "--status" and i + 1 < len(tokens):
                        new_status = tokens[i + 1]
                        i += 2
                    else:
                        i += 1

                p = manager.get_project_by_name(project_name)
                if not p:
                    _print_msg(f"Project '{project_name}' not found.", j)
                else:
                    t = p.get_task_by_id(tid)
                    if not t:
                        _print_msg(f"Error: Task #{tid} not found in project '{project_name}'", j)
                    else:
                        _print_msg(
                            t.edit_task(
                                new_title=new_title,
                                new_description=new_desc,
                                new_deadline=new_deadline,
                                new_status=new_status,
                            ),
                            j,
                        )

    if args.list_tasks:
        any_action = True
        project_name = args.list_tasks
        p = manager.get_project_by_name(project_name)
        if not p:
            _print_msg(f"Project '{project_name}' not found.", j)
        else:
            _print_tasks_of_project(p, j)

    if not any_action:
        parser.print_help()

    _save_state(manager)


if __name__ == "__main__":
    main()
