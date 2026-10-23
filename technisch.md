# Technische Dokumentation

## Überblick

Client-Server-Todo-App. Das Backend ist ein Flask-Server (`app.py`) mit SQLite und einer REST-API, das Frontend eine einzelne Datei (`static/index.html`, Vanilla JS) ohne Build-Schritt oder Framework. Der Server liefert das Frontend unter `/` aus.

## Dateien

| Datei | Zweck |
|---|---|
| `app.py` | Flask-App, REST-API, SQLite-Zugriff |
| `static/index.html` | Frontend (Markup, Styles, Logik) |
| `requirements.txt` | Abhängigkeiten (`Flask>=3.0`) |
| `.gitignore` | Schließt `.venv/`, `__pycache__/` und `*.db` aus |
| `devlog.md` | Laufendes Entwicklungsprotokoll |
| `technisch.md` / `fachlich.md` | Dokumentation |

## Ausführen

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py     # http://127.0.0.1:5000
```

`app.py` startet den Entwicklungsserver mit `debug=True`; das ist nur für lokale Nutzung geeignet.

## Datenmodell

Tabelle `todos` in SQLite (`todos.db`, Pfad per Umgebungsvariable `TODO_DB` änderbar, Tabelle wird beim Import von `app.py` per `init_db()` angelegt):

| Spalte | Typ | Bedeutung |
|---|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Eindeutige ID |
| `text` | TEXT NOT NULL | Aufgabentext (getrimmt, nicht leer) |
| `done` | INTEGER NOT NULL DEFAULT 0 | 0/1, in der API als Boolean |

Das JSON-Objekt der API: `{ "id": number, "text": string, "done": boolean }`.

## REST-API

| Methode | Pfad | Body | Antwort |
|---|---|---|---|
| GET | `/api/todos` | – | 200, Liste (sortiert nach `id`) |
| POST | `/api/todos` | `{text}` | 201, neue Aufgabe; 400 bei leerem/fehlendem Text |
| PATCH | `/api/todos/<id>` | `{text?, done?}` | 200, aktualisierte Aufgabe; 400 bei leerem Text oder nicht-booleschem `done`; 404 unbekannt |
| DELETE | `/api/todos/<id>` | – | 204; 404 unbekannt |

Fehler kommen als `{"error": "…"}`. Der Text wird serverseitig mit `strip()` bereinigt.

## Backend

- Pro Request wird eine SQLite-Verbindung über `flask.g` geöffnet (`get_db()`) und im `teardown_appcontext` geschlossen.
- SQL läuft ausschließlich mit Platzhaltern (`?`), also ohne SQL-Injection.
- `GET /` liefert `static/index.html` per `send_from_directory`.

## Frontend

- `api()` kapselt `fetch` auf `/api/todos`; `load()` lädt die Liste beim Start. `update()` und `remove()` rufen PATCH bzw. DELETE auf und rendern danach neu.
- `render()` baut die Liste bei jeder Änderung komplett neu auf und aktualisiert den Zähler. Der Filter (`all`/`open`/`done`) liegt nur im Speicher und wird clientseitig angewendet.
- Texte werden über `textContent` gesetzt, nicht über `innerHTML` (Schutz vor HTML-Injection).
- Ist der Server nicht erreichbar, zeigt die Zählzeile „Server nicht erreichbar“; Fehler bei Änderungen erscheinen per `alert`.
- Inline-Bearbeiten: `ondblclick` ersetzt den Text durch ein Eingabefeld. Enter oder `blur` übernimmt, Escape verwirft, leerer oder unveränderter Text löst keinen Request aus. Das Flag `finished` verhindert doppeltes Ausführen, weil das Neurendern zusätzlich ein `blur` auslösen kann.

## Tests

pytest-Suite unter `tests/` (Konfiguration in `pytest.ini`, Abhängigkeit in `requirements-dev.txt`), 73 Tests in drei Ebenen, per Marker einzeln startbar (`-m unit|module|integration`):

| Ebene | Datei | Gegenstand |
|---|---|---|
| Unit | `tests/test_unit.py` | `clean_text`, `row_to_dict`, `init_db` (Schema, Idempotenz), `TODO_DB`-Auswertung (im Subprozess) |
| Modul | `tests/test_module.py` | Alle Endpunkte samt SQLite über den Flask-Test-Client: Statuscodes, Validierung, Teil-Updates, Rollback bei Fehlern, 404/405, SQL-Injection, ID-Vergabe, Schließen der DB-Verbindung, Auslieferung von `/` |
| Integration | `tests/test_integration.py` | Echter Server-Prozess auf freiem Port, Zugriff per HTTP: Lebenszyklus, Fehlerantworten, Persistenz über Neustart, parallele Schreibzugriffe |

`tests/conftest.py` biegt `DB_PATH` pro Test auf eine temporäre Datei um (`db_path`, `client`). Die echte `todos.db` wird nicht berührt.

Nicht abgedeckt: Das Frontend (`static/index.html`) hat keine automatisierten Tests, es wird nur auf Auslieferung geprüft. Die Browserlogik (Rendern, Filter, Doppelklick-Bearbeiten) ist weiter manuell zu testen.

## Bekannte Einschränkungen

- Keine Authentifizierung und keine Benutzertrennung: Alle teilen sich eine Liste.
- Entwicklungsserver mit `debug=True`, nicht für den produktiven Betrieb.
- Bei gleichzeitigen Änderungen aus mehreren Browsern gilt „letzter gewinnt“; es gibt keine Live-Synchronisation, ein Neuladen ist nötig.
- Das Bearbeiten per Doppelklick ist auf Touchgeräten nicht komfortabel erreichbar und hat keine Tastatur-Alternative.
- Kein Remote-Repository konfiguriert (siehe `devlog.md`).
