# ToDo List — Phase 1 (In-Memory, OOP)

## Run (Poetry)
poetry install --with dev
cp .env.example .env
poetry run python src/todo_list/main.py

## Env
- MAX_NUMBER_OF_PROJECT(S)
- MAX_NUMBER_OF_TASK(S)

## Features (Phase 1)
- Create / Edit / Delete Project (cascade on delete)
- Add / Edit / Delete Task, Change Status
- Status: todo | doing | done (lowercase, default todo)
- Deadline: ISO YYYY-MM-DD (optional; validated)
- Limits from .env (no hardcode)
- List projects (sorted by created_at)
- Show IDs; delete Project/Task by ID

## Dev
poetry run ruff check .
poetry run mypy src
poetry run pytest -q

## Notes
- Code under src/todo_list/
- .env is local-only; use .env.example as template
