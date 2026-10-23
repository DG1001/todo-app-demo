# AGENTS.md

Hinweise für KI-Coding-Agenten in diesem Repository.

## Projekt

Todo-App als einzelne Datei `index.html` (HTML, CSS und Vanilla-JS gemeinsam). Kein Build, keine Abhängigkeiten, kein Paketmanager, keine Tests. Details: `fachlich.md` (Verhalten) und `technisch.md` (Aufbau).

## Starten und prüfen

- Starten: `open index.html` (kein Server nötig).
- Es gibt keine automatisierten Tests. Änderungen manuell im Browser prüfen: hinzufügen, abhaken, bearbeiten (Doppelklick), löschen, Filter, Neuladen (Persistenz).
- Ist keine Browserprüfung möglich, das in Commit-Nachricht und Devlog ausdrücklich so festhalten.

## Konventionen

- Sprache: Deutsch für UI-Texte, Dokumentation und Commit-Nachrichten.
- Alles bleibt in `index.html`, solange kein Aufteilen ausdrücklich gewünscht ist. Keine Frameworks oder externen Bibliotheken ergänzen.
- Texte der Nutzer immer über `textContent` setzen, nie über `innerHTML`.
- Zugriffe auf `localStorage` in `try/catch` kapseln. Die App muss auch ohne Speicher funktionieren.
- Stil des vorhandenen Codes übernehmen (Einrückung, Benennung, sparsame Kommentare).
- Aufgaben haben keine IDs, sondern werden über Objektidentität referenziert. Bei Änderungen daran `technisch.md` anpassen.

## Dokumentation pflegen

Nach jeder Änderung, jedem Commit und jedem relevanten Ergebnis (auch Fehlschlägen) einen kurzen Eintrag in `devlog.md` ergänzen (neueste Einträge oben, nach Datum).

Ändert sich Verhalten, `fachlich.md` anpassen. Ändern sich Aufbau, Datenmodell oder Einschränkungen, `technisch.md` anpassen. Neue Funktionen auch in `README.md` aufnehmen.

## Git

- Der Branch ist `master`. Es ist derzeit kein Remote konfiguriert.
- Commit-Nachrichten ausführlich auf Deutsch: Titelzeile, dann Begründung, Verhalten und Umsetzung.
- Nicht ohne ausdrückliche Aufforderung committen oder pushen.
