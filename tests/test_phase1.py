# tests/test_phase1.py
from todo_list.main import ManageProject, Project, Task

def test_status_normalization_and_deadline_parse():
    # status باید lowercase ذخیره شود و deadline ISO معتبر شود
    t = Task(title="T1", description="desc", deadline="2025-12-01", status="Doing")
    assert t.status == "doing"
    assert str(t.deadline) == "2025-12-01"

    # تغییر وضعیت با حروف مختلف → نرمال می‌شود
    msg = t.change_status("DONE")
    assert "changed" in msg.lower()
    assert t.status == "done"

def test_add_edit_and_remove_task_by_id():
    p = Project("P1", "first")
    t1 = Task("A", "a", "2025-12-10")
    t2 = Task("B", "b", None)

    # افزودن
    assert "added successfully" in p.add_task(t1).lower()
    assert "added successfully" in p.add_task(t2).lower()
    assert len(p.tasks) == 2

    # ویرایش با deadline نامعتبر → باید پیام خطا بدهد (edit_task شما string خطا برمی‌گرداند)
    err = t2.edit_task(new_deadline="10-12-2025")
    assert "error" in err.lower()

    # حذف با شناسه
    ok = p.remove_task_by_id(t1.id)
    assert "removed successfully" in ok.lower()
    assert len(p.tasks) == 1

def test_project_create_edit_delete_cascade_and_uniqueness():
    mp = ManageProject()

    # ساخت دو پروژه با نام‌های یکتا
    assert "created successfully" in mp.create_project("Work", "desc").lower()
    assert "created successfully" in mp.create_project("Home", "desc").lower()

    # یکتا بودن نام (case-sensitive در پیاده‌سازی فعلی؛ همین را تست می‌کنیم)
    dup = mp.create_project("Work", "anything")
    assert "already exists" in dup

    # پیدا کردن پروژه اول با نام (برای Phase 1 کفایت می‌کند)
    p = next(p for p in mp.projects if p.name == "Work")
    # اضافه‌کردن task و سپس حذف پروژه → باید cascade پاک شوند
    p.add_task(Task("X", "x", None))
    assert len(p.tasks) == 1

    # اگر delete by ID را پیاده‌سازی کرده‌ای:
    #   msg = mp.delete_project_by_id(p.id)
    #   assert "deleted successfully" in msg.lower()
    # در غیر این صورت، حذف بر اساس نام:
    msg = mp.delete_project("Work")
    assert "deleted successfully" in msg.lower()

    # پروژه Work دیگر نباید وجود داشته باشد
    names = [pr.name for pr in mp.projects]
    assert "Work" not in names
