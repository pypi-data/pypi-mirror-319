import sqlite3
from contextlib import contextmanager
from queue import Queue
from typing import Optional, List, Tuple, Any
from datetime import datetime
import uuid
import threading

class ConnectionPool:
    def __init__(self, db_path: str, max_connections: int = 5):
        self.db_path = db_path
        self.max_connections = max_connections
        self._local = threading.local()
        self._lock = threading.Lock()
        self.active_connections = 0

    def _create_connection(self):
        with self._lock:
            if self.active_connections >= self.max_connections:
                raise Exception("Maximum connections reached")
            self.active_connections += 1
        
        try:
            return sqlite3.connect(self.db_path)
        
        except Exception:
            with self._lock:
                self.active_connections -= 1
            raise

    @contextmanager
    def get_connection(self):
        if not hasattr(self._local, 'connection'):
            self._local.connection = self._create_connection()
        
        try:
            yield self._local.connection

        except Exception as e:
            self._local.connection.rollback()
            raise e
        
        finally:
            if not hasattr(self._local, 'connection'):
                return
            
            with self._lock:
                self.active_connections -= 1

            if self.active_connections == 0:
                self._local.connection.close()
                delattr(self._local, 'connection')

    def close_all(self):
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            with self._lock:
                self.active_connections -= 1
            delattr(self._local, 'connection')


class BaseHandler:
    def __init__(self, pool: ConnectionPool):
        self.pool = pool

    @contextmanager
    def get_cursor(self):
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            finally:
                cursor.close()


class ClipboardHandler(BaseHandler):
    def __init__(self, db_path: str):
        pool = ConnectionPool(db_path)
        super().__init__(pool)
        self._create_table()

    def _create_table(self):
        with self.get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clipboard (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    pinned BOOLEAN DEFAULT FALSE
                )
            ''')

    def create(self, text: str, pinned: bool = False) -> str:
        new_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()

        with self.get_cursor() as cursor:
            cursor.execute(
                'INSERT INTO clipboard (id, text, created_at, pinned) VALUES (?, ?, ?, ?)',
                (new_id, text, created_at, pinned)
            )
        return new_id

    def read(self, clip_id: str) -> Optional[Tuple]:
        with self.get_cursor() as cursor:
            cursor.execute('SELECT * FROM clipboard WHERE id = ?', (clip_id,))
            row = cursor.fetchone()

        if row:
            return {
                "id": row[0],
                "text": row[1],
                "created_at": row[2],
                "pinned": row[3]
            }

    def update(self, clip_id: str, text: Optional[str] = None, pinned: Optional[bool] = None) -> bool:
        updates = []
        params = []
        if text is not None:
            updates.append("text = ?")
            params.append(text)
        if pinned is not None:
            updates.append("pinned = ?")
            params.append(pinned)
        
        if not updates:
            return False

        params.append(clip_id)
        query = f"UPDATE clipboard SET {', '.join(updates)} WHERE id = ?"
        
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount > 0

    def delete(self, clip_id: str) -> bool:
        with self.get_cursor() as cursor:
            cursor.execute('DELETE FROM clipboard WHERE id = ?', (clip_id,))
            return cursor.rowcount > 0


class JournalHandler(BaseHandler):
    def __init__(self, db_path: str):
        pool = ConnectionPool(db_path)
        super().__init__(pool)
        self._create_table()

    def _create_table(self):
        with self.get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS journal (
                    id TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL
                )
            ''')

    def create(self, query: str, session_id: str) -> str:
        new_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        with self.get_cursor() as cursor:
            cursor.execute(
                'INSERT INTO journal (id, query, session_id, created_at) VALUES (?, ?, ?, ?)',
                (new_id, query, session_id, created_at)
            )
        return new_id

    def read(self, journal_id: str) -> Optional[Tuple]:
        with self.get_cursor() as cursor:
            cursor.execute('SELECT * FROM journal WHERE id = ?', (journal_id,))
            row = cursor.fetchone()

        if row:
            return {
                "id": row[0],
                "query": row[1],
                "session_id": row[2],
                "created_at": row[3]
            }

    def update(self, journal_id: str, query: str) -> bool:
        with self.get_cursor() as cursor:
            cursor.execute(
                'UPDATE journal SET query = ? WHERE id = ?',
                (query, journal_id)
            )
            return cursor.rowcount > 0

    def delete(self, journal_id: str) -> bool:
        with self.get_cursor() as cursor:
            cursor.execute('DELETE FROM journal WHERE id = ?', (journal_id,))
            return cursor.rowcount > 0


class ConfigHandler(BaseHandler):
    def __init__(self, pool: ConnectionPool):
        super().__init__(pool)
        self._create_table()

    def _create_table(self):
        with self.get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            ''')

    def set(self, key: str, value: str) -> None:
        with self.get_cursor() as cursor:
            cursor.execute(
                'INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)',
                (key, value)
            )

    def get(self, key: str) -> Optional[str]:
        with self.get_cursor() as cursor:
            cursor.execute('SELECT value FROM config WHERE key = ?', (key,))
            result = cursor.fetchone()
            return result[0] if result else None