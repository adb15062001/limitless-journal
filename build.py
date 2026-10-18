#!/usr/bin/env python3
"""Baut index.html, archiv.html und ausgabe/YYYY-MM-DD.html aus editions/*.json (nur Standardbibliothek)."""
import json, glob, os, html
from datetime import date
B = os.path.dirname(os.path.abspath(__file__))
MON = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]
DAY = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
e = html.escape
def dlong(s):
    d = date.fromisoformat(s); return f"{DAY[d.weekday()]}, {d.day}. {MON[d.month-1]} {d.year}"
CSS = """*{box-sizing:border-box}
body{background:#fafaf7;color:#151515;font-family:Georgia,'Times New Roman',serif;margin:0;font-size:21px;line-height:1.6}
.wrap{max-width:1000px;margin:auto;padding:28px 32px 60px}
header{text-align:center;border-bottom:5px double #151515;padding-bottom:10px}
.mast{font-family:'UnifrakturMaguntia','Old English Text MT',Georgia,serif;font-size:84px;line-height:1.1;margin:14px 0}
.mast a{color:inherit;text-decoration:none}
.bar{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;border-top:1px solid #151515;border-bottom:1px solid #151515;padding:6px 0;font-size:15px;text-transform:uppercase;letter-spacing:2px}
.bar a{color:#151515}
.front{padding:40px 0 30px;border-bottom:3px solid #151515;text-align:center}
.kicker{text-transform:uppercase;letter-spacing:4px;font-size:15px;color:#7a1d1d}
h1.head{font-size:64px;line-height:1.08;margin:14px 0 22px}
.lead{font-size:26px;font-style:italic;max-width:860px;margin:0 auto}
.ticker{display:flex;flex-wrap:wrap;justify-content:center;gap:12px 28px;margin-top:28px;font-family:Helvetica,Arial,sans-serif;font-size:18px;font-weight:bold}
section{padding:46px 0 36px;border-bottom:3px solid #151515}
.label{text-transform:uppercase;letter-spacing:4px;font-size:15px;border-bottom:1px solid #151515;padding-bottom:6px;margin-bottom:12px}
h2{font-size:48px;line-height:1.1;margin:8px 0 6px}
h3{font-size:30px;margin:28px 0 8px}
.price{font-family:Helvetica,Arial,sans-serif;font-size:34px;font-weight:bold;margin:8px 0 22px}
.price small{font-size:17px;font-weight:normal;color:#444;display:block;letter-spacing:1px;text-transform:uppercase}
.down{color:#a40000}.up{color:#0b6b0b}
table.fig{width:100%;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;font-size:18px;margin:6px 0 10px}
table.fig td{padding:9px 6px;border-bottom:1px dotted #888}
table.fig td:last-child{text-align:right;font-weight:bold}
ul.news li{margin:10px 0}
.outlook{font-size:22px;border-left:5px solid #151515;padding:6px 0 6px 20px;margin-top:10px}
.macro{margin:34px 0 10px;padding-top:10px;border-top:1px solid #151515}
.macro h3{margin-top:10px}
.macro dt{font-weight:bold;text-transform:uppercase;letter-spacing:2px;font-size:15px;margin-top:14px}
.macro dd{margin:4px 0 0}
.idea{margin:30px 0;padding-top:12px;border-top:1px solid #151515}
.idea .sec{font-style:italic;color:#444}
.sources{font-size:16px;line-height:1.5}
.sources h3{font-size:20px;margin:18px 0 4px}
.sources a{color:#333;word-break:break-word}
.disc{margin-top:30px;font-size:15px;text-align:center}
ul.arch{font-size:22px}ul.arch li{margin:10px 0}

.tag{display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:.8em;font-weight:bold;padding:2px 9px;border-radius:3px;color:#fff;white-space:nowrap}
.tag.up{background:#0b6b0b}.tag.down{background:#a40000}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-top:28px;text-align:left}
.tile{border:1.5px solid #151515;background:#ffffff;padding:10px 12px;font-family:Helvetica,Arial,sans-serif}
.tile .t{font-size:14px;letter-spacing:2px;text-transform:uppercase;color:#444}
.tile .v{font-size:24px;font-weight:bold;margin:2px 0}
.tile .spark{width:100%;height:36px;display:block;margin-top:6px}
.chart{margin:18px 0 8px;padding:0}
.chart figcaption{font-family:Helvetica,Arial,sans-serif;font-size:16px;margin-bottom:6px}
.chart svg{width:100%;height:auto;display:block;font-family:Helvetica,Arial,sans-serif;font-size:13px;fill:#333}
.chart svg .b{font-weight:bold;fill:#151515}.chart svg .big{font-size:18px}
.badge{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;background:#151515;color:#fafaf7;font-family:Helvetica,Arial,sans-serif;font-weight:bold;font-size:15px;margin-right:12px;vertical-align:middle}
.mini{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:10px 30px}
.chartnote{font-size:14px;color:#555;font-style:italic}
.sunbadge{display:inline-block;background:#7a1d1d;color:#fff;font-family:Helvetica,Arial,sans-serif;font-size:15px;font-weight:bold;letter-spacing:2px;text-transform:uppercase;padding:6px 14px;border-radius:3px;margin-top:6px}
.archtag{display:inline-block;background:#7a1d1d;color:#fff;font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:bold;letter-spacing:1px;padding:2px 8px;border-radius:3px;margin-right:6px;vertical-align:middle}
.tznote{font-family:Helvetica,Arial,sans-serif;font-size:16px;background:#fff;border:1px solid #bbb;padding:10px 14px;margin:14px 0}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;font-family:Helvetica,Arial,sans-serif;font-size:15px;margin:8px 0 4px}
.legend span{display:inline-flex;align-items:center;gap:6px}.legend i{display:inline-block;width:14px;height:14px;border-radius:3px}
.weekgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:18px 0}
.daycard{border:1.5px solid #151515;background:#fff;padding:8px 10px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:1.35}
.daycard .dn{font-weight:bold;font-size:16px;border-bottom:1px solid #151515;margin-bottom:6px;padding-bottom:3px}
.daycard div.ev{margin:5px 0;padding-left:8px;border-left:4px solid #999}
.day{margin:30px 0 10px}.day h3{margin:0 0 8px;border-bottom:1px solid #151515;padding-bottom:4px}
.ev2{display:grid;grid-template-columns:110px 1fr;gap:4px 14px;padding:10px 0;border-bottom:1px dotted #888}
.ev2 .tm{font-family:Helvetica,Arial,sans-serif;font-weight:bold;font-size:17px}
.ev2 .tt{font-weight:bold}.ev2 .nt{font-size:18px;color:#333}.ev2 .sr{font-size:14px}.ev2 .sr a{color:#555}
.chip{display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:12px;font-weight:bold;color:#fff;padding:1px 7px;border-radius:3px;margin-right:6px;vertical-align:middle;letter-spacing:1px;text-transform:uppercase}
table.wk{width:100%;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;font-size:18px;margin:10px 0}
table.wk th{text-align:left;border-bottom:2px solid #151515;padding:6px;font-size:14px;text-transform:uppercase;letter-spacing:1px}
table.wk td{padding:8px 6px;border-bottom:1px dotted #888}table.wk td.n{text-align:right;white-space:nowrap}
.stock{margin:30px 0;padding-top:12px;border-top:1px solid #151515}
.stock .src{font-size:14px}.stock .src a{color:#555}
.tidea{margin:30px 0;padding:16px 18px;border:2px solid #151515;background:#fff}
.tidea h3{margin-top:0}.tidea dt{font-weight:bold;text-transform:uppercase;letter-spacing:2px;font-size:14px;margin-top:12px;font-family:Helvetica,Arial,sans-serif}
.tidea dd{margin:3px 0 0}.tidea dd.inv{border-left:4px solid #a40000;padding-left:10px}
.warn{border:3px solid #a40000;background:#fff5f5;padding:14px 18px;font-family:Helvetica,Arial,sans-serif;font-size:18px;margin:16px 0}
.warn b{color:#a40000;text-transform:uppercase;letter-spacing:2px}
ul.look{font-size:19px}ul.look li{margin:8px 0}ul.look a{color:#555;font-size:14px}
@media(max-width:700px){.ev2{grid-template-columns:1fr}.weekgrid{grid-template-columns:1fr}.tidea{padding:12px}.sunbadge{font-size:13px}table.wk{font-size:16px}}
@media(max-width:700px){.tiles{grid-template-columns:repeat(2,1fr);gap:10px}.tile .v{font-size:20px}.badge{width:36px;height:36px;font-size:13px}.chart svg{font-size:21px}.chart svg .big{font-size:22px}.chart figcaption{font-size:14px}}
@media(max-width:700px){body{font-size:18px}.mast{font-size:44px}h1.head{font-size:38px}h2{font-size:34px}.lead{font-size:20px}.wrap{padding:16px}}"""

