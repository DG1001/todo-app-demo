# Devlog

Laufendes Entwicklungsprotokoll der Todo-App. Neueste Einträge oben.

## 2026-10-23

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
