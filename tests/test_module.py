"""Modul-Tests: API-Endpunkte zusammen mit SQLite über den Flask-Test-Client."""
import sqlite3

import pytest

pytestmark = pytest.mark.module


def add(client, text="a"):
    r = client.post("/api/todos", json={"text": text})
    assert r.status_code == 201
    return r.json


def rows(db_path):
    with sqlite3.connect(db_path) as db:
        return db.execute("SELECT id, text, done FROM todos ORDER BY id").fetchall()


# --- GET /api/todos ---

def test_liste_ist_anfangs_leer(client):
    r = client.get("/api/todos")
    assert r.status_code == 200
    assert r.json == []


def test_liste_ist_nach_id_sortiert(client):
    for t in ["c", "a", "b"]:
        add(client, t)
    assert [t["text"] for t in client.get("/api/todos").json] == ["c", "a", "b"]


# --- POST /api/todos ---

def test_anlegen_liefert_201_und_objekt(client):
    r = client.post("/api/todos", json={"text": "Milch"})
    assert r.status_code == 201
    assert r.json == {"id": 1, "text": "Milch", "done": False}


def test_anlegen_trimmt_text_und_speichert_in_db(client, db_path):
    add(client, "  Brot  ")
    assert rows(db_path) == [(1, "Brot", 0)]


@pytest.mark.parametrize("body", [{}, {"text": ""}, {"text": "   "}, {"text": None}, {"text": 5}, {"foo": "x"}])
def test_anlegen_ungueltig_gibt_400(client, db_path, body):
    r = client.post("/api/todos", json=body)
    assert r.status_code == 400
    assert "error" in r.json
    assert rows(db_path) == []


def test_anlegen_ohne_json_gibt_400(client):
    assert client.post("/api/todos", data="kein json").status_code == 400
    assert client.post("/api/todos", data="{kaputt", content_type="application/json").status_code == 400


def test_html_im_text_bleibt_unveraendert(client):
    t = add(client, "<script>alert(1)</script>")
    assert t["text"] == "<script>alert(1)</script>"


def test_sql_injection_im_text_ist_wirkungslos(client, db_path):
    add(client, "'); DROP TABLE todos; --")
    assert rows(db_path) == [(1, "'); DROP TABLE todos; --", 0)]


def test_unicode_text(client):
    assert add(client, "Äpfel 🍎 日本語")["text"] == "Äpfel 🍎 日本語"


def test_ids_werden_nicht_wiederverwendet(client):
    first = add(client, "a")
    client.delete(f"/api/todos/{first['id']}")
    assert add(client, "b")["id"] == first["id"] + 1


# --- PATCH /api/todos/<id> ---

def test_done_aendern_laesst_text_unveraendert(client):
    t = add(client, "x")
    r = client.patch(f"/api/todos/{t['id']}", json={"done": True})
    assert r.status_code == 200
    assert r.json == {"id": t["id"], "text": "x", "done": True}


def test_text_aendern_laesst_done_unveraendert(client):
    t = add(client, "x")
    client.patch(f"/api/todos/{t['id']}", json={"done": True})
    r = client.patch(f"/api/todos/{t['id']}", json={"text": "  y "})
    assert r.json == {"id": t["id"], "text": "y", "done": True}


def test_done_wieder_zuruecksetzen(client):
    t = add(client)
    client.patch(f"/api/todos/{t['id']}", json={"done": True})
    r = client.patch(f"/api/todos/{t['id']}", json={"done": False})
    assert r.json["done"] is False


def test_text_und_done_gleichzeitig(client):
    t = add(client, "x")
    r = client.patch(f"/api/todos/{t['id']}", json={"text": "y", "done": True})
    assert r.json == {"id": t["id"], "text": "y", "done": True}


def test_leerer_patch_aendert_nichts(client):
    t = add(client, "x")
    r = client.patch(f"/api/todos/{t['id']}", json={})
    assert r.status_code == 200
    assert r.json == t


