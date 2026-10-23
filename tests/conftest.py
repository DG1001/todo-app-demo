import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import app as todo_app  # noqa: E402


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    """Leere SQLite-Datei pro Test; die echte todos.db bleibt unberührt."""
    path = str(tmp_path / "test.db")
    monkeypatch.setattr(todo_app, "DB_PATH", path)
    todo_app.init_db()
    return path


@pytest.fixture
def client(db_path):
    todo_app.app.config["TESTING"] = True
    return todo_app.app.test_client()
