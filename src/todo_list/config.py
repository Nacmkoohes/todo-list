from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

def _read_int_multi(keys: list[str], default: int) -> int:
    for key in keys:
        val = os.getenv(key)
        if val is None or not val.strip():
            continue
        try:
            return int(val)
        except ValueError:
            continue
    return default


MAX_NUMBER_OF_PROJECT = _read_int_multi(
    ["MAX_NUMBER_OF_PROJECT", "MAX_NUMBER_OF_PROJECTS"], 50
)
MAX_NUMBER_OF_TASK = _read_int_multi(
    ["MAX_NUMBER_OF_TASK", "MAX_NUMBER_OF_TASKS"], 500
)

# alias ها (تا اگر در کد جمع ایمپورت شد، کار کند)
MAX_NUMBER_OF_PROJECTS = MAX_NUMBER_OF_PROJECT
MAX_NUMBER_OF_TASKS = MAX_NUMBER_OF_TASK
