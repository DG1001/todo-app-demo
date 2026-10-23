# Todo App

Einfache Todo-Liste in einer einzigen HTML-Datei. Kein Build, kein Framework, kein Backend.

## Funktionen

- Aufgaben hinzufügen, abhaken und löschen
- Aufgaben per Doppelklick bearbeiten (Enter speichert, Esc bricht ab)
- Filter: Alle / Offen / Erledigt
- Zähler der offenen Aufgaben
- Speicherung im Browser (`localStorage`), die Liste bleibt nach dem Neuladen erhalten

## Starten

```sh
open index.html
```

Alternativ die Datei `index.html` einfach im Browser öffnen. Ein Server ist nicht nötig.

## Projektstruktur

| Datei | Inhalt |
|---|---|
| `index.html` | Die komplette App (HTML, CSS, JavaScript) |
| `fachlich.md` | Fachliche Beschreibung: Zweck, Funktionen, Regeln |
| `technisch.md` | Technische Dokumentation: Aufbau, Datenmodell, Einschränkungen |
| `devlog.md` | Laufendes Entwicklungsprotokoll |
| `AGENTS.md` | Hinweise für KI-Coding-Agenten |

## Hinweise

Die Daten liegen nur im jeweiligen Browser und sind nicht zwischen Geräten synchronisiert.
