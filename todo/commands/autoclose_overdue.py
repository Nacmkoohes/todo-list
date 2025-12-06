from __future__ import annotations
from datetime import datetime
from todo.services.app_factory import build_services
from todo.repositories.task_repository import SqlAlchemyTaskRepository
from todo.db.session import SessionLocal
import sys


def run(dry_run: bool = False) -> int:
    # Build the service instances
    ps, ts = build_services()
    task_repo = SqlAlchemyTaskRepository(SessionLocal)

    # Get the overdue tasks
    candidates = list(task_repo.list_overdue_open())  # ✅ Sized
    if not candidates:
        print("No overdue open tasks.")
        return 0

    print(f"Found {len(candidates)} overdue open tasks.")
    affected = 0

    for t in candidates:
        if dry_run:
            print(f"DRY-RUN would close: [#{t.id}] {t.title} (deadline={t.deadline})")
            continue

        # Update task to 'done' status and set closed_at
        ts.update_task_status(
            task_id=t.id,
            status="done",
            closed_at=datetime.utcnow()
        )

        print(f"Closed: [#{t.id}] {t.title}")
        affected += 1

    if dry_run:
        print("Dry-run done. No changes committed.")
        return 0

    print(f"Done. Closed {affected} tasks.")
    return affected


if __name__ == "__main__":
    dry = any(a in ("--dry", "--dry-run") for a in sys.argv[1:])
    run(dry_run=dry)
