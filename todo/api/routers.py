from fastapi import APIRouter
from .controllers import project_controller, task_controller, maintenance_controller

router = APIRouter()

# Projects
router.include_router(
    project_controller.router,
    prefix="/projects",
    tags=["Projects"],
)

# Tasks nested under projects
router.include_router(
    task_controller.router,
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"],
)

# Maintenance (autoclose)
router.include_router(
    maintenance_controller.router,
    prefix="/maintenance",
    tags=["Maintenance"],
)
