import pytest
import os
import sqlite3
from datetime import datetime
from clipthread.core.db import ConnectionPool, ClipboardHandler, JournalHandler, ConfigHandler

@pytest.fixture
def db_path():
    path = "test.db"
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture 
def pool(db_path):
    return ConnectionPool(db_path)

@pytest.fixture
def clipboard_handler(db_path):
    return ClipboardHandler(db_path)

@pytest.fixture
def journal_handler(db_path):
    return JournalHandler(db_path)

@pytest.fixture
def config_handler(pool):
    return ConfigHandler(pool)

class TestConnectionPool:
    def test_init(self, pool):
        assert pool.db_path == "test.db"
        assert pool.max_connections == 5
        assert pool.active_connections == 0

    def test_create_connection(self, pool):
        conn = pool._create_connection()
        assert isinstance(conn, sqlite3.Connection)
        assert pool.active_connections == 1
        conn.close()

    def test_max_connections(self, pool):
        connections = []
        for _ in range(5):
            connections.append(pool._create_connection())
        
        with pytest.raises(Exception, match="Maximum connections reached"):
            pool._create_connection()

        for conn in connections:
            conn.close()

class TestClipboardHandler:
    def test_create(self, clipboard_handler):
        clip_id = clipboard_handler.create("test text")
        assert isinstance(clip_id, str)
        
        result = clipboard_handler.read(clip_id)
        assert result["text"] == "test text"
        assert result["pinned"] == False

    def test_read_nonexistent(self, clipboard_handler):
        result = clipboard_handler.read("nonexistent")
        assert result is None

    def test_update(self, clipboard_handler):
        clip_id = clipboard_handler.create("original")
        
        assert clipboard_handler.update(clip_id, text="updated")
        result = clipboard_handler.read(clip_id)
        assert result["text"] == "updated"

        assert clipboard_handler.update(clip_id, pinned=True)
        result = clipboard_handler.read(clip_id)
        assert result["pinned"] == True

    def test_delete(self, clipboard_handler):
        clip_id = clipboard_handler.create("test")
        assert clipboard_handler.delete(clip_id)
        assert clipboard_handler.read(clip_id) is None

class TestJournalHandler:
    def test_create(self, journal_handler):
        journal_id = journal_handler.create("test query", "session1")
        assert isinstance(journal_id, str)
        
        result = journal_handler.read(journal_id)
        assert result["query"] == "test query"
        assert result["session_id"] == "session1"

    def test_read_nonexistent(self, journal_handler):
        result = journal_handler.read("nonexistent")
        assert result is None

    def test_update(self, journal_handler):
        journal_id = journal_handler.create("original", "session1")
        
        assert journal_handler.update(journal_id, "updated")
        result = journal_handler.read(journal_id)
        assert result["query"] == "updated"

    def test_delete(self, journal_handler):
        journal_id = journal_handler.create("test", "session1")
        assert journal_handler.delete(journal_id)
        assert journal_handler.read(journal_id) is None

class TestConfigHandler:
    def test_set_get(self, config_handler):
        config_handler.set("test_key", "test_value")
        assert config_handler.get("test_key") == "test_value"

    def test_get_nonexistent(self, config_handler):
        assert config_handler.get("nonexistent") is None

    def test_overwrite(self, config_handler):
        config_handler.set("test_key", "original")
        config_handler.set("test_key", "updated")
        assert config_handler.get("test_key") == "updated"