# Fachliche Beschreibung

## Zweck

Die App hilft dabei, Aufgaben zu erfassen und abzuarbeiten. Sie ist für eine Person oder ein kleines Team gedacht, das schnell eine gemeinsame Liste führen möchte, ohne Konto. Ein Server muss dafür laufen (siehe `README.md`).

## Funktionen

1. **Aufgabe anlegen:** Text eingeben und mit „Hinzufügen“ oder Enter bestätigen. Leere Eingaben werden nicht angelegt.
2. **Aufgabe erledigen:** Über die Checkbox lässt sich eine Aufgabe als erledigt markieren; erledigte Aufgaben erscheinen durchgestrichen und grau. Das Häkchen kann wieder entfernt werden.
3. **Aufgabe bearbeiten:** Doppelklick auf den Text ändert ihn direkt in der Liste. Enter oder Klick daneben speichert, Esc bricht ab. Ein leerer Text wird nicht übernommen.
4. **Aufgabe löschen:** Mit ✕ wird die Aufgabe entfernt, ohne Rückfrage und ohne Papierkorb.
5. **Filtern:** „Alle“, „Offen“ oder „Erledigt“ schränken die Anzeige ein.
6. **Übersicht:** Eine Zeile zeigt, wie viele Aufgaben offen sind, im Verhältnis zur Gesamtzahl (z. B. „2 offen von 5“).

## Regeln

- Neue Aufgaben starten immer als „offen“ und werden am Ende der Liste eingefügt.
- Die Reihenfolge entspricht der Anlage-Reihenfolge.
- Die Liste liegt auf dem Server. Sie bleibt über Neustarts und in jedem Browser, der den Server erreicht, erhalten.
- Es gibt nur eine gemeinsame Liste und keine Anmeldung: Wer den Server erreicht, sieht und ändert dieselben Aufgaben. Änderungen anderer erscheinen erst nach dem Neuladen.
- Der gewählte Filter wird nicht gespeichert; nach dem Neuladen gilt wieder „Alle“.

## Abgrenzung (nicht enthalten)

Fälligkeitsdaten, Prioritäten, Kategorien, Sortierung, mehrere Listen, Anmeldung, Live-Synchronisation und getrennte Listen pro Benutzer.

## Mögliche Erweiterungen

Erledigte Aufgaben gesammelt löschen, Fälligkeitsdatum, Priorität, Drag & Drop zum Umsortieren, Dark Mode.
