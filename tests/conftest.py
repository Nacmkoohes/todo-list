# tests/conftest.py
import os, sys, pathlib, importlib

# ریشهٔ ریپو را به مسیر import اضافه کن
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# تنظیم پیش‌فرض‌های محیط برای تست‌ها (در صورت نیاز)
os.environ.setdefault("MAX_NUMBER_OF_PROJECTS", "3")
os.environ.setdefault("MAX_NUMBER_OF_TASKS", "5")
os.environ.setdefault("ALLOWED_STATUSES", "todo,doing,done")

# config را بعد از ست کردن env ها reload کن
import config
importlib.reload(config)
