"""
Alembic environment configuration for the ZAYVORA Knowledge Service.

The Knowledge service uses **two** storage backends:
- PostgreSQL (via SQLAlchemy) for Source Library, OCR, and Provenance models.
- Neo4j (schema-less graph DB) for the knowledge graph — Neo4j requires NO
  Alembic migrations; see migrations/README.md.

The database URL is read from ``ZAYVORA_KNOWLEDGE_DATABASE_URL`` first,
falling back to ``sqlalchemy.url`` in alembic.ini.

Import strategy:
  source.py defines Base.  ocr.py imports Base from app.models.source and
  registers its tables on the same metadata — importing both suffices.
"""
from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# ---------------------------------------------------------------------------
# Make the service's package importable
# ---------------------------------------------------------------------------
_SERVICE_ROOT = Path(__file__).resolve().parents[2]  # …/services/knowledge
if str(_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(_SERVICE_ROOT))

# ---------------------------------------------------------------------------
# Import models — ocr.py re-uses Base from source.py
# ---------------------------------------------------------------------------
from app.models.source import Base  # noqa: E402  # registers source library tables
import app.models.ocr  # noqa: E402, F401  # registers OCR + extraction tables

target_metadata = Base.metadata

# ---------------------------------------------------------------------------
# Alembic Config object
# ---------------------------------------------------------------------------
config = context.config

_db_url = os.environ.get(
    "ZAYVORA_KNOWLEDGE_DATABASE_URL",
    config.get_main_option("sqlalchemy.url"),
)
config.set_main_option("sqlalchemy.url", _db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Generate a SQL migration script without connecting to the DB."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Apply migrations against a live database connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
