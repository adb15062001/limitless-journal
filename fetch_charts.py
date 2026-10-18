#!/usr/bin/env python3
"""Lädt echte Tagesschlusskurse (3 Monate) von Yahoo Finance und speichert sie in editions/<datum>.json unter "charts".
Aufruf: python3 fetch_charts.py 2026-10-16   (ohne Datum: neueste Ausgabe). Nur Standardbibliothek."""
import json, sys, glob, os, urllib.request, datetime
B = os.path.dirname(os.path.abspath(__file__))
MACRO = {"^GSPC": "S&P 500", "^IXIC": "Nasdaq", "^TNX": "US-Rendite 10 J. (%)", "BZ=F": "Brent ($/Barrel)"}
# Optionale Zusatzsymbole (Feld "extra_symbols" in der Ausgabe, z. B. Sonntagsausgabe)
EXTRA = {"^DJI": "Dow Jones", "^VIX": "VIX (Volatilität)"}
def fetch(sym, end):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?range=6mo&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    r = json.load(urllib.request.urlopen(req, timeout=20))["chart"]["result"][0]
    out = []
    for t, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]):
        d = datetime.datetime.fromtimestamp(t + r["meta"].get("gmtoffset", 0), datetime.timezone.utc).date().isoformat()
        if c is not None and d <= end: out.append([d, round(c, 4)])
    return out[-64:]  # ca. 3 Monate
import urllib.parse
files = sorted(glob.glob(os.path.join(B, "editions", "*.json")))
path = os.path.join(B, "editions", sys.argv[1] + ".json") if len(sys.argv) > 1 else files[-1]
ed = json.load(open(path, encoding="utf-8"))
syms = [x["ticker"] for x in (ed.get("watchlist") or ed.get("holdings", []))] + list(MACRO) + [x for x in ed.get("extra_symbols", []) if x not in MACRO]
ed["charts"] = {"source": "Yahoo Finance (Tagesschlusskurse)", "series": {}}
for s in syms:
    data = fetch(s, ed["date"])
    if data and data[-1][0] != ed["date"] and ed.get("type") != "sunday": print(f"WARNUNG {s}: letzter Kurs {data[-1][0]} != {ed['date']}")
    if ed.get("type") == "sunday" and data and data[-1][0] != ed.get("week", {}).get("to", data[-1][0]): print(f"WARNUNG {s}: letzter Kurs {data[-1][0]} != Wochenende {ed['week']['to']}")
    ed["charts"]["series"][s] = {"label": MACRO.get(s, EXTRA.get(s, s)), "data": data}
    print(s, len(data), data[-1] if data else None)
json.dump(ed, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
