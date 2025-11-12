# alembic/env.py
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv
import os

load_dotenv()

from todo.db.base import Base
from todo.models.project import Project  # noqa: F401
from todo.models.task import Task        # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER','todolist')}:"
    f"{os.getenv('DB_PASSWORD','secret')}@{os.getenv('DB_HOST','localhost')}:"
    f"{os.getenv('DB_PORT','5432')}/{os.getenv('DB_NAME','todolist')}"
)
config.set_main_option("sqlalchemy.url", DB_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
