# Todo App

Einfache Todo-Liste als Client-Server-App: Flask-Backend mit SQLite, Frontend als einzelne HTML-Datei (Vanilla JS).

## Funktionen

- Aufgaben hinzufügen, abhaken und löschen
- Aufgaben per Doppelklick bearbeiten (Enter speichert, Esc bricht ab)
- Filter: Alle / Offen / Erledigt
- Zähler der offenen Aufgaben
- Speicherung auf dem Server (SQLite), die Liste bleibt über Neustarts und Browser hinweg erhalten

## Starten

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Danach http://127.0.0.1:5000 im Browser öffnen. Die Datenbank `todos.db` wird beim ersten Start angelegt. Mit der Umgebungsvariable `TODO_DB` lässt sich ein anderer Pfad festlegen.

## API

| Methode | Pfad | Beschreibung |
|---|---|---|
| GET | `/api/todos` | Alle Aufgaben |
| POST | `/api/todos` | Anlegen, Body `{"text": "…"}` |
| PATCH | `/api/todos/<id>` | Ändern, Body `{"text"?: "…", "done"?: true}` |
| DELETE | `/api/todos/<id>` | Löschen |

## Projektstruktur

| Datei | Inhalt |
|---|---|
| `app.py` | Flask-Server, REST-API und SQLite-Zugriff |
| `static/index.html` | Frontend (HTML, CSS, JavaScript) |
| `requirements.txt` | Python-Abhängigkeiten |
| `fachlich.md` | Fachliche Beschreibung: Zweck, Funktionen, Regeln |
| `technisch.md` | Technische Dokumentation: Aufbau, Datenmodell, Einschränkungen |
| `devlog.md` | Laufendes Entwicklungsprotokoll |
| `AGENTS.md` | Hinweise für KI-Coding-Agenten |

## Hinweise

Es gibt keine Anmeldung: Alle, die den Server erreichen, sehen und ändern dieselbe Liste. Der Flask-Entwicklungsserver ist nur für lokale Nutzung gedacht.
