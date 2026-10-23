# AGENTS.md

Hinweise für KI-Coding-Agenten in diesem Repository.

## Projekt

Client-Server-Todo-App: Flask-Backend mit SQLite in `app.py`, Frontend als einzelne Datei `static/index.html` (HTML, CSS, Vanilla-JS). Einzige Abhängigkeit ist Flask (`requirements.txt`), kein Build-Schritt. Details: `fachlich.md` (Verhalten) und `technisch.md` (Aufbau, API).

## Starten und prüfen

- Starten: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python app.py`, dann http://127.0.0.1:5000.
- Es gibt keine Test-Suite im Repo. Die API mit dem Flask-Test-Client prüfen (`TODO_DB` auf eine temporäre Datei setzen, damit `todos.db` unberührt bleibt) und das Frontend manuell im Browser: hinzufügen, abhaken, bearbeiten (Doppelklick), löschen, Filter, Neuladen (Persistenz).
- Ist keine Browserprüfung möglich, das in Commit-Nachricht und Devlog ausdrücklich so festhalten.

## Konventionen

- Sprache: Deutsch für UI-Texte, Dokumentation und Commit-Nachrichten.
- Backend in `app.py`, Frontend in `static/index.html`. Keine Frameworks oder externen Bibliotheken im Frontend, keine weiteren Python-Abhängigkeiten ohne Absprache.
- Texte der Nutzer immer über `textContent` setzen, nie über `innerHTML`.
- SQL nur mit Platzhaltern (`?`), nie mit String-Zusammenbau.
- Neue oder geänderte API-Endpunkte in `README.md` und `technisch.md` nachziehen.
- Stil des vorhandenen Codes übernehmen (Einrückung, Benennung, sparsame Kommentare).

## Dokumentation pflegen

Nach jeder Änderung, jedem Commit und jedem relevanten Ergebnis (auch Fehlschlägen) einen kurzen Eintrag in `devlog.md` ergänzen (neueste Einträge oben, nach Datum).

Ändert sich Verhalten, `fachlich.md` anpassen. Ändern sich Aufbau, Datenmodell oder Einschränkungen, `technisch.md` anpassen. Neue Funktionen auch in `README.md` aufnehmen.

## Git

- Der Branch ist `master`. Es ist derzeit kein Remote konfiguriert.
- Commit-Nachrichten ausführlich auf Deutsch: Titelzeile, dann Begründung, Verhalten und Umsetzung.
- Nicht ohne ausdrückliche Aufforderung committen oder pushen.