UP, DN = "#0b6b0b", "#a40000"
def fmt(v, dec=2): return f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def series(d, sym): return (d.get("charts") or {}).get("series", {}).get(sym, {}).get("data", [])
def pct(a, b): return (b / a - 1) * 100
def ddm(iso): y, m, dd = iso.split("-"); return f"{int(dd)}.{int(m)}."
def tag(v): 
    c = "up" if v >= 0 else "down"; a = "▲" if v >= 0 else "▼"
    return f'<span class="tag {c}">{a} {fmt(abs(v))} %</span>'
def spark(data, w=120, h=34):
    if len(data) < 2: return ""
    v = [x[1] for x in data]; lo, hi = min(v), max(v); r = (hi - lo) or 1
    pts = " ".join(f"{i*(w-4)/(len(v)-1)+2:.1f},{h-3-(x-lo)/r*(h-6):.1f}" for i, x in enumerate(v))
    col = UP if v[-1] >= v[0] else DN
    return f'<svg class="spark" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true"><polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" vector-effect="non-scaling-stroke"/></svg>'
def linechart(data, title, dec=2, unit=""):
    if len(data) < 2: return ""
    W, H, L, R, T, Bm = 640, 280, 80, 14, 22, 34
    v = [x[1] for x in data]; lo, hi = min(v), max(v); pad = (hi - lo) * 0.08 or 1; lo2, hi2 = lo - pad, hi + pad
    X = lambda i: L + i * (W - L - R) / (len(v) - 1); Y = lambda x: T + (hi2 - x) / (hi2 - lo2) * (H - T - Bm)
    col = UP if v[-1] >= v[0] else DN
    pts = " ".join(f"{X(i):.1f},{Y(x):.1f}" for i, x in enumerate(v))
    area = f"{X(0):.1f},{H-Bm} {pts} {X(len(v)-1):.1f},{H-Bm}"
    g = ""
    for k in range(4):
        yv = lo2 + (hi2 - lo2) * k / 3; yy = Y(yv)
        g += f'<line x1="{L}" x2="{W-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#bbb" stroke-dasharray="3 4"/><text x="{L-6}" y="{yy+4:.1f}" text-anchor="end">{fmt(yv, dec)}</text>'
    for i in (0, len(v)//2, len(v)-1):
        g += f'<text x="{X(i):.1f}" y="{H-8}" text-anchor="{"start" if i==0 else "end" if i==len(v)-1 else "middle"}">{ddm(data[i][0])}</text>'
    imax, imin = v.index(hi), v.index(lo)
    g += f'<circle cx="{X(imax):.1f}" cy="{Y(hi):.1f}" r="3.5" fill="#151515"/><text x="{X(imax):.1f}" y="{Y(hi)-8:.1f}" text-anchor="middle" class="b">Hoch {fmt(hi, dec)}</text>'
    g += f'<circle cx="{X(imin):.1f}" cy="{Y(lo):.1f}" r="3.5" fill="#151515"/><text x="{X(imin):.1f}" y="{Y(lo)+18:.1f}" text-anchor="middle" class="b">Tief {fmt(lo, dec)}</text>'
    g += f'<circle cx="{X(len(v)-1):.1f}" cy="{Y(v[-1]):.1f}" r="5" fill="{col}"/>'
    ch = pct(v[0], v[-1])
    return (f'<figure class="chart"><figcaption><b>{e(title)}</b> · {ddm(data[0][0])}–{ddm(data[-1][0])} {tag(ch)}</figcaption>'
            f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(title)}"><polygon points="{area}" fill="{col}" opacity=".10"/>{g}'
            f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5" stroke-linejoin="round"/></svg></figure>')
def barchart(items):
    if not items: return ""
    m = max(abs(v) for _, v in items) or 1; W, rowh = 460, 50; H = rowh * len(items) + 10; mid = W / 2
    g = f'<line x1="{mid}" x2="{mid}" y1="0" y2="{H}" stroke="#151515"/>'
    for i, (t, v) in enumerate(sorted(items, key=lambda x: x[1])):
        y = 8 + i * rowh; w = abs(v) / m * (mid - 110); col = UP if v >= 0 else DN
        x = mid if v >= 0 else mid - w
        g += f'<rect x="{x:.1f}" y="{y}" width="{max(w,2):.1f}" height="30" fill="{col}"/>'
        g += f'<text x="{mid-8 if v>=0 else mid+8}" y="{y+21}" text-anchor="{"end" if v>=0 else "start"}" class="b big">{e(t)}</text>'
        g += f'<text x="{(x+w+8) if v>=0 else (x-8):.1f}" y="{y+21}" text-anchor="{"start" if v>=0 else "end"}" class="b big" fill="{col}">{"+" if v>=0 else "−"}{fmt(abs(v))} %</text>'
    return f'<figure class="chart"><svg viewBox="0 0 {W} {H}" role="img" aria-label="Tagesveränderung">{g}</svg></figure>'

def page(title, body):
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div class="wrap">{body}
<p class="disc">Alle Angaben ohne Gewähr. Keine Anlageberatung – automatisch erstellte Einschätzung auf Basis öffentlicher Quellen.</p></div></body></html>"""
def mast(pre, sub, tickers="", badge="", rubrics="Watchlist · Makro · Ideen"):
    b = f'<div class="sunbadge">{e(badge)}</div>' if badge else ""
    return f"""<header><div class="bar"><span>{e(sub)}</span><span><a href="{pre}index.html">Aktuelle Ausgabe</a> · <a href="{pre}archiv.html">Archiv</a></span></div>
<div class="mast"><a href="{pre}index.html">Limitless Journal</a></div>{b}<div class="bar"{' style="margin-top:8px"' if badge else ""}><span>{e(rubrics)}</span><span>{e(tickers)}</span></div></header>"""
def edition(d, pre):
    H = d.get("watchlist") or d.get("holdings", []); tick = " · ".join(x["ticker"] for x in H)
    h = mast(pre, dlong(d["date"]), tick)
    h += f'<div class="front"><div class="kicker">Die Lage am Morgen</div><h1 class="head">{e(d["headline"])}</h1><p class="lead">{e(d["lead"])}</p><div class="tiles">'
    for x in H:
        sd = series(d, x["ticker"]); dc = pct(sd[-2][1], sd[-1][1]) if len(sd) > 1 else None
        h += f'<div class="tile"><div class="t">{e(x["ticker"])}</div><div class="v">{e(x["close"])}</div>{tag(dc) if dc is not None else e(x["change"])}{spark(sd[-30:])}</div>'
    h += "</div></div>"
    bars = [(x["ticker"], pct(series(d, x["ticker"])[-2][1], series(d, x["ticker"])[-1][1])) for x in H if len(series(d, x["ticker"])) > 1]
    if bars: h += '<section><div class="label">Watchlist im Überblick</div><h2>Tagesveränderung</h2>' + barchart(bars) + '<p class="chartnote">Veränderung zum Vortagesschluss. Daten: Yahoo Finance.</p></section>' 
    for x in H:
        h += f'<section><div class="label">Watchlist · {e(x["ticker"])}</div><h2><span class="badge">{e(x["ticker"][:4])}</span>{e(x["name"])}</h2>'
        h += f'<div class="price"><small>Schlusskurs · Kursveränderung seit letzter Ausgabe</small>{e(x["close"])} <span class="{x["dir"]}">{e(x["change"])}</span></div>'
        h += linechart(series(d, x["ticker"]), f'{x["name"]} – Schlusskurse 3 Monate, $')
        if x.get("figures"): h += '<h3>Kennzahlen</h3><table class="fig">' + "".join(f"<tr><td>{e(k)}</td><td>{e(v)}</td></tr>" for k,v in x["figures"]) + "</table>"
        news = x["news"] if isinstance(x["news"], list) else [x["news"]]
        h += '<h3>Neuigkeiten seit der letzten Ausgabe</h3><ul class="news">' + "".join(f"<li>{e(n)}</li>" for n in news) + "</ul>"
        h += f'<h3>Ausblick</h3><p class="outlook">{e(x["outlook"])}</p></section>'
    h += '<section><div class="label">Der Gesamtmarkt</div><h2>Wall Street am Freitag</h2>' + "".join(f"<p>{e(m)}</p>" for m in d["market"]) + "</section>"
    if d.get("macro"):
        h += '<section><div class="label">Makro</div><h2>Was die Kurse bewegt</h2>'
        ms = [(k, v) for k, v in (d.get("charts") or {}).get("series", {}).items() if k.startswith("^") or "=" in k]
        if ms:
            h += '<div class="tiles">'
            for k, v in ms:
                dt = v["data"]; dc = pct(dt[-2][1], dt[-1][1]) if len(dt) > 1 else 0
                h += f'<div class="tile"><div class="t">{e(v["label"])}</div><div class="v">{fmt(dt[-1][1], 2)}</div>{tag(dc)}{spark(dt[-30:])}</div>'
            h += '</div><div class="mini">' + "".join(linechart(v["data"], v["label"] + " – 3 Monate") for k, v in ms) + '</div><p class="chartnote">Kacheln: Schlusswert und Veränderung zum Vortag. 10-J.-Rendite laut Yahoo (^TNX); offizieller Treasury-Wert im Text.</p>'
        for m in d["macro"]:
            h += f'<div class="macro"><h3>{e(m["title"])}</h3><dl><dt>Was passiert</dt><dd>{e(m["what"])}</dd><dt>Wirkung auf Markt &amp; Watchlist</dt><dd>{e(m["effect"])}</dd><dt>Was das voraussichtlich bedeutet</dt><dd>{e(m["next"])}</dd></dl></div>'
        h += "</section>"
    h += '<section><div class="label">Drei Ideen</div><h2>Noch nicht vom KI-Hype erfasst – mit Potenzial</h2>'
    h += "".join(f'<div class="idea"><h3>{e(i["name"])} ({e(i["ticker"])})</h3><div class="sec">{e(i["sector"])}</div><p>{e(i["why"])}</p></div>' for i in d["ideas"]) + "</section>"
    groups0 = [(f'{x["name"]} ({x["ticker"]})', x.get("sources", [])) for x in H] + [("Gesamtmarkt", d.get("market_sources", []))] + [(f'Makro: {m["title"]}', m.get("sources", [])) for m in d.get("macro", [])]
    groups = groups0 + ([("Charts", [((d.get("charts") or {}).get("source","Yahoo Finance"), "https://finance.yahoo.com/")])] if d.get("charts") else [])
    h += '<section class="sources"><div class="label">Quellen</div>'
    for g, l in groups:
        if l: h += f"<h3>{e(g)}</h3>" + " · ".join(f'<a href="{e(u)}">{e(n)}</a>' for n,u in l)
    h += "</section>"
    return page(f'Limitless Journal – {dlong(d["date"])}', h)

# ---------- Sonntagsausgabe – Wochenausblick (type: "sunday") ----------
SUNDAY_LABEL = "Sonntagsausgabe – Wochenausblick"
CATS = {"fed": ("Notenbanken", "#1f4e9c"), "data": ("Konjunktur", "#5b5b5b"), "earn": ("Quartalszahlen", "#b36b00"),
        "watch": ("Watchlist", "#0b6b0b"), "pol": ("Politik/Trump", "#7a1d1d"), "geo": ("Geopolitik/Handel", "#6a2c91"), "ipo": ("IPO", "#00838f")}
LINECOLS = ["#1f4e9c", "#b36b00", "#0b6b0b", "#7a1d1d", "#6a2c91", "#00838f", "#c2185b", "#455a64"]
DSHORT = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
def close_on(d, sym, iso):
    v = [x for x in series(d, sym) if x[0] <= iso]
    return v[-1] if v else None
def week_change(d, sym):
    a, b = close_on(d, sym, d["week"]["from"]), close_on(d, sym, d["week"]["to"])
    return (a, b, pct(a[1], b[1])) if a and b else None
def chip(cat):
    n, c = CATS.get(cat, (cat, "#555")); return f'<span class="chip" style="background:{c}">{e(n)}</span>'
def legend(cats):
    return '<div class="legend">' + "".join(f'<span><i style="background:{CATS[c][1]}"></i>{e(CATS[c][0])}</span>' for c in CATS if c in cats) + "</div>"
def density(cal):
    """Horizontales gestapeltes Balkendiagramm: Termine je Tag und Kategorie."""
    rows = [(date.fromisoformat(dd["date"]), dd["items"]) for dd in cal]
    m = max(len(i) for _, i in rows) or 1; W, rh, L = 460, 44, 110; H = rh * len(rows) + 8
    g = ""
    for k, (dt, items) in enumerate(rows):
        y = 6 + k * rh; x = L
        g += f'<text x="{L-10}" y="{y+23}" text-anchor="end" class="b big">{DSHORT[dt.weekday()]} {dt.day}.{dt.month}.</text>'
        for c in CATS:
            n = sum(1 for it in items if it["cat"] == c)
            if n:
                w = n / m * (W - L - 60)
                g += f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="30" fill="{CATS[c][1]}"><title>{e(CATS[c][0])}: {n}</title></rect>'
                if w > 18: g += f'<text x="{x+w/2:.1f}" y="{y+21}" text-anchor="middle" style="fill:#fff;font-weight:bold">{n}</text>'
                x += w
        g += f'<text x="{x+8:.1f}" y="{y+21}" class="b">{len(items)}</text>'
    return f'<figure class="chart"><svg viewBox="0 0 {W} {H}" role="img" aria-label="Termine pro Tag">{g}</svg></figure>'
def multiline(d, syms, start, end, title):
    """Indexierter Verlauf (Start = 100) mehrerer Werte."""
    S = []
    for s in syms:
        v = [x for x in series(d, s) if start <= x[0] <= end]
        if len(v) > 1: S.append((s, v))
    if not S: return ""
    W, H, L, R, T, Bm = 500, 340, 44, 96, 18, 56
    dates = sorted({x[0] for _, v in S for x in v}); n = len(dates)
    vals = [x[1] / v[0][1] * 100 for _, v in S for x in v]; lo, hi = min(vals), max(vals); pad = (hi - lo) * .06 or 1; lo -= pad; hi += pad
    X = lambda i: L + i * (W - L - R) / (n - 1); Y = lambda y: T + (hi - y) / (hi - lo) * (H - T - Bm)
    g = ""
    for k in range(5):
        yv = lo + (hi - lo) * k / 4; yy = Y(yv)
        g += f'<line x1="{L}" x2="{W-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#ccc" stroke-dasharray="3 4"/><text x="{L-6}" y="{yy+4:.1f}" text-anchor="end">{fmt(yv,0)}</text>'
    g += f'<line x1="{L}" x2="{W-R}" y1="{Y(100):.1f}" y2="{Y(100):.1f}" stroke="#151515"/>'
    for i, dt in enumerate(dates):
        g += f'<text x="{X(i):.1f}" y="{H-30}" text-anchor="middle">{DSHORT[date.fromisoformat(dt).weekday()]}</text>'
        if i in (0, n - 1): g += f'<text x="{X(i):.1f}" y="{H-6}" text-anchor="middle">{ddm(dt)}</text>'
    labs = []
    for j, (s, v) in enumerate(S):
        col = LINECOLS[j % len(LINECOLS)]; dash = ' stroke-dasharray="6 4"' if s.startswith("^") else ""
        pts = " ".join(f"{X(dates.index(x[0])):.1f},{Y(x[1]/v[0][1]*100):.1f}" for x in v)
        g += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5"{dash}/>'
        labs.append([Y(v[-1][1] / v[0][1] * 100), s, col])
    labs.sort()
    for k in range(1, len(labs)):
        if labs[k][0] - labs[k-1][0] < 19: labs[k][0] = labs[k-1][0] + 19
    lbl = {"^GSPC": "S&P", "^IXIC": "Nasdaq", "^DJI": "Dow"}
    for y, s, col in labs: g += f'<text x="{W-R+6}" y="{y+4:.1f}" class="b" style="fill:{col}">{e(lbl.get(s, s))}</text>'
    return f'<figure class="chart"><figcaption><b>{e(title)}</b></figcaption><svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(title)}">{g}</svg></figure>'
def srclinks(l): return " · ".join(f'<a href="{e(u)}">{e(n)}</a>' for n, u in l)
def sunday(d, pre):
    H = d.get("watchlist", []); tick = " · ".join(x["ticker"] for x in H); wf, wt = d["week"]["from"], d["week"]["to"]
    h = mast(pre, dlong(d["date"]), tick, SUNDAY_LABEL, "Termine · Wochenrückblick · Trading-Ideen")
    h += f'<div class="front"><div class="kicker">{SUNDAY_LABEL}</div><h1 class="head">{e(d["headline"])}</h1><p class="lead">{e(d["lead"])}</p>'
    if d.get("theme"): h += f'<p style="font-family:Helvetica,Arial,sans-serif;font-size:18px;margin-top:22px"><b>THEMA DER WOCHE:</b> {e(d["theme"])}</p>'
    h += '<div class="tiles">'
    for x in H:
        wc = week_change(d, x["ticker"]); sd = [p for p in series(d, x["ticker"]) if p[0] <= wt]
        if wc: h += f'<div class="tile"><div class="t">{e(x["ticker"])} · Woche</div><div class="v">{fmt(wc[1][1])} $</div>{tag(wc[2])}{spark(sd[-30:])}</div>'
    h += "</div></div>"
    # 1) Termine
    cal = d.get("calendar", []); a, b = date.fromisoformat(cal[0]["date"]), date.fromisoformat(cal[-1]["date"])
    h += f'<section><div class="label">Teil 1 · Wichtige Termine</div><h2>Die Woche vom {a.day}. bis {b.day}. {MON[b.month-1]}</h2>'
    if d.get("timezone_note"): h += f'<div class="tznote">🕑 {e(d["timezone_note"])}</div>'
    used = {it["cat"] for dd in cal for it in dd["items"]}
    h += '<h3>Termin-Dichte pro Tag</h3>' + legend(used) + density(cal)
    h += '<h3>Wochenkalender auf einen Blick</h3><div class="weekgrid">'
    for dd in cal:
        dt = date.fromisoformat(dd["date"])
        h += f'<div class="daycard"><div class="dn">{DAY[dt.weekday()]}, {dt.day}.{dt.month}.</div>'
        h += "".join(f'<div class="ev" style="border-left-color:{CATS.get(it["cat"],("","#999"))[1]}"><b>{e(it["time"])}</b> {e(it["title"])}</div>' for it in dd["items"]) + "</div>"
    h += "</div>"
    for dd in cal:
        dt = date.fromisoformat(dd["date"])
        h += f'<div class="day"><h3>{dlong(dd["date"])}</h3>'
        for it in dd["items"]:
            h += f'<div class="ev2"><div class="tm">{e(it["time"])}</div><div>{chip(it["cat"])}<span class="tt">{e(it["title"])}</span>'
            if it.get("note"): h += f'<div class="nt">{e(it["note"])}</div>'
            if it.get("src"): h += f'<div class="sr">Quelle: {srclinks(it["src"])}</div>'
            h += "</div></div>"
        h += "</div>"
    if d.get("lookahead"):
        h += '<h3>Danach im Blick</h3><ul class="look">' + "".join(f'<li><b>{e(t)}</b> – {e(x)} <a href="{e(sv[1])}">({e(sv[0])})</a></li>' for t, x, sv in d["lookahead"]) + "</ul>"
    h += "</section>"
    # 2) Wochenrückblick
    fa, ta = date.fromisoformat(wf), date.fromisoformat(wt)
    h += f'<section><div class="label">Teil 2 · Wochenrückblick der Watchlist</div><h2>So lief die Woche</h2><p class="chartnote">Schlusskurs Freitag, {ta.day}.{ta.month}. ggü. Schlusskurs Freitag, {fa.day}.{fa.month}. Daten: Yahoo Finance.</p>'
    bars = [(x["ticker"], week_change(d, x["ticker"])[2]) for x in H if week_change(d, x["ticker"])]
    idx = [(lbl, week_change(d, s)) for s, lbl in (("^GSPC", "S&P 500"), ("^IXIC", "Nasdaq"), ("^DJI", "Dow Jones"))]
    h += barchart(bars + [(l, w[2]) for l, w in idx if w])
    h += multiline(d, [x["ticker"] for x in H] + ["^GSPC", "^IXIC"], wf, wt, f"Wochenverlauf indexiert ({fa.day}.{fa.month}. = 100) – gestrichelt: Indizes")
    h += f'<table class="wk"><tr><th>Wert</th><th style="text-align:right">{fa.day}.{fa.month}.</th><th style="text-align:right">{ta.day}.{ta.month}.</th><th style="text-align:right">Woche</th></tr>'
    for x in H:
        w = week_change(d, x["ticker"])
        if w: h += f'<tr><td><b>{e(x["ticker"])}</b> {e(x["name"])}</td><td class="n">{fmt(w[0][1])} $</td><td class="n">{fmt(w[1][1])} $</td><td class="n">{tag(w[2])}</td></tr>'
    for s, lbl in (("^GSPC", "S&P 500"), ("^IXIC", "Nasdaq Composite"), ("^DJI", "Dow Jones"), ("BZ=F", "Brent ($/Barrel)"), ("^TNX", "US-Rendite 10 J. (%)"), ("^VIX", "VIX")):
        w = week_change(d, s)
        if w and s == "^TNX":
            bp = round((w[1][1] - w[0][1]) * 100); cl = "up" if bp >= 0 else "down"
            h += f'<tr><td>{e(lbl)}</td><td class="n">{fmt(w[0][1])}</td><td class="n">{fmt(w[1][1])}</td><td class="n"><span class="tag {cl}">{"+" if bp >= 0 else "−"}{abs(bp)} Bp</span></td></tr>'
        elif w: h += f'<tr><td>{e(lbl)}</td><td class="n">{fmt(w[0][1])}</td><td class="n">{fmt(w[1][1])}</td><td class="n">{tag(w[2])}</td></tr>'
    h += "</table>"
    for x in H:
        w = week_change(d, x["ticker"])
        h += f'<div class="stock"><h3><span class="badge">{e(x["ticker"][:4])}</span>{e(x["name"])} {tag(w[2]) if w else ""}</h3><p>{e(x.get("note",""))}</p>'
        h += linechart([p for p in series(d, x["ticker"]) if p[0] <= wt], f'{x["name"]} – Schlusskurse 3 Monate, $')
        if x.get("sources"): h += f'<div class="src">Quellen: {srclinks(x["sources"])}</div>'
        h += "</div>"
    if d.get("review_market"):
        h += '<h3>Der Gesamtmarkt</h3>' + "".join(f"<p>{e(m)}</p>" for m in d["review_market"])
        h += '<div class="mini">' + "".join(linechart([p for p in series(d, s) if p[0] <= wt], (d["charts"]["series"][s]["label"]) + " – 3 Monate") for s in ("^GSPC", "^IXIC", "^TNX", "BZ=F") if series(d, s)) + "</div>"
    h += "</section>"
    # 3) Trading-Ideen
    disc = '<div class="warn"><b>⚠ Keine Anlageberatung.</b> Die folgenden Szenarien sind automatisch erstellte, unverbindliche Einschätzungen auf Basis öffentlicher Quellen – keine Aufforderung zum Kauf oder Verkauf. Aktien und insbesondere Optionen können zum Totalverlust führen. Jede Entscheidung auf eigenes Risiko.</div>'
    h += '<section><div class="label">Teil 3 · Trading-Ideen für die Woche</div><h2>Szenarien &amp; Auslöser</h2>' + disc
    if d.get("ideas_intro"): h += f'<p>{e(d["ideas_intro"])}</p>'
    for i, t in enumerate(d.get("trade_ideas", []), 1):
        h += f'<div class="tidea"><h3>{i}. {e(t["title"])}</h3><dl>'
        for k, lab in (("scenario", "Szenario"), ("assets", "Betroffene Werte/Sektoren"), ("direction", "Mögliche Richtung"), ("trigger", "Auslöser"), ("risks", "Risiken"), ("invalidation", "Entkräftung – was die Idee ungültig macht")):
            h += f'<dt>{lab}</dt><dd{" class=inv" if k=="invalidation" else ""}>{e(t.get(k,""))}</dd>'
        h += "</dl>"
        if t.get("sources"): h += f'<div class="sr" style="font-size:14px">Quellen: {srclinks(t["sources"])}</div>'
        h += "</div>"
    h += disc + "</section>"
    # Quellen
    seen, allsrc = set(), []
    for l in [it.get("src", []) for dd in cal for it in dd["items"]] + [[x[2]] for x in d.get("lookahead", [])] + [x.get("sources", []) for x in H] + [d.get("review_sources", [])] + [t.get("sources", []) for t in d.get("trade_ideas", [])]:
        for n, u in l:
            if u not in seen: seen.add(u); allsrc.append((n, u))
    h += '<section class="sources"><div class="label">Quellen</div><h3>Termine, Rückblick &amp; Ideen</h3><ol>' + "".join(f'<li><a href="{e(u)}">{e(n)}</a></li>' for n, u in allsrc) + "</ol>"
    if d.get("charts"): h += f'<h3>Charts</h3><a href="https://finance.yahoo.com/">{e(d["charts"].get("source","Yahoo Finance"))}</a>'
    h += "</section>"
    return page(f'Limitless Journal – {SUNDAY_LABEL} – {dlong(d["date"])}', h)
def render(d, pre): return sunday(d, pre) if d.get("type") == "sunday" else edition(d, pre)
eds = sorted((json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(B,"editions","*.json"))), key=lambda x: x["date"], reverse=True)
os.makedirs(os.path.join(B,"ausgabe"), exist_ok=True)
for d in eds: open(os.path.join(B,"ausgabe",d["date"]+".html"),"w",encoding="utf-8").write(render(d,"../"))
if eds: open(os.path.join(B,"index.html"),"w",encoding="utf-8").write(render(eds[0],""))
a = mast("", "Archiv") + '<div class="front"><h1 class="head">Archiv</h1></div>'; cur = None
for d in eds:
    dt = date.fromisoformat(d["date"]); m = f"{MON[dt.month-1]} {dt.year}"
    if m != cur: a += ("</ul>" if cur else "") + f'<h2>{m}</h2><ul class="arch">'; cur = m
    st = f'<span class="archtag">{SUNDAY_LABEL}</span>' if d.get("type") == "sunday" else ""
    a += f'<li>{st}<a href="ausgabe/{d["date"]}.html">{dlong(d["date"])}</a> – {e(d["headline"])}</li>'
a += "</ul>" if cur else "<p>Noch keine Ausgaben.</p>"
open(os.path.join(B,"archiv.html"),"w",encoding="utf-8").write(page("Archiv – Limitless Journal", a))
print(f"{len(eds)} Ausgabe(n) gebaut.")
