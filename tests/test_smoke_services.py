# tests/test_smoke_services.py
from project_service import ProjectService
from task_service import TaskService
import config

def test_projects_basic():
    ps = ProjectService()  # چون auto-wire کردیم، بدون ورودی کار می‌کند
    assert list(ps.list_projects()) == []

    p1 = ps.create_project("Proj A", "demo")
    p2 = ps.create_project("Proj B", "web")

    names = [p.name for p in ps.list_projects()]
    assert "Proj A" in names and "Proj B" in names

def test_tasks_flow():
    # یک سرویس پروژه و یک پروژه می‌سازیم
    ps = ProjectService()
    p = ps.create_project("X")

    # TaskService را به همان انبار پروژه‌ها وصل می‌کنیم
    ts = TaskService(project_store=ps.project_store)

    # add دو تسک
    t1 = ts.add_task(p.id, "Write tests")
    t2 = ts.add_task(p.id, "Refactor services")

    titles = [t.title for t in ts.list_tasks(p.id)]
    assert titles == ["Write tests", "Refactor services"]

    # change_status
    ts.change_status(p.id, t1.id, "doing")
    t1_after = [t for t in ts.list_tasks(p.id) if t.id == t1.id][0]
    assert t1_after.status == "doing"
    assert "doing" in config.ALLOWED_STATUSES

    # edit_task (فقط title را تغییر بده)
    ts.edit_task(p.id, t2.id, title="Refactor services (clean)")
    t2_after = [t for t in ts.list_tasks(p.id) if t.id == t2.id][0]
    assert t2_after.title == "Refactor services (clean)"

    # delete_task
    ts.delete_task(p.id, t1.id)
    ids_after = [t.id for t in ts.list_tasks(p.id)]
    assert t1.id not in ids_after
