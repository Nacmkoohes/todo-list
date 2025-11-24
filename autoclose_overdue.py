from __future__ import annotations

from todo.app_factory import build_services
from todo.repositories.task_repository import SqlAlchemyTaskRepository
from todo.db.session import SessionLocal


def run(dry_run: bool = False) -> int:
    """
    Find all overdue, non-done tasks and close them.

    dry_run=True  → فقط چاپ می‌کند، تغییری در DB نمی‌دهد.
    dry_run=False → واقعاً در DB status و closed_at را آپدیت می‌کند.
    """
    # سرویس‌ها و ریپو را بسازیم
    ps, ts = build_services()
    task_repo = SqlAlchemyTaskRepository(SessionLocal)

    # 1) کاندیدها (همون list_overdue_open)
    candidates = list(task_repo.list_overdue_open())
    if not candidates:
        print("No overdue open tasks.")
        return 0

    print("Overdue open tasks:")
    for t in candidates:
        print(f"- [#{t.id}] {t.title}  (status={t.status}, deadline={t.deadline})")

    if dry_run:
        print(f"\nDry-run: would close {len(candidates)} tasks, but no changes applied.")
        return 0

    # 2) واقعاً ببندیم
    affected = 0
    for t in candidates:
        ts.change_task_status(t.id, "done")  # یا task_repo.update(t.id, status="done", closed_at=now)
        affected += 1
        print(f"Closed: [#{t.id}] {t.title}")

    print(f"\nDone. Closed {affected} tasks.")
    return affected


if __name__ == "__main__":
    import sys
    dry = any(a in ("--dry", "--dry-run") for a in sys.argv[1:])
    run(dry_run=dry)
