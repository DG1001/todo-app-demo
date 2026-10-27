# Security-Review: Todo-App

Stand: Commit `3369576`, 2026-10-23. Geprüft: `app.py`, `static/index.html`, `requirements*.txt`, Repo-Suche nach Secrets, Probe-Requests auf einer Kopie mit temporärer Datenbank. Der Code wurde dabei nicht verändert.

**Gesamturteil:** Für den lokalen Betrieb (`127.0.0.1`) gibt es keine kritische Schwachstelle. Die Befunde 1–3 sind vor jedem Betrieb außerhalb von localhost Pflicht.

## Freigabe

Zum Freigeben `[ ]` zu `[x]` ändern. Umgesetzt wird nur, was angekreuzt ist. Danach wird nur auf ausdrückliche Aufforderung committet.

- [ ] **1. `debug=True` abschalten** (Hoch, sobald erreichbar)
- [ ] **2. Host-Prüfung per `TRUSTED_HOSTS`** (Mittel)
- [ ] **3. Größenlimits für Request und Text** (Mittel)
- [ ] **4. Riesige IDs sauber mit 404 beantworten** (Niedrig)
- [ ] **5. Security-Header und CSP** (Niedrig)
- [ ] **6. Abhängigkeiten pinnen und `pip-audit` ausführen** (Niedrig)
- [ ] **7. Session-Links aus den Commit-Nachrichten entfernen** (Hinweis, schreibt die Historie um)
- [ ] Zu jedem freigegebenen Punkt Tests ergänzen
- [ ] Doku (`README.md`, `technisch.md`, `AGENTS.md`, `devlog.md`) anpassen

## Befunde

### 1. `debug=True` ist fest eingebaut — Hoch, sobald erreichbar (derzeit niedrig)

- **Stelle:** `app.py:107` (`app.run(debug=True)`)
- **Problem:** Der Werkzeug-Debugger erlaubt Codeausführung, und 500er-Fehler zeigen Tracebacks mit Quelltext und Pfaden. Heute bindet der Server nur an `127.0.0.1`. Ein `host="0.0.0.0"` oder eine Kopie auf einem Server macht daraus Remote Code Execution. Der Server läuft gerade mit diesem Flag.
- **Vorschlag:** Debug nur über eine Umgebungsvariable einschalten (z. B. `TODO_DEBUG=1`), Standard aus.
- [ ] freigegeben

### 2. Keine Authentifizierung, keine Host-Prüfung — Mittel

- **Stelle:** `app.py` gesamt
- **Problem:**
  - Wer den Server erreicht, kann alles lesen, ändern und löschen. Das ist als Design dokumentiert.
  - Der Host-Header wird nicht geprüft (Probe: `Host: evil.example` → 200). Per DNS-Rebinding könnte eine fremde Webseite, die bei laufendem Server besucht wird, die Liste lesen und verändern. Die Auswirkung ist bei Todo-Daten gering.
  - Cross-Site-Schreibzugriffe (CSRF) sind derzeit nur zufällig blockiert: Formulare und `text/plain` ergeben 400, und es gibt keine CORS-Header. Das liegt an `get_json(silent=True)` und ist kein bewusster Schutz.
- **Vorschlag:** `TRUSTED_HOSTS` setzen (Flask 3.1). Für Mehrbenutzerbetrieb wäre eine Anmeldung nötig; das ist ein eigenes Feature.
- [ ] freigegeben (nur Host-Prüfung)

### 3. Keine Größenbegrenzung — Mittel

- **Stelle:** `app.py`, `clean_text()` und App-Konfiguration
- **Problem:** Ein 5-MB-Text wurde mit 201 gespeichert, `MAX_CONTENT_LENGTH` ist nicht gesetzt, und es gibt keine Obergrenze für die Anzahl der Zeilen. Speicher und Datenbank lassen sich füllen (Denial of Service).
- **Vorschlag:** `MAX_CONTENT_LENGTH` setzen (z. B. 16 KB), Text auf z. B. 500 Zeichen begrenzen (Antwort 400 bzw. 413).
- [ ] freigegeben

### 4. Riesige IDs führen zu 500 — Niedrig

- **Stelle:** `update_todo`, `delete_todo` (`app.py`)
- **Problem:** `PATCH` und `DELETE` auf `/api/todos/` mit einer 30-stelligen Zahl liefern 500 (`OverflowError: Python int too large to convert to SQLite INTEGER`). Im Debug-Modus zusätzlich ein Informationsleck.
- **Vorschlag:** ID-Bereich prüfen und 404 zurückgeben.
- [ ] freigegeben

### 5. Keine Security-Header, keine CSP — Niedrig

- **Stelle:** `app.py` (Antworten), `static/index.html` (Inline-Skript)
- **Problem:** Es fehlen `X-Content-Type-Options`, Clickjacking-Schutz (`frame-ancestors`) und eine CSP. Eine strenge CSP geht wegen des Inline-Skripts nur, wenn es in eine eigene Datei ausgelagert wird oder per Hash freigegeben wird.
- **Vorschlag:** `after_request`-Handler mit Headern; Skript nach `static/app.js` auslagern und CSP `default-src 'self'` setzen.
- [ ] freigegeben

### 6. Abhängigkeiten nicht gepinnt — Niedrig

- **Stelle:** `requirements.txt` (`Flask>=3.0`), `requirements-dev.txt` (`pytest>=8.0`)
- **Problem:** Keine Obergrenze, kein Lockfile, keine Hashes. Installiert sind Flask 3.1.3 und Werkzeug 3.1.9. Ein CVE-Scan wurde bisher nicht ausgeführt.
- **Vorschlag:** Auf getestete Versionen pinnen (`==`), `pip-audit` ausführen und das Ergebnis im Devlog festhalten.
- [ ] freigegeben

### 7. Session-Link in Commit-Nachrichten — Hinweis

- **Stelle:** Alle bisherigen Commits ab dem Doku-Commit (`git log`, Zeile `Claude-Session: https://claude.ai/code/session_…`)
- **Problem:** Kein Secret, aber Metadaten. Bei einem Push in ein öffentliches Repo wären sie sichtbar.
- **Vorschlag:** Vor dem ersten Push entscheiden. Entfernen heißt, die Historie umzuschreiben (neue Commit-Hashes); das ist nur sinnvoll, solange es keinen Remote gibt.
- [ ] freigegeben

## Geprüft und in Ordnung

- [x] **SQL-Injection:** SQL läuft durchgehend mit Platzhaltern, ein Test mit `'); DROP TABLE …` ist grün.
- [x] **XSS:** Nutzerdaten gelangen nur über `textContent` in die Seite, das einzige `innerHTML` ist `list.innerHTML = ''`.
- [x] **Pfad-Traversal:** `/static/../app.py` und `/static/%2e%2e/app.py` ergeben 404, `todos.db` und der Quelltext liegen außerhalb von `static/`.
- [x] **Eingabevalidierung:** Typen werden strikt geprüft (`done` nur als Boolean, `text` nur als nicht leerer String).
- [x] **CORS:** Es gibt keine CORS-Freigabe.
- [x] **Secrets im Repo:** Suche nach `password`, `secret`, `token`, `api key` ohne Treffer; `todos.db` und `.venv` stehen in `.gitignore`.

## Nicht geprüft

- Dependency-Schwachstellen (kein `pip-audit`)
- Verhalten des Werkzeug-Debuggers unter DNS-Rebinding (belegt ist nur, dass der Host-Header nicht geprüft wird)
- Das Frontend im echten Browser
