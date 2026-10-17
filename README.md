# Die KI-Börsenzeitung

Statische Zeitungs-Webseite für das tägliche Aktien-Briefing.

- `editions/YYYY-MM-DD.json` – eine Datei pro Ausgabe (Felder: date, headline, lead, holdings[] (je Wert: ticker, name, close, change = Kursveränderung seit letzter Ausgabe, dir up/down, news = Neuigkeiten seit letzter Ausgabe, outlook = Ausblick, sources), market[], market_sources[], ideas[]).
- `build.py` – erzeugt `index.html` (neueste Ausgabe), `archiv.html` (nach Monaten gruppiert) und `ausgabe/YYYY-MM-DD.html`. Nur Python-Standardbibliothek.

## Täglicher Lauf
1. Kursveränderung jeweils gegenüber dem Schlusskurs der letzten Ausgabe berechnen (erste Ausgabe: ggü. Vortag). Daten recherchieren (Schlusskurse, News, Markt, 3 Ideen) – nur verifizierte Zahlen.
2. Neue Datei `editions/<Datum>.json` nach Vorbild der vorhandenen anlegen.
3. `python3 build.py` ausführen.
4. Optional: neu zippen / hochladen (`cd /workspace && zip -r aktien-zeitung.zip aktien-zeitung`).

## Veröffentlichen (GitHub Pages)
Repo: `https://github.com/adb15062001/aktien-zeitung` (öffentlich), Pages aus Branch `main`, Ordner `/` (root).
Öffentliche URL: `https://adb15062001.github.io/aktien-zeitung/`

Nach jedem Build:
```
git add -A && git commit -m "Ausgabe <Datum>" && git push origin main
```
GitHub Pages veröffentlicht automatisch innerhalb von ca. 1–2 Minuten. (Push läuft über einen Cursor Cloud Agent bzw. eine authentifizierte Git-Verbindung – keine Tokens im Skript.)
