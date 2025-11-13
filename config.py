import os
from dotenv import load_dotenv

load_dotenv()

# Business limits
MAX_NUMBER_OF_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECTS", "100"))
MAX_NUMBER_OF_TASKS    = int(os.getenv("MAX_NUMBER_OF_TASKS", "1000"))

# Statuses
_raw_statuses = os.getenv("ALLOWED_STATUSES", "todo,doing,done,blocked")
ALLOWED_STATUSES = [s.strip().lower() for s in _raw_statuses.split(",") if s.strip()]

# DB config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "todolist")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")
DB_NAME = os.getenv("DB_NAME", "todolist")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)
