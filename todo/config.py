from __future__ import annotations
import os
from typing import List

try:
    from dotenv import load_dotenv  # pip install python-dotenv
    load_dotenv()  # loads .env if present
except Exception:
    pass  # if dotenv not available, fall back to defaults

def _getint(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default

def _getlist(name: str, default_csv: str) -> List[str]:
    raw = os.getenv(name, default_csv)
    return [x.strip() for x in raw.split(",") if x.strip()]

MAX_NUMBER_OF_PROJECTS = _getint("MAX_NUMBER_OF_PROJECTS", 5)
MAX_NUMBER_OF_TASKS   = _getint("MAX_NUMBER_OF_TASKS", 20)
ALLOWED_STATUSES      = _getlist("ALLOWED_STATUSES", "todo,doing,done")
