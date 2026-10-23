"""Unit-Tests: einzelne Funktionen, ohne HTTP."""
import sqlite3

import pytest

import app as todo_app

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "value, expected",
    [
        ("abc", "abc"),
        ("  abc  ", "abc"),
        ("\tabc\n", "abc"),
        ("a  b", "a  b"),
        ("<b>x</b>", "<b>x</b>"),
        ("", None),
        ("   ", None),
        ("\n\t", None),
        (None, None),
        (5, None),
        (True, None),
        (["a"], None),
        ({"text": "a"}, None),
    ],
)
def test_clean_text(value, expected):
    assert todo_app.clean_text(value) == expected


def _row(id_, text, done):
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    return db.execute("SELECT ? AS id, ? AS text, ? AS done", (id_, text, done)).fetchone()


@pytest.mark.parametrize("done, expected", [(0, False), (1, True)])
def test_row_to_dict_wandelt_done_in_bool(done, expected):
    result = todo_app.row_to_dict(_row(7, "x", done))
    assert result == {"id": 7, "text": "x", "done": expected}
    assert isinstance(result["done"], bool)


def test_init_db_legt_tabelle_an(db_path):
    with sqlite3.connect(db_path) as db:
        cols = {r[1]: r for r in db.execute("PRAGMA table_info(todos)")}
    assert set(cols) == {"id", "text", "done"}
    assert cols["id"][5] == 1  # Primary Key
    assert cols["text"][3] == 1  # NOT NULL
    assert cols["done"][4] == "0"  # Default


def test_init_db_ist_idempotent_und_erhaelt_daten(db_path):
    with sqlite3.connect(db_path) as db:
        db.execute("INSERT INTO todos (text) VALUES ('a')")
    todo_app.init_db()
    with sqlite3.connect(db_path) as db:
        assert db.execute("SELECT COUNT(*) FROM todos").fetchone()[0] == 1


def test_db_path_nimmt_umgebungsvariable(tmp_path):
    import os
    import subprocess
    import sys

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target = str(tmp_path / "env.db")
    out = subprocess.run(
        [sys.executable, "-c", "import app; print(app.DB_PATH)"],
        cwd=root,
        env={**os.environ, "TODO_DB": target},
        capture_output=True,
        text=True,
        check=True,
    )
    assert out.stdout.strip() == target
    assert os.path.exists(target)  # init_db() legt die Datei beim Import an
