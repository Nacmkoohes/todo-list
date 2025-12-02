# Todo List – Phase 3 (Web API with FastAPI)

This project is a multi-phase Todo List application.  
Phase 1 and 2 implemented the core domain model and persistence layer (in-memory, then PostgreSQL with SQLAlchemy).  
**Phase 3** adds a full Web API on top of the existing services using **FastAPI**.

---

## Features (Phase 3)

- RESTful HTTP API for managing:
  - **Projects**
  - **Tasks** belonging to projects
- Layered architecture:
  - API (controllers + request/response schemas)
  - Services (business logic)
  - Repositories (data access)
  - Models (SQLAlchemy ORM)
- PostgreSQL + SQLAlchemy integration (from Phase 2)
- Pydantic v2 models for request/response validation
- Automatic OpenAPI documentation via FastAPI (`/docs`)

---

## Tech Stack

- Python 3.10
- FastAPI
- Uvicorn
- SQLAlchemy
- Psycopg2
- Pydantic v2
- PostgreSQL
- Alembic (migrations)
- Poetry (dependency management)

---

## Project Structure

```text
todo/                                 # Application Package

├── api                               # API Layer
│   ├── controllers                   # FastAPI controllers (HTTP endpoints)
│   │   ├── project_controller.py
│   │   ├── task_controller.py
│   │   └── __init__.py
│   │
│   ├── controller_schemas            # Pydantic models for input/output
│   │   ├── project_requests.py
│   │   ├── project_responses.py
│   │   ├── task_requests.py
│   │   ├── task_responses.py
│   │   └── __init__.py
│   │
│   ├── routers.py                    # Aggregates routers, prefix /api/v1
│   └── __init__.py
│
├── services                          # Business Logic Layer
│   ├── app_factory.py                # Creates service instances
│   ├── project_service.py            # Use-cases for projects
│   ├── task_service.py               # Use-cases for tasks
│   └── __init__.py
│
├── repositories                      # Data Access Layer
│   ├── project_repository.py         # ProjectRepository + SQLAlchemy impl
│   ├── task_repository.py            # TaskRepository + SQLAlchemy impl
│   └── __init__.py
│
├── models                            # ORM Models (SQLAlchemy)
│   ├── project.py                    # Project ORM model
│   ├── task.py                       # Task ORM model
│   └── __init__.py
│
├── db                                # Database setup & session
│   ├── base.py                       # Declarative Base
│   ├── session.py                    # Engine + SessionLocal
│   └── __init__.py
│
├── commands                          # CLI tools / background jobs
│   ├── autoclose_overdue.py          # Auto-close overdue tasks
│   └── scheduler.py                  # Optional scheduling utility
│
├── exceptions                        # Domain-specific exceptions
│   ├── service_exceptions.py
│   └── __init__.py
│
├── cli.py                            # CLI entrypoint from previous phases
├── config.py                         # Application configuration (limits, statuses)
└── __init__.py                       # Package marker
