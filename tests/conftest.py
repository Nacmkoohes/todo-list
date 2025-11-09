from project_service import ProjectService
from task_service import TaskService

# سرویس‌ها خودشان in-memory store می‌سازند
ps = ProjectService()
p = ps.create_project("Proj A")

ts = TaskService(project_store=ps.project_store)  # به همان پروژه‌ها وصلش کن
t1 = ts.add_task(p.id, "Write tests")
t2 = ts.add_task(p.id, "Refactor services")

print([t.title for t in ts.list_tasks(p.id)])  # ['Write tests', 'Refactor services']

ts.change_status(p.id, t1.id, "doing")
ts.edit_task(p.id, t2.id, title="Refactor services (clean)")
ts.delete_task(p.id, t1.id)

print([(t.title, t.status) for t in ts.list_tasks(p.id)])  # فقط تسک دوم با status پیش‌فرض
