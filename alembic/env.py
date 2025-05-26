from __future__ import annotations

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from db.base import Base
from db import models  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Interpret the config file for Python logging.
# Add your model's MetaData object here for 'autogenerate' support.
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = os.getenv("DATABASE_URL")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    connectable = engine_from_config(
        configuration,
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
