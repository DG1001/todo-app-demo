# Technische Dokumentation

## Überblick

Single-Page-Todo-App in einer einzelnen Datei (`index.html`) ohne Build-Schritt, Framework oder Backend. HTML, CSS und JavaScript (Vanilla) liegen gemeinsam in der Datei.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | Die komplette App (Markup, Styles, Logik) |
| `devlog.md` | Laufendes Entwicklungsprotokoll |
| `technisch.md` | Diese technische Dokumentation |
| `fachlich.md` | Fachliche Beschreibung |

## Ausführen

`index.html` im Browser öffnen (z. B. `open index.html`). Es wird kein Server benötigt.

## Datenmodell

Der Zustand besteht aus einem Array von Objekten:

```js
{ text: string, done: boolean }
```

Zusätzlich gibt es die Variable `filter` mit den Werten `'all'`, `'open'` oder `'done'`. Sie wird nicht gespeichert.

## Persistenz

- Speicherort: `localStorage`, Schlüssel `todos`, Wert als JSON.
- `save()` schreibt nach jeder Änderung; beim Start wird einmalig gelesen.
- Lese- und Schreibzugriffe sind in `try/catch` gekapselt. Ist `localStorage` nicht verfügbar, läuft die App ohne Persistenz weiter.
- Die Daten gelten nur für den jeweiligen Browser und die jeweilige Herkunft (Origin), also auch nicht geräteübergreifend.

## Aufbau der Logik

- `render()` baut die Liste bei jeder Änderung komplett neu auf (`innerHTML = ''` und neue DOM-Elemente) und aktualisiert den Zähler.
- Texte werden über `textContent` gesetzt, nicht über `innerHTML`. Dadurch ist die Eingabe gegen HTML-Injection geschützt.
- Formular-Submit fügt eine Aufgabe hinzu (Text per `trim()` bereinigt, leere Eingaben werden ignoriert).
- Checkbox ändert `done`, der Button ✕ entfernt die Aufgabe.
- Die Filterbuttons nutzen Event-Delegation auf dem Container `#filters` und das Attribut `data-f`.
- Inline-Bearbeiten: `ondblclick` auf dem Textelement ersetzt es durch ein Eingabefeld.
  - Enter oder `blur` übernimmt, Escape verwirft, leerer Text wird verworfen.
  - Das Flag `finished` verhindert doppeltes Ausführen, weil das Neurendern zusätzlich ein `blur` auslösen kann.

## Bekannte Einschränkungen

- Aufgaben werden über Objektidentität referenziert, es gibt keine IDs.
- Kein automatisierter Test, die Änderungen wurden bisher nicht im Browser geprüft.
- Das Bearbeiten per Doppelklick ist auf Touchgeräten nicht komfortabel erreichbar.
- Keine Tastatur-Alternative zum Doppelklick.
- Kein Remote-Repository konfiguriert (siehe `devlog.md`).
