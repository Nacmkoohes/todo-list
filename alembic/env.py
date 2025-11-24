from __future__ import annotations

import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from todo.db.base import Base
from todo.models.project import Project  # noqa: F401
from todo.models.task import Task        # noqa: F401

# این همون config Alembic هست
config = context.config

# لاگینگ از روی alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")

# ======  اینجا مستقیم URL درست رو می‌نویسیم  ======
DB_URL = "postgresql+psycopg2://todolist:secret@127.0.0.1:5433/todolist"
print("=== DB_URL used by Alembic ===")
print(DB_URL)
# =====================================

# متادیتای مدل‌ها برای autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = DB_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        DB_URL,
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
