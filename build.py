#!/usr/bin/env python3
"""Baut index.html, archiv.html und ausgabe/YYYY-MM-DD.html aus editions/*.json."""
import json, glob, os, html
from datetime import date
B = os.path.dirname(os.path.abspath(__file__))
MON = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]
DAY = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
e = html.escape
def dlong(s):
    d = date.fromisoformat(s); return f"{DAY[d.weekday()]}, {d.day}. {MON[d.month-1]} {d.year}"
CSS = """body{background:#f4efe4;color:#1a1a1a;font-family:Georgia,'Times New Roman',serif;margin:0}
.wrap{max-width:1100px;margin:auto;padding:20px}
header{text-align:center;border-bottom:4px double #1a1a1a;padding-bottom:8px}
.mast{font-family:'Old English Text MT','UnifrakturMaguntia',Georgia,serif;font-size:56px;margin:6px 0;letter-spacing:1px}
.mast a{color:inherit;text-decoration:none}
.bar{display:flex;justify-content:space-between;border-top:1px solid #1a1a1a;border-bottom:1px solid #1a1a1a;padding:4px 0;font-size:13px;text-transform:uppercase;letter-spacing:1px}
.bar a{color:#1a1a1a}
h1.head{font-size:40px;text-align:center;margin:18px 0 6px;line-height:1.1}
.lead{text-align:center;font-style:italic;font-size:18px;max-width:800px;margin:0 auto 16px}
.cols{column-count:2;column-gap:32px;column-rule:1px solid #999}
article{break-inside:avoid;margin-bottom:18px}
h2.sec{border-bottom:2px solid #1a1a1a;text-transform:uppercase;letter-spacing:2px;font-size:16px;margin-top:26px}
h3{margin:4px 0;font-size:22px}
.kurs{font-family:Helvetica,Arial,sans-serif;font-weight:bold}
.down{color:#a40000}.up{color:#006400}
.src{font-size:12px;color:#444}.src a{color:#444}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.three div{border-top:3px solid #1a1a1a;padding-top:6px}
.disc{border-top:1px solid #1a1a1a;margin-top:30px;font-size:12px;text-align:center;padding-top:8px}
ul.arch li{margin:4px 0}
@media(max-width:700px){.cols{column-count:1}.three{grid-template-columns:1fr}.mast{font-size:34px}}"""
def page(title, body, pre=""):
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div class="wrap">{body}
<div class="disc">Alle Angaben ohne Gewähr. Keine Anlageberatung – nur eine automatisch erstellte Einschätzung auf Basis öffentlicher Quellen.</div></div></body></html>"""
def mast(pre, sub):
    return f"""<header><div class="bar"><span>{e(sub)}</span><span><a href="{pre}index.html">Aktuell</a> · <a href="{pre}archiv.html">Archiv</a></span></div>
<div class="mast"><a href="{pre}index.html">Die KI-Börsenzeitung</a></div><div class="bar"><span>Ihr Depot · Der Markt · Die Ideen</span><span>LMND · CRWV · UBER · NBIS</span></div></header>"""
def srcs(l): return '<div class="src">Quellen: ' + " · ".join(f'<a href="{e(u)}">{e(n)}</a>' for n,u in l) + "</div>"
def edition(d, pre):
    h = mast(pre, dlong(d["date"])) + f'<h1 class="head">{e(d["headline"])}</h1><p class="lead">{e(d["lead"])}</p>'
    h += '<h2 class="sec">Ihr Depot</h2><div class="cols">'
    for x in d["holdings"]:
        h += f'<article><h3>{e(x["name"])} ({e(x["ticker"])})</h3><div class="kurs">Schluss: {e(x["close"])} · Kursveränderung seit letzter Ausgabe: <span class="{x["dir"]}">{e(x["change"])}</span></div><p><b>Neuigkeiten seit der letzten Ausgabe:</b> {e(x["news"])}</p><p><b>Ausblick:</b> {e(x["outlook"])}</p>{srcs(x["sources"])}</article>'
    h += '</div><h2 class="sec">Der Gesamtmarkt</h2><div class="cols">' + "".join(f"<p>{e(m)}</p>" for m in d["market"]) + srcs(d["market_sources"]) + "</div>"
    h += '<h2 class="sec">Drei Ideen: Noch nicht vom KI-Hype erfasst – mit Potenzial</h2><div class="three">'
    h += "".join(f'<div><h3>{e(i["name"])} ({e(i["ticker"])})</h3><i>{e(i["sector"])}</i><p>{e(i["why"])}</p></div>' for i in d["ideas"]) + "</div>"
    return page(f'Die KI-Börsenzeitung – {dlong(d["date"])}', h)
eds = sorted((json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(B,"editions","*.json"))), key=lambda x: x["date"], reverse=True)
os.makedirs(os.path.join(B,"ausgabe"), exist_ok=True)
for d in eds: open(os.path.join(B,"ausgabe",d["date"]+".html"),"w",encoding="utf-8").write(edition(d,"../"))
if eds: open(os.path.join(B,"index.html"),"w",encoding="utf-8").write(edition(eds[0],""))
a = mast("", "Archiv") + '<h1 class="head">Archiv</h1>'; cur = None
for d in eds:
    dt = date.fromisoformat(d["date"]); m = f"{MON[dt.month-1]} {dt.year}"
    if m != cur: a += ("</ul>" if cur else "") + f'<h2 class="sec">{m}</h2><ul class="arch">'; cur = m
    a += f'<li><a href="ausgabe/{d["date"]}.html">{dlong(d["date"])}</a> – {e(d["headline"])}</li>'
a += "</ul>" if cur else "<p>Noch keine Ausgaben.</p>"
open(os.path.join(B,"archiv.html"),"w",encoding="utf-8").write(page("Archiv – Die KI-Börsenzeitung", a))
print(f"{len(eds)} Ausgabe(n) gebaut.")
