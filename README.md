# Limitless Journal

Statische Zeitungs-Webseite für das tägliche Aktien-Briefing. Layout: lange, vertikal gestapelte Seite (Titelseite, ein großer Abschnitt je Depotwert, Gesamtmarkt, Makro, Ideen, Quellenverzeichnis am Ende).

- `editions/YYYY-MM-DD.json` – eine Datei pro Ausgabe. Felder:
  - `date`, `headline`, `lead`
  - `holdings[]` (aktuell NBIS, CRWV, LMND, UBER, COCO), je Wert: `ticker`, `name`, `close`, `change` (= Kursveränderung seit letzter Ausgabe), `dir` (up/down), `figures` [[Bezeichnung, Wert], …] (Kennzahlen), `news` [Liste] (= Neuigkeiten seit letzter Ausgabe), `outlook` (= Ausblick, Absatz), `sources` [[Name, URL], …]
  - `market[]` (Absätze Gesamtmarkt), `market_sources[]`
  - `macro[]` – Makro-Faktoren (Zinsen/Notenbanken, Inflation, Konjunkturdaten, Geopolitik/Öl/Rohstoffe, Zölle, Termine), je: `title`, `what` (was passiert), `effect` (Wirkung auf Markt & Depot), `next` (was das voraussichtlich bedeutet), `sources`
  - `ideas[]` – 3 Aktien, die vom KI-Hype noch NICHT profitiert haben, aber künftig profitieren könnten: `ticker`, `name`, `sector`, `why`
- `build.py` – erzeugt `index.html` (neueste Ausgabe), `archiv.html` (nach Monaten gruppiert) und `ausgabe/YYYY-MM-DD.html`. Nur Python-Standardbibliothek.

## Täglicher Lauf
1. Kursveränderung jeweils gegenüber dem Schlusskurs der letzten Ausgabe berechnen (erste Ausgabe: ggü. Vortag). Daten recherchieren (Schlusskurse + Kennzahlen, News, Markt, Makro, 3 Ideen ohne offensichtliche KI-Gewinner) – nur verifizierte Zahlen.
2. Neue Datei `editions/<Datum>.json` nach Vorbild der vorhandenen anlegen.
3. `python3 build.py` ausführen.
4. Screenshot (optional): `google-chrome --headless=new --no-sandbox --window-size=1100,16000 --screenshot=/tmp/full.png file://$PWD/index.html` und unten zuschneiden.
5. Optional: neu zippen / hochladen (`cd /workspace && zip -r aktien-zeitung.zip aktien-zeitung`).

## Veröffentlichen (GitHub Pages)
Repo: `https://github.com/adb15062001/aktien-zeitung` (öffentlich), Pages aus Branch `main`, Ordner `/` (root).
Öffentliche URL: `https://adb15062001.github.io/aktien-zeitung/`

Nach jedem Build:
```
git add -A && git commit -m "Ausgabe <Datum>" && git push origin main
```
GitHub Pages veröffentlicht automatisch innerhalb von ca. 1–2 Minuten. (Push läuft über einen Cursor Cloud Agent bzw. eine authentifizierte Git-Verbindung – keine Tokens im Skript.)
