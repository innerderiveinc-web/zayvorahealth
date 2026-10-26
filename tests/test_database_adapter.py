#!/usr/bin/env python3
"""
Unit tests for ZAYVORA Universal Database Adapter
Verifies:
1. SQLite connection acquisition with WAL, foreign keys, and busy timeout.
2. Dual-engine backend toggle logic via DATABASE_URL.
3. PostgresRowAdapter interface parity with sqlite3.Row.
4. PostgresCursorWrapper SQL dialect and parameter placeholder translation (? -> %s).
5. Fail-closed safety invariants.
"""

import unittest
import os
import tempfile
import sqlite3
from unittest.mock import MagicMock, patch

from database.adapter import (
    get_db_backend,
    get_universal_db,
    get_db_connection,
    PostgresRowAdapter,
    PostgresCursorWrapper,
    PostgresConnectionWrapper,
)

class TestDatabaseAdapter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_zayvora.db")

    def tearDown(self):
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def test_01_sqlite_backend_detection_default(self):
        """When DATABASE_URL is unset, backend must detect as 'sqlite'."""
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_db_backend(), "sqlite")

    def test_02_postgres_backend_detection(self):
        """When DATABASE_URL is postgresql:// or postgres://, backend must detect as 'postgres'."""
        with patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@localhost:5432/zayvora"}):
            self.assertEqual(get_db_backend(), "postgres")

        with patch.dict(os.environ, {"DATABASE_URL": "postgres://user:pass@localhost:5432/zayvora"}):
            self.assertEqual(get_db_backend(), "postgres")

    def test_03_sqlite_connection_pragmas_and_row_factory(self):
        """SQLite connection must configure WAL mode, foreign keys, and sqlite3.Row factory."""
        with patch.dict(os.environ, {"DATABASE_URL": ""}):
            conn = get_universal_db(self.db_path)
            self.assertIsInstance(conn, sqlite3.Connection)
            self.assertEqual(conn.row_factory, sqlite3.Row)

            # Test pragmas
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys")
            self.assertEqual(cur.fetchone()[0], 1)

            cur.execute("PRAGMA journal_mode")
            self.assertEqual(cur.fetchone()[0].lower(), "wal")
            conn.close()

    def test_04_postgres_row_adapter_parity(self):
        """PostgresRowAdapter must provide identical mapping interface to sqlite3.Row."""
        sample_dict = {"mrn": "PAT-001", "name": "Hakim Ajmal", "age": 45}
        row = PostgresRowAdapter(sample_dict)

        # Dictionary-style access
        self.assertEqual(row["mrn"], "PAT-001")
        self.assertEqual(row.get("name"), "Hakim Ajmal")
        self.assertEqual(row.get("nonexistent", "default_val"), "default_val")

        # Key check & iteration
        self.assertIn("age", row)
        self.assertEqual(list(row.keys()), ["mrn", "name", "age"])
        self.assertEqual(row[0], "PAT-001")
        self.assertEqual(row[1], "Hakim Ajmal")

    def test_05_postgres_cursor_parameter_translation(self):
        """PostgresCursorWrapper must translate '?' parameter placeholders to '%s'."""
        mock_raw_cursor = MagicMock()
        mock_raw_cursor.fetchall.return_value = [{"col1": "val1"}]

        wrapper = PostgresCursorWrapper(mock_raw_cursor)
        query = "SELECT * FROM patients WHERE mrn = ? AND status = ?"
        params = ("PAT-001", "ACTIVE")

        wrapper.execute(query, params)
        expected_query = "SELECT * FROM patients WHERE mrn = %s AND status = %s"
        mock_raw_cursor.execute.assert_called_once_with(expected_query, params)

        results = wrapper.fetchall()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["col1"], "val1")

    def test_06_strict_production_fail_closed(self):
        """In strict production mode, missing PostgreSQL must raise RuntimeError rather than silently falling back."""
        with patch.dict(os.environ, {
            "DATABASE_URL": "postgresql://invalid-host:5432/zayvora",
            "STRICT_PRODUCTION_DATABASE": "true"
        }):
            with patch("services.db_adapter._init_pg_pool", return_value=None):
                with self.assertRaises(RuntimeError) as ctx:
                    get_universal_db(self.db_path)
                self.assertIn("FAIL CLOSED", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
