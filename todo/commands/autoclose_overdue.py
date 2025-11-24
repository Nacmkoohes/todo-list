from __future__ import annotations
# from datetime import datetime, timezone
from todo.app_factory import build_services
from todo.repositories.task_repository import SqlAlchemyTaskRepository
from todo.db.session import SessionLocal
from datetime import datetime


def run(dry_run: bool = False) -> int:
    ps, ts = build_services()
    task_repo = SqlAlchemyTaskRepository(SessionLocal)

    candidates = list(task_repo.list_overdue_open())  # ✅ Sized شد
    if not candidates:
        print("No overdue open tasks.")
        return 0

    print(f"Found {len(candidates)} overdue open tasks.")
    affected = 0
    for t in candidates:
        if dry_run:
            print(f"DRY-RUN would close: [#{t.id}] {t.title} (deadline={t.deadline})")
            continue
        ts.task_store.update(t.id, status="done", closed_at=datetime.utcnow())
        print(f"Closed: [#{t.id}] {t.title}")
        affected += 1

    if dry_run:
        print("Dry-run done. No changes committed.")
        return 0

    print(f"Done. Closed {affected} tasks.")
    return affected

if __name__ == "__main__":
    import sys
    dry = any(a in ("--dry", "--dry-run") for a in sys.argv[1:])
    run(dry_run=dry)