@pytest.mark.parametrize("body", [{"text": ""}, {"text": "  "}, {"text": None}, {"text": 1}])
def test_patch_mit_ungueltigem_text_gibt_400(client, db_path, body):
    t = add(client, "x")
    assert client.patch(f"/api/todos/{t['id']}", json=body).status_code == 400
    assert rows(db_path) == [(1, "x", 0)]


@pytest.mark.parametrize("value", ["true", 1, 0, None, [], "x"])
def test_patch_mit_nicht_booleschem_done_gibt_400(client, db_path, value):
    t = add(client)
    assert client.patch(f"/api/todos/{t['id']}", json={"done": value}).status_code == 400
    assert rows(db_path)[0][2] == 0


def test_patch_fehler_aendert_nichts_teilweise(client, db_path):
    t = add(client, "x")
    r = client.patch(f"/api/todos/{t['id']}", json={"text": "neu", "done": "kaputt"})
    assert r.status_code == 400
    assert rows(db_path) == [(1, "x", 0)]


def test_patch_unbekannte_id_gibt_404(client):
    r = client.patch("/api/todos/99", json={"done": True})
    assert r.status_code == 404
    assert "error" in r.json


def test_patch_trifft_nur_die_gewaehlte_aufgabe(client):
    a, b = add(client, "a"), add(client, "b")
    client.patch(f"/api/todos/{a['id']}", json={"done": True})
    assert [t["done"] for t in client.get("/api/todos").json] == [True, False]


# --- DELETE /api/todos/<id> ---

def test_loeschen_gibt_204_und_entfernt_zeile(client, db_path):
    t = add(client)
    r = client.delete(f"/api/todos/{t['id']}")
    assert r.status_code == 204
    assert r.data == b""
    assert rows(db_path) == []


def test_loeschen_trifft_nur_die_gewaehlte_aufgabe(client):
    a, b = add(client, "a"), add(client, "b")
    client.delete(f"/api/todos/{a['id']}")
    assert [t["text"] for t in client.get("/api/todos").json] == ["b"]


def test_loeschen_unbekannte_id_gibt_404(client):
    assert client.delete("/api/todos/99").status_code == 404


def test_zweimal_loeschen_gibt_beim_zweiten_mal_404(client):
    t = add(client)
    assert client.delete(f"/api/todos/{t['id']}").status_code == 204
    assert client.delete(f"/api/todos/{t['id']}").status_code == 404


# --- Routing ---

@pytest.mark.parametrize("method, path", [
    ("put", "/api/todos"),
    ("delete", "/api/todos"),
    ("post", "/api/todos/1"),
    ("get", "/api/todos/1"),
])
def test_nicht_erlaubte_methoden_geben_405(client, method, path):
    assert getattr(client, method)(path).status_code == 405


@pytest.mark.parametrize("path", ["/api/todos/abc", "/api/todos/1.5", "/api/unbekannt", "/nope"])
def test_unbekannte_pfade_geben_404(client, path):
    assert client.get(path).status_code == 404


def test_startseite_liefert_frontend(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.mimetype == "text/html"
    html = r.get_data(as_text=True)
    assert "<title>Todo App</title>" in html
    assert "/api/todos" in html


# --- Datenbankverbindung ---

def test_daten_ueberleben_neue_requests(client):
    add(client, "bleibt")
    assert [t["text"] for t in client.get("/api/todos").json] == ["bleibt"]


def test_verbindung_wird_nach_request_geschlossen(client, monkeypatch):
    import app as todo_app

    opened = []
    real_connect = sqlite3.connect

    class Spy:
        def __init__(self, conn):
            self.conn = conn
            self.closed = False
            opened.append(self)

        def close(self):
            self.closed = True
            self.conn.close()

        def __getattr__(self, name):
            return getattr(self.conn, name)

        def __setattr__(self, name, value):
            if name in ("conn", "closed"):
                object.__setattr__(self, name, value)
            else:
                setattr(self.conn, name, value)

    monkeypatch.setattr(todo_app.sqlite3, "connect", lambda *a, **k: Spy(real_connect(*a, **k)))
    client.get("/api/todos")
    assert opened and all(s.closed for s in opened)
