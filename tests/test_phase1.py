# tests/test_phase1_full.py
import importlib
import pytest

# --- یک فیکسچر برای ست‌کردن سقف‌ها از طریق ENV و ریلود ماژول‌ها ---
@pytest.fixture
def M(monkeypatch):
    # سقف‌ها را کوچک می‌کنیم تا تست‌ها سریع و قابل پیش‌بینی باشند
    monkeypatch.setenv("MAX_NUMBER_OF_PROJECTS", "2")
    monkeypatch.setenv("MAX_NUMBER_OF_TASKS", "2")

    # ریلود config و main تا مقادیر جدید ENV اعمال شوند
    import todo_list.config as cfg
    import todo_list.main as m
    importlib.reload(cfg)
    importlib.reload(m)
    return m


# US1/US2/US3 — ساخت، یکتایی نام (case-insensitive)، سقف تعداد پروژه‌ها
def test_create_projects_and_limits_and_uniqueness(M):
    mp = M.ManageProject()

    # ساخت دو پروژه OK
    assert "created successfully" in mp.create_project("Work", "first").lower()
    assert "created successfully" in mp.create_project("Home", "second").lower()

    # نام تکراری (case-insensitive)
    assert "already exists" in mp.create_project("work", "dup").lower()

    # سقف پروژه‌ها
    assert "maximum number of projects" in mp.create_project("Extra", "x").lower()


# US4 — ویرایش پروژه (محدودیت‌ها + یکتایی + بدون تغییر)
def test_edit_project_paths(M):
    mp = M.ManageProject()
    mp.create_project("Work", "desc")
    mp.create_project("Home", "desc")

    # تغییر موفق
    msg_ok = mp.edit_project("Work", "Work v2", "new desc")
    assert "updated successfully" in msg_ok.lower()

    # یکتایی نام جدید (به "HOME")
    msg_dup = mp.edit_project("Work v2", "HOME", "x")
    assert "already exists" in msg_dup

    # بدون تغییر واقعی
    msg_noop = mp.edit_project("Work v2", "Work v2", "new desc")
    assert "no changes" in msg_noop.lower()

    # محدودیت طول نام
    long_name = "n " * 31
    assert "name must be <= 30 words" in mp.edit_project("Work v2", long_name, "d")

    # محدودیت طول توضیح
    long_desc = "d " * 151
    assert "description must be <= 150 words" in mp.edit_project("Work v2", "W3", long_desc)


# US5 — لیست پروژه‌ها به‌ترتیب created_at (جدیدترین اول)
def test_list_projects_sorted_by_created_at(M):
    mp = M.ManageProject()
    mp.create_project("P1", "d")
    mp.create_project("P2", "d")
    lst = mp.list_projects()
    assert isinstance(lst, list)
    # جدیدترین باید P2 باشد (به‌خاطر ساخته‌شدن بعدی)
    assert "Project Name: P2" in lst[0]
    assert "Project Name: P1" in lst[1]


# US6 — افزودن تسک (سقف، طول عنوان/توضیح، status/deadline)
def test_add_tasks_and_limits_and_validation(M):
    mp = M.ManageProject()
    mp.create_project("P", "d")
    p = next(p for p in mp.projects if p.name == "P")

    # status نرمال به lowercase و deadline ISO
    t1 = M.Task("Write tests", "pytest", "2025-12-01", "Doing")
    assert "added successfully" in p.add_task(t1).lower()
    assert t1.status == "doing"
    assert str(t1.deadline) == "2025-12-01"

    # پیش‌فرض status = todo و deadline None
    t2 = M.Task("Ship", "release", None)
    assert "added successfully" in p.add_task(t2).lower()
    assert t2.status == "todo"
    assert t2.deadline is None

    # سقف تسک‌ها
    t3 = M.Task("Extra", "x", "2025-12-02")
    assert "maximum number of tasks" in p.add_task(t3).lower()

    # deadline نامعتبر در سازنده → باید استثنا بدهد
    with pytest.raises(ValueError):
        M.Task("Bad", "date", "30-12-2025")


# US7 — تغییر وضعیت تسک + نرمال‌سازی
def test_task_change_status(M):
    t = M.Task("T", "d", "2025-01-01", "todo")
    assert "changed" in t.change_status("DONE").lower()
    assert t.status == "done"
    assert "invalid status" in t.change_status("in-progress").lower()


# US8 — ویرایش تسک (عنوان/توضیح/ددلاین/وضعیت) با اعتبارسنجی
def test_task_edit_validation(M):
    t = M.Task("A", "a", None, "doing")

    # عنوان بلند
    long_title = "t " * 31
    assert "title must be <= 30 words" in t.edit_task(new_title=long_title)

    # توضیح بلند
    long_desc = "d " * 151
    assert "description must be <= 150 words" in t.edit_task(new_description=long_desc)

    # deadline نامعتبر → پیام خطا
    assert "deadline must be in yyyy-mm-dd" in t.edit_task(new_deadline="2025/12/30").lower()

    # status نامعتبر
    assert "status is invalid" in t.edit_task(new_status="blocked").lower()

    # تغییرات معتبر
    ok = t.edit_task(new_title="B", new_description="bb", new_deadline="2025-12-30", new_status="Done")
    assert "updated successfully" in ok.lower()
    assert t.title == "B" and t.description == "bb" and str(t.deadline) == "2025-12-30" and t.status == "done"


# US9 — حذف تسک/پروژه بر اساس شناسه (ID) + Cascade
def test_delete_by_id_and_cascade(M):
    mp = M.ManageProject()
    mp.create_project("P", "d")
    p = next(p for p in mp.projects if p.name == "P")

    t1 = M.Task("X", "x", None)
    t2 = M.Task("Y", "y", None)
    p.add_task(t1)
    p.add_task(t2)
    assert len(p.tasks) == 2

    # حذف تسک با ID
    msg = p.remove_task_by_id(t1.id)
    assert "removed successfully" in msg.lower()
    assert len(p.tasks) == 1 and p.tasks[0].title == "Y"

    # حذف پروژه با ID → باید Cascade شود
    msg2 = mp.delete_project_by_id(p.id)
    assert "deleted successfully" in msg2.lower()
    assert all(pr.id != p.id for pr in mp.projects)
