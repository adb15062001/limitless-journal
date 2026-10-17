# Limitless Journal

Statische Zeitungs-Webseite für das tägliche Aktien-Briefing. Layout: lange, vertikal gestapelte Seite (Titelseite, ein großer Abschnitt je beobachteter Aktie (Watchlist), Gesamtmarkt, Makro, Ideen, Quellenverzeichnis am Ende).

- `editions/YYYY-MM-DD.json` – eine Datei pro Ausgabe. Felder:
  - `date`, `headline`, `lead`
  - `watchlist[]` – beobachtete Aktien, kein Depot (aktuell NBIS, CRWV, LMND, UBER, COCO), je Wert: `ticker`, `name`, `close`, `change` (= Kursveränderung seit letzter Ausgabe), `dir` (up/down), `figures` [[Bezeichnung, Wert], …] (Kennzahlen), `news` [Liste] (= Neuigkeiten seit letzter Ausgabe), `outlook` (= Ausblick, Absatz), `sources` [[Name, URL], …]
  - `market[]` (Absätze Gesamtmarkt), `market_sources[]`
  - `macro[]` – Makro-Faktoren (Zinsen/Notenbanken, Inflation, Konjunkturdaten, Geopolitik/Öl/Rohstoffe, Zölle, Termine), je: `title`, `what` (was passiert), `effect` (Wirkung auf Markt & Watchlist), `next` (was das voraussichtlich bedeutet), `sources`
  - `ideas[]` – 3 Aktien, die vom KI-Hype noch NICHT profitiert haben, aber künftig profitieren könnten: `ticker`, `name`, `sector`, `why`
- `charts` (wird automatisch von `fetch_charts.py` gefüllt): `{"source": ..., "series": {SYMBOL: {"label", "data": [[datum, schluss], …]}}}` – ca. 3 Monate Tagesschlusskurse von Yahoo Finance für alle Watchlist-Werte sowie ^GSPC, ^IXIC, ^TNX (10-J.-Rendite), BZ=F (Brent).
- `fetch_charts.py` – holt die Chartdaten (Yahoo-Finance-Chart-API, nur Standardbibliothek) und schreibt sie in die Ausgabe-JSON. Warnt, wenn der letzte Kurs nicht zum Ausgabedatum passt.
- `build.py` – erzeugt `index.html` (neueste Ausgabe), `archiv.html` (nach Monaten gruppiert) und `ausgabe/YYYY-MM-DD.html`. Nur Python-Standardbibliothek.

## Täglicher Lauf
1. Kursveränderung jeweils gegenüber dem Schlusskurs der letzten Ausgabe berechnen (erste Ausgabe: ggü. Vortag). Daten recherchieren (Schlusskurse + Kennzahlen, News, Markt, Makro, 3 Ideen ohne offensichtliche KI-Gewinner) – nur verifizierte Zahlen.
2. Neue Datei `editions/<Datum>.json` nach Vorbild der vorhandenen anlegen.
3. `python3 fetch_charts.py <Datum>` ausführen (Chartdaten laden).
4. `python3 build.py` ausführen – erzeugt Inline-SVG-Grafiken (Sparklines, Balkendiagramm Tagesveränderung, 3-Monats-Charts je Aktie, Makro-Kacheln und -Charts); kein externes JavaScript.
5. Screenshot (optional): `google-chrome --headless=new --no-sandbox --window-size=1100,16000 --screenshot=/tmp/full.png file://$PWD/index.html` und unten zuschneiden.
6. Optional: neu zippen / hochladen (`cd /workspace && zip -r aktien-zeitung.zip aktien-zeitung`).

## Veröffentlichen (GitHub Pages)
Repo: `https://github.com/adb15062001/limitless-journal` (öffentlich), Pages aus Branch `main`, Ordner `/` (root).
Öffentliche URL: `https://adb15062001.github.io/limitless-journal/`

Nach jedem Build:
```
git add -A && git commit -m "Ausgabe <Datum>" && git push origin main
```
GitHub Pages veröffentlicht automatisch innerhalb von ca. 1–2 Minuten. (Push läuft über einen Cursor Cloud Agent bzw. eine authentifizierte Git-Verbindung – keine Tokens im Skript.)

## Watchlist
Die aktuelle Watchlist steht in `watchlist.json`. Jede Ausgabe deckt alle dort gelisteten Aktien ab. Gruppenmitglieder können per „Hey Bobby!“ Aktien hinzufügen oder entfernen lassen.
