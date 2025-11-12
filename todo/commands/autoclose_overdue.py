# todo/commands/autoclose_overdue.py
from __future__ import annotations
from datetime import datetime, timezone

from todo.app_factory import build_services
from todo.db.session import SessionLocal

def run(dry_run: bool = False) -> int:
    """
    Close overdue tasks: if deadline < now and status != 'done',
    set status='done' and closed_at=now.
    Returns number of affected tasks.
    """
    project_service, task_service = build_services()

    from todo.repositories.task_repository import SqlAlchemyTaskRepository
    task_repo = SqlAlchemyTaskRepository(SessionLocal)

    candidates = task_repo.list_overdue_open(SessionLocal)
    if not candidates:
        print("No overdue open tasks.")
        return 0

    print(f"Found {len(candidates)} overdue open tasks.")
    affected = 0
    now = datetime.now(timezone.utc)

    for t in candidates:
        if dry_run:
            print(f"DRY-RUN would close: [#{t.id}] {t.title} (deadline={t.deadline})")
            continue
        task_service.edit_task(t.id, status="done")
        affected += 1
        print(f"Closed: [#{t.id}] {t.title}")

    if dry_run:
        print("Dry-run done. No changes committed.")
        return 0

    print(f"Done. Closed {affected} tasks.")
    return affected


if __name__ == "__main__":
    import sys
    dry = "--dry" in sys.argv or "--dry-run" in sys.argv
    run(dry_run=dry)
