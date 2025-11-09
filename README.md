# ToDo List — Phase 1 (Python, Layered, In-Memory)

A clean, **layered** CLI ToDo app written in Python.  
Phase 1 focuses on **business logic separation** from I/O and storage, **in-memory repositories**, and a simple **interactive CLI** that covers **9 user stories** end-to-end.

---

## Highlights

- **Layered architecture**: Presentation (CLI) ⇢ Services (business rules) ⇢ Repositories/Stores (data)
- **9 complete user stories**:
  1) Create Project  
  2) List Projects  
  3) Edit Project  
  4) Delete Project  
  5) Add Task  
  6) List Tasks (per project)  
  7) Change Task Status (strictly validated)  
  8) Edit Task  
  9) Delete Task
- **Config via `.env`** (no hard-coding)
- **Sequential numeric IDs** (projects start at 1; tasks start at 1 per project)
- **English, menu-driven CLI** with tidy ASCII tables
- **Easy to swap storage later** (JSON/DB in Phase 2) thanks to repository interfaces

---



**Separation of concerns**:
- `services/` contain **only** business rules (limits, validation, status changes, etc.).
- `in_memory_store.py` contains **only** CRUD/storage details.
- `cli.py` handles **only** user interaction (input/print) and calls services.
- `config.py` centralizes environment-based configuration.

---

## ⚙️ Requirements

- Python **3.10+**
- (Optional) `python-dotenv` if you use a `.env` file

Install:
'''bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt # if provided (or: pip install python-dotenv)

## 🔧Configuration
Create a .env (or edit .env.example and copy it):
MAX_NUMBER_OF_PROJECTS=5
MAX_NUMBER_OF_TASKS=20
ALLOWED_STATUSES=todo,doing,done
Do not commit your real .env (it’s ignored by .gitignore).
The app reads these values at runtime. Defaults apply if not provided.

## ▶️ Run (Interactive CLI)
From the repository root:
python main.py

