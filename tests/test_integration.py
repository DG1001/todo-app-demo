"""Integrationstests: echter Server-Prozess, HTTP-Zugriff und Persistenz."""
import urllib.request

import pytest

pytestmark = pytest.mark.integration


def test_startseite_und_api_ueber_http(server):
    with urllib.request.urlopen(server.base + "/") as r:
        assert r.status == 200
        assert r.headers.get_content_type() == "text/html"
        assert "Todo App" in r.read().decode()
    assert server.request("GET", "/api/todos") == (200, [])


def test_kompletter_lebenszyklus(server):
    status, a = server.request("POST", "/api/todos", {"text": "Erste"})
    assert status == 201
    _, b = server.request("POST", "/api/todos", {"text": "Zweite"})

    assert server.request("PATCH", f"/api/todos/{a['id']}", {"done": True})[0] == 200
    assert server.request("PATCH", f"/api/todos/{b['id']}", {"text": "Zweite (neu)"})[0] == 200

    _, todos = server.request("GET", "/api/todos")
    assert todos == [
        {"id": a["id"], "text": "Erste", "done": True},
        {"id": b["id"], "text": "Zweite (neu)", "done": False},
    ]

    assert server.request("DELETE", f"/api/todos/{a['id']}")[0] == 204
    _, todos = server.request("GET", "/api/todos")
    assert [t["id"] for t in todos] == [b["id"]]


def test_fehlerantworten_ueber_http(server):
    assert server.request("POST", "/api/todos", {"text": ""})[0] == 400
    assert server.request("PATCH", "/api/todos/99", {"done": True})[0] == 404
    assert server.request("DELETE", "/api/todos/99")[0] == 404


def test_daten_ueberleben_serverneustart(server):
    _, t = server.request("POST", "/api/todos", {"text": "persistent"})
    server.request("PATCH", f"/api/todos/{t['id']}", {"done": True})

    server.stop()
    server.start()

    _, todos = server.request("GET", "/api/todos")
    assert todos == [{"id": t["id"], "text": "persistent", "done": True}]


def test_neue_ids_nach_neustart_kollidieren_nicht(server):
    _, a = server.request("POST", "/api/todos", {"text": "a"})
    server.request("DELETE", f"/api/todos/{a['id']}")
    server.stop()
    server.start()
    _, b = server.request("POST", "/api/todos", {"text": "b"})
    assert b["id"] > a["id"]


def test_zwei_clients_sehen_dieselbe_liste(server):
    server.request("POST", "/api/todos", {"text": "geteilt"})
    # zweiter Client = frischer Request ohne gemeinsamen Zustand
    _, todos = server.request("GET", "/api/todos")
    assert [t["text"] for t in todos] == ["geteilt"]


def test_parallele_schreibzugriffe(server):
    from concurrent.futures import ThreadPoolExecutor

    def create(i):
        return server.request("POST", "/api/todos", {"text": f"t{i}"})

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(create, range(24)))

    assert all(status == 201 for status, _ in results)
    ids = [body["id"] for _, body in results]
    assert len(set(ids)) == 24
    _, todos = server.request("GET", "/api/todos")
    assert len(todos) == 24
