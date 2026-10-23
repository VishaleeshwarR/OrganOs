"""
TransplantLink Repository Base Layer
Supports both local SQLite database (with JSON support) and Supabase client.
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(__file__).resolve().parent.parent / "transplantlink.db"
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()


def get_sqlite_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


_SUPABASE_WARNED = False


class BaseRepository:
    def __init__(self):
        # Strictly use local high-performance SQLite database
        self.use_supabase = False
        self._supabase_client = None

    def get_connection(self) -> sqlite3.Connection:
        return get_sqlite_connection()

    def parse_json_field(self, value: Any, default: Any = None) -> Any:
        if value is None:
            return default if default is not None else {}
        if isinstance(value, (dict, list)):
            return value
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return default if default is not None else {}
        return default if default is not None else {}
