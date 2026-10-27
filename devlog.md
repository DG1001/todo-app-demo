# Devlog

Laufendes Entwicklungsprotokoll der Todo-App. Neueste Einträge oben.

## 2026-10-27

- **Veröffentlichung vorbereitet (committed):** Repo auf personen- und firmenbezogene Daten geprüft. Dateien sauber; die Historie enthält Autorname und Firmen-Mailadresse sowie `Claude-Session:`-Links. Entscheidung: Historie und Mailadresse bleiben bewusst unverändert, `security-review.md` bleibt im Repo (Befunde offen). MIT-`LICENSE` (Copyright 2026 Frederik Wystup) ergänzt, README verweist darauf. Das Projekt soll als Beispiel öffentlich sichtbar machen, wie es vom einfachen Prompt zur dokumentierten, getesteten und geprüften App kam (README, AGENTS.md, Devlog, Tests, Review). Noch kein Remote konfiguriert.

## 2026-10-23

- **UI-Tests (committed):** `tests/test_ui.py` mit 31 Playwright-Tests (Chromium, headless) angelegt, dazu `tests/helpers.py` (gemeinsame `Server`-Klasse, aus `test_integration.py` herausgelöst) und `pytest-playwright` in `requirements-dev.txt`. Gesamt 104 Tests, alle grün; die UI-Tests liefen dreimal hintereinander stabil. Gegenprobe mit fünf Frontend-Fehlern in einer Kopie: `innerHTML` statt `textContent`, Escape wirkungslos, Filter wirkungslos und falscher Zähler wurden erkannt. Das entfernte `finished`-Flag wurde zunächst NICHT erkannt; dafür gibt es jetzt einen Test mit verzögerter PATCH-Antwort, der es erkennt. Beim Schreiben der Tests aufgefallen: Der Eingabetext wird erst nach der Serverantwort geleert; tippt man währenddessen schon die nächste Aufgabe, wird sie gelöscht (nicht behoben).
- **Security-Review (committed):** `security-review.md` mit 7 Befunden und Freigabe-Checkboxen angelegt (u. a. `debug=True`, fehlende Host-Prüfung, keine Größenlimits, 500 bei riesigen IDs). Es wurde nichts am Code geändert; Umsetzung erst nach Freigabe.
- **Tests (committed):** pytest-Suite mit 73 Tests angelegt (`tests/test_unit.py`, `test_module.py`, `test_integration.py`, `conftest.py`, `pytest.ini`, `requirements-dev.txt`). Alle bestehen. Gegenprobe mit vier absichtlich eingebauten Fehlern (`strip` entfernt, 404→200, `DELETE` ohne `WHERE`, kein `commit`) in einer Kopie: Jeder wurde von den Tests erkannt. Frontend weiterhin ohne automatisierte Tests. README, technisch.md, AGENTS.md, `.gitignore` angepasst.
- **App gestartet:** Server läuft lokal auf http://127.0.0.1:5000 (Hinweis: `localhost` kann auf macOS durch den AirPlay-Empfänger auf Port 5000 belegt sein).
- **Client-Server-Umstellung (committed):** `app.py` (Flask, SQLite, REST-API unter `/api/todos`), `requirements.txt`, `.gitignore` angelegt; `index.html` nach `static/index.html` verschoben und von `localStorage` auf `fetch` umgestellt. API mit dem Flask-Test-Client geprüft (alle Endpunkte, 400/404-Fälle: OK). Frontend nicht im Browser getestet. README, technisch.md, fachlich.md, AGENTS.md angepasst.
- **Commit:** Dokumentation (`devlog.md`, `technisch.md`, `fachlich.md`, `README.md`, `AGENTS.md`) committed.
- **Doku:** `README.md` (Überblick, Starten, Projektstruktur) und `AGENTS.md` (Konventionen und Arbeitsregeln für Agenten) angelegt.
- **Doku:** `technisch.md` (Architektur, Datenmodell, Persistenz, Einschränkungen) und `fachlich.md` (Zweck, Funktionen, Regeln, Abgrenzung) angelegt.
- **Devlog:** `devlog.md` angelegt.
- **Push versucht, gescheitert:** Das Repo hat keinen Remote (`git push` → "No configured push destination"). Offen: Remote-URL oder neues GitHub-Repo.
- **Commit `cafad0e`:** Aufgaben per Doppelklick inline bearbeiten (Enter/Blur speichert, Esc verwirft, leerer Text wird ignoriert). Nicht im Browser getestet.
- **Feature:** Inline-Bearbeiten in `index.html` ergänzt. Ein `finished`-Flag verhindert doppeltes Ausführen, weil Enter/Esc beim Neurendern zusätzlich `blur` auslösen.
- **Start:** Todo-App als einzelne `index.html` (Vanilla JS, Persistenz via localStorage). Funktionen: hinzufügen, abhaken, löschen, Filter Alle/Offen/Erledigt, Zähler. Commit `ac1fe42`.
