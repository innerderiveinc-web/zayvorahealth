"""
ZAYVORA Health OS — Enterprise Database Adapter Export
Dual-Engine: High-Performance SQLite (Local/Edge/Offline) & PostgreSQL (Cloud-Scale)
"""

from services.db_adapter import (
    get_db_backend,
    get_universal_db,
    PostgresRowAdapter,
    PostgresCursorWrapper,
    PostgresConnectionWrapper,
)

# Standard alias for direct connection acquisition
get_db_connection = get_universal_db

__all__ = [
    "get_db_backend",
    "get_universal_db",
    "get_db_connection",
    "PostgresRowAdapter",
    "PostgresCursorWrapper",
    "PostgresConnectionWrapper",
]
