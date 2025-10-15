from __future__ import annotations
import os
from dotenv import load_dotenv


load_dotenv()

def _read_int(key: str, default: int) -> int:
    val = os.getenv(key)
    if val is None or not val.strip():
        return default
    try:
        return int(val)
    except ValueError:
        return default

MAX_NUMBER_OF_PROJECT = _read_int("MAX_NUMBER_OF_PROJECTS", 50)
MAX_NUMBER_OF_TASK    = _read_int("MAX_NUMBER_OF_TASKS", 500)
