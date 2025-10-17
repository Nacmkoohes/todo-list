import importlib
import pytest

@pytest.fixture
def M(monkeypatch):
    # سقف‌ها برای سرعت تست
    monkeypatch.setenv("MAX_NUMBER_OF_PROJECTS", "5")
    monkeypatch.setenv("MAX_NUMBER_OF_TASKS", "5")
    import todo_list.config as cfg
    import todo_list.main as m
    importlib.reload(cfg)
    importlib.reload(m)
    return m

def test_lookup_by_name_index_create_edit_delete(M):
    mp = M.ManageProject()

    # create → index set
    assert "created successfully" in mp.create_project("Work", "d").lower()
    assert mp.get_project_by_name("work") is not None
    assert mp.get_project_by_name("  WORK ") is not None

    # duplicate via index
    assert "already exists" in mp.create_project("WORK", "dup")

    # edit → index key updated
    assert "updated successfully" in mp.edit_project("Work", "Work v2", "dd").lower()
    assert mp.get_project_by_name("work") is None
    assert mp.get_project_by_name("work v2") is not None

    # delete → index key removed
    assert "deleted successfully" in mp.delete_project("work v2").lower()
    assert mp.get_project_by_name("work v2") is None
