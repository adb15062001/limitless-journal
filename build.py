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
body{background:#f4efe4;color:#151515;font-family:Georgia,'Times New Roman',serif;margin:0;font-size:21px;line-height:1.6}
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
@media(max-width:700px){body{font-size:18px}.mast{font-size:44px}h1.head{font-size:38px}h2{font-size:34px}.lead{font-size:20px}.wrap{padding:16px}}"""
def page(title, body):
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div class="wrap">{body}
<p class="disc">Alle Angaben ohne Gewähr. Keine Anlageberatung – automatisch erstellte Einschätzung auf Basis öffentlicher Quellen.</p></div></body></html>"""
def mast(pre, sub, tickers=""):
    return f"""<header><div class="bar"><span>{e(sub)}</span><span><a href="{pre}index.html">Aktuelle Ausgabe</a> · <a href="{pre}archiv.html">Archiv</a></span></div>
<div class="mast"><a href="{pre}index.html">Die KI-Börsenzeitung</a></div><div class="bar"><span>Depot · Makro · Ideen</span><span>{e(tickers)}</span></div></header>"""
def edition(d, pre):
    H = d["holdings"]; tick = " · ".join(x["ticker"] for x in H)
    h = mast(pre, dlong(d["date"]), tick)
    h += f'<div class="front"><div class="kicker">Die Lage am Morgen</div><h1 class="head">{e(d["headline"])}</h1><p class="lead">{e(d["lead"])}</p><div class="ticker">'
    h += "".join(f'<span>{e(x["ticker"])} {e(x["close"])} <span class="{x["dir"]}">{e(x["change"])}</span></span>' for x in H) + "</div></div>"
    for x in H:
        h += f'<section><div class="label">Ihr Depot · {e(x["ticker"])}</div><h2>{e(x["name"])}</h2>'
        h += f'<div class="price"><small>Schlusskurs · Kursveränderung seit letzter Ausgabe</small>{e(x["close"])} <span class="{x["dir"]}">{e(x["change"])}</span></div>'
        if x.get("figures"): h += '<h3>Kennzahlen</h3><table class="fig">' + "".join(f"<tr><td>{e(k)}</td><td>{e(v)}</td></tr>" for k,v in x["figures"]) + "</table>"
        news = x["news"] if isinstance(x["news"], list) else [x["news"]]
        h += '<h3>Neuigkeiten seit der letzten Ausgabe</h3><ul class="news">' + "".join(f"<li>{e(n)}</li>" for n in news) + "</ul>"
        h += f'<h3>Ausblick</h3><p class="outlook">{e(x["outlook"])}</p></section>'
    h += '<section><div class="label">Der Gesamtmarkt</div><h2>Wall Street am Freitag</h2>' + "".join(f"<p>{e(m)}</p>" for m in d["market"]) + "</section>"
    if d.get("macro"):
        h += '<section><div class="label">Makro</div><h2>Was die Kurse bewegt</h2>'
        for m in d["macro"]:
            h += f'<div class="macro"><h3>{e(m["title"])}</h3><dl><dt>Was passiert</dt><dd>{e(m["what"])}</dd><dt>Wirkung auf Markt &amp; Depot</dt><dd>{e(m["effect"])}</dd><dt>Was das voraussichtlich bedeutet</dt><dd>{e(m["next"])}</dd></dl></div>'
        h += "</section>"
    h += '<section><div class="label">Drei Ideen</div><h2>Noch nicht vom KI-Hype erfasst – mit Potenzial</h2>'
    h += "".join(f'<div class="idea"><h3>{e(i["name"])} ({e(i["ticker"])})</h3><div class="sec">{e(i["sector"])}</div><p>{e(i["why"])}</p></div>' for i in d["ideas"]) + "</section>"
    groups = [(f'{x["name"]} ({x["ticker"]})', x.get("sources", [])) for x in H] + [("Gesamtmarkt", d.get("market_sources", []))] + [(f'Makro: {m["title"]}', m.get("sources", [])) for m in d.get("macro", [])]
    h += '<section class="sources"><div class="label">Quellen</div>'
    for g, l in groups:
        if l: h += f"<h3>{e(g)}</h3>" + " · ".join(f'<a href="{e(u)}">{e(n)}</a>' for n,u in l)
    h += "</section>"
    return page(f'Die KI-Börsenzeitung – {dlong(d["date"])}', h)
eds = sorted((json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(B,"editions","*.json"))), key=lambda x: x["date"], reverse=True)
os.makedirs(os.path.join(B,"ausgabe"), exist_ok=True)
for d in eds: open(os.path.join(B,"ausgabe",d["date"]+".html"),"w",encoding="utf-8").write(edition(d,"../"))
if eds: open(os.path.join(B,"index.html"),"w",encoding="utf-8").write(edition(eds[0],""))
a = mast("", "Archiv") + '<div class="front"><h1 class="head">Archiv</h1></div>'; cur = None
for d in eds:
    dt = date.fromisoformat(d["date"]); m = f"{MON[dt.month-1]} {dt.year}"
    if m != cur: a += ("</ul>" if cur else "") + f'<h2>{m}</h2><ul class="arch">'; cur = m
    a += f'<li><a href="ausgabe/{d["date"]}.html">{dlong(d["date"])}</a> – {e(d["headline"])}</li>'
a += "</ul>" if cur else "<p>Noch keine Ausgaben.</p>"
open(os.path.join(B,"archiv.html"),"w",encoding="utf-8").write(page("Archiv – Die KI-Börsenzeitung", a))
print(f"{len(eds)} Ausgabe(n) gebaut.")
