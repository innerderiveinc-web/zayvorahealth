"""
ZAYVORA Universal Database Adapter
Dual-Engine: High-Performance SQLite (Local/Edge/Offline) & PostgreSQL (Enterprise Multi-Hospital)
Automatically toggles via DATABASE_URL environment variable.
"""

import os
import sqlite3
import threading
import logging

logger = logging.getLogger("zayvora.db")

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
DB_BACKEND = "postgres" if (DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://")) else "sqlite"

_pg_pool = None
_pool_lock = threading.Lock()

def get_db_backend():
    return DB_BACKEND

class PostgresRowAdapter:
    """Wraps psycopg2 dictionary/named tuple rows to behave identically to sqlite3.Row."""
    def __init__(self, data_dict):
        self._data = data_dict or {}

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self._data.values())[key]
        return self._data.get(key)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __iter__(self):
        return iter(self._data.keys())

    def __contains__(self, key):
        return key in self._data

    def __repr__(self):
        return f"<PostgresRow {self._data}>"

class PostgresCursorWrapper:
    """Translates '?' parameter syntax to '%s' and provides sqlite3 cursor compatibility."""
    def __init__(self, pg_cursor):
        self._cursor = pg_cursor

    def execute(self, query, params=None):
        # Convert SQLite parameter placeholder '?' to PostgreSQL '%s'
        pg_query = query.replace("?", "%s")
        # Handle SQLite-specific INSERT OR REPLACE syntax
        if "INSERT OR REPLACE INTO" in pg_query:
            pg_query = pg_query.replace("INSERT OR REPLACE INTO", "INSERT INTO")
        if params is not None:
            self._cursor.execute(pg_query, params)
        else:
            self._cursor.execute(pg_query)
        return self

    def executemany(self, query, params_list):
        pg_query = query.replace("?", "%s")
        self._cursor.executemany(pg_query, params_list)
        return self

    def fetchone(self):
        row = self._cursor.fetchone()
        if row is None:
            return None
        return PostgresRowAdapter(dict(row))

    def fetchall(self):
        rows = self._cursor.fetchall()
        return [PostgresRowAdapter(dict(r)) for r in rows]

    def fetchmany(self, size=None):
        rows = self._cursor.fetchmany(size)
        return [PostgresRowAdapter(dict(r)) for r in rows]

    @property
    def rowcount(self):
        return self._cursor.rowcount

    @property
    def lastrowid(self):
        return getattr(self._cursor, "lastrowid", None)

    def close(self):
        self._cursor.close()

class PostgresConnectionWrapper:
    """Wraps a psycopg2 pooled connection to provide context management and cursor compatibility."""
    def __init__(self, raw_conn, pool=None):
        self._conn = raw_conn
        self._pool = pool

    def cursor(self):
        import psycopg2.extras
        cur = self._conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return PostgresCursorWrapper(cur)

    def execute(self, query, params=None):
        cur = self.cursor()
        cur.execute(query, params)
        return cur

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        if self._pool:
            self._pool.putconn(self._conn)
        else:
            self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.close()

def _init_pg_pool():
    global _pg_pool
    if _pg_pool is None:
        with _pool_lock:
            if _pg_pool is None:
                try:
                    import psycopg2.pool
                    url = DATABASE_URL
                    # Fix Heroku/Railway 'postgres://' format to 'postgresql://' if needed
                    if url.startswith("postgres://"):
                        url = "postgresql://" + url[len("postgres://"):]
                    _pg_pool = psycopg2.pool.ThreadedConnectionPool(minconn=2, maxconn=30, dsn=url)
                    logger.info("ZAYVORA Universal Database Adapter: PostgreSQL ThreadedConnectionPool Initialized.")
                except ImportError:
                    logger.warning("psycopg2 not installed. Falling back to SQLite.")
                    return None
                except Exception as e:
                    logger.error(f"PostgreSQL connection failed ({e}). Falling back to SQLite.")
                    return None
    return _pg_pool

def get_universal_db(db_path):
    """
    Returns an active database connection context.
    If DATABASE_URL is configured and psycopg2 is available -> PostgreSQL.
    Otherwise -> SQLite.
    """
    if DB_BACKEND == "postgres":
        pool = _init_pg_pool()
        if pool:
            try:
                raw_conn = pool.getconn()
                return PostgresConnectionWrapper(raw_conn, pool)
            except Exception as e:
                logger.error(f"Error leasing PG connection: {e}. Falling back to SQLite.")

    # SQLite Fallback Engine
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable Write-Ahead Logging (WAL) for 10x higher concurrency in SQLite
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn
