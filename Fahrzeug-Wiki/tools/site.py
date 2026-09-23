"""Erzeugt aus dem Markdown-Wiki eine statische HTML-Seite unter site/ (für localhost).

Aufruf:  python tools/site.py      danach:  python -m http.server 8765  (im Wiki-Root)  →  http://localhost:8765
Die Bilder werden nicht kopiert, sondern relativ aus ../Bilder/ geladen.
"""
import html
import json
import re
from collections import defaultdict
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"

SECTIONS = [  # (Ordner, Bereichsname)
    ("wiki/synthesis", "Übersichten"),
    ("wiki/entities/hersteller", "Hersteller"),
    ("wiki/entities/fahrzeuge", "Fahrzeuge"),
    ("wiki/concepts", "Fachbegriffe"),
    ("wiki/sources", "Quellen"),
]

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
EMBED = re.compile(r"!\[\[([^\]|\\]+)(?:\\?\|(\d+))?\]\]")
WIKILINK = re.compile(r"\[\[([^\]|\\#]+)(?:\\?\|([^\]]+))?\]\]")
H1 = re.compile(r"^# (.+)$", re.M)


def parse_frontmatter(text):
    m = FRONTMATTER.match(text)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            v = v.strip()
            try:
                meta[k.strip()] = json.loads(v)
            except json.JSONDecodeError:
                meta[k.strip()] = v
        text = text[m.end():]
    return meta, text


def load_pages():
    pages = {}
    for folder, section in SECTIONS:
        for p in sorted((ROOT / folder).glob("*.md")):
            meta, body = parse_frontmatter(p.read_text(encoding="utf-8"))
            title = H1.search(body).group(1).strip()
            pages[p.stem] = {"title": title, "section": section, "meta": meta, "body": body}
    for name, title in [("index", "Index"), ("log", "Protokoll")]:
        body = (ROOT / f"{name}.md").read_text(encoding="utf-8")
        pages[name] = {"title": title, "section": "Wiki", "meta": {}, "body": body}
    ci = ROOT / "ci" / "CI-Leitfaden.md"
    if ci.exists():
        pages["corporate-identity"] = {"title": "Corporate Identity", "section": "Wiki", "meta": {},
                                       "body": ci.read_text(encoding="utf-8")}
    return pages


def to_html(slug, page, pages):
    body = page["body"]
    body = EMBED.sub(lambda m: f'<img src="../Bilder/{m.group(1)}" width="{m.group(2) or 300}" alt="" loading="lazy">', body)
    body = body.replace("](../../../Bilder/", "](../Bilder/")

    def link(m):
        target, label = m.group(1).strip(), m.group(2)
        if target not in pages:
            return html.escape(label or target)
        return f"[{label or pages[target]['title']}]({target}.html)"

    body = WIKILINK.sub(link, body)
    # Zahl und Einheit nicht trennen (geschütztes Leerzeichen)
    body = re.sub(r"(\d) (kWh|%|km|kW)(?!\w)", r"\1&nbsp;\2", body)
    return markdown.markdown(body, extensions=["tables", "sane_lists"], output_format="html5")


def backlinks(pages):
    back = defaultdict(set)
    for slug, p in pages.items():
        if slug in ("index", "log"):
            continue
        for m in WIKILINK.finditer(p["body"]):
            t = m.group(1).strip()
            if t in pages and t != slug:
                back[t].add(slug)
    return back


def nav(pages, current):
    groups = [("Wiki", ["index"])]
    groups += [(name, [s for s, p in pages.items() if p["section"] == name]) for _, name in SECTIONS]
    out = []
    for name, slugs in groups:
        if name == "Fahrzeuge":
            # nach Hersteller gruppiert
            by_brand = defaultdict(list)
            for s in slugs:
                by_brand[pages[s]["meta"].get("hersteller", "?")].append(s)
            inner = []
            for brand in sorted(by_brand):
                open_ = " open" if current in by_brand[brand] else ""
                items = "".join(nav_item(pages, s, current) for s in by_brand[brand])
                inner.append(f"<details{open_}><summary>{html.escape(brand)} <span class='n'>{len(by_brand[brand])}</span></summary><ul>{items}</ul></details>")
            out.append(f"<h3>Fahrzeuge <span class='n'>{len(slugs)}</span></h3>{''.join(inner)}")
            continue
        items = "".join(nav_item(pages, s, current) for s in sorted(slugs, key=lambda s: pages[s]["title"].lower()) if s != "log")
        if name == "Wiki":
            items = "".join(nav_item(pages, s, current) for s in ("index", "corporate-identity", "log") if s in pages)
        open_ = " open" if name != "Fachbegriffe" or pages.get(current, {}).get("section") == name else ""
        out.append(f"<details class='sec'{open_}><summary><h3>{name} <span class='n'>{len(slugs)}</span></h3></summary><ul>{items}</ul></details>")
    return "\n".join(out)


def nav_item(pages, s, current):
    cls = " class='active'" if s == current else ""
    return f"<li><a href='{s}.html'{cls}>{html.escape(pages[s]['title'])}</a></li>"


CSS = """
/* Farben, Schriften, Radien kommen aus ci/tokens.css (Corporate Identity) */
:root{--bg:var(--fw-bg);--panel:var(--fw-surface);--ink:var(--fw-ink);--muted:var(--fw-muted);--line:var(--fw-line);
  --accent:var(--fw-primary);--accent-soft:var(--fw-primary-soft);--code:var(--fw-surface-2)}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--bg);color:var(--ink);font:16px/1.6 var(--fw-font-text);display:grid;grid-template-columns:290px minmax(0,1fr);min-height:100vh;-webkit-font-smoothing:antialiased}
h1,h2,h3,.stat b,.brand{font-family:var(--fw-font-display);letter-spacing:-.01em}
aside{background:var(--panel);border-right:1px solid var(--line);padding:18px 16px;position:sticky;top:0;height:100vh;overflow-y:auto;font-size:14px}
aside .brand{display:flex;align-items:center;gap:10px;margin-bottom:6px;color:var(--ink);text-decoration:none;font-size:19px;font-weight:500}
aside .brand img{width:34px;height:34px}
aside .brand b{color:var(--accent);font-weight:700}
aside .claim{font-size:12px;color:var(--muted);margin:0 0 14px 44px}
aside .ask{width:100%;display:flex;align-items:center;justify-content:center;gap:8px;margin:0 0 12px;padding:9px 12px;border:0;border-radius:var(--fw-radius-m);
  background:var(--accent);color:var(--fw-on-primary);font:600 14px var(--fw-font-text);cursor:pointer}
aside .ask:hover{background:var(--fw-primary-strong)}
aside .ask svg{width:16px;height:16px;color:var(--fw-accent)}
table{font-variant-numeric:tabular-nums}
aside input{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);font:inherit;margin-bottom:10px}
aside h3{display:inline;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0}
aside details{margin:4px 0}aside summary{cursor:pointer;padding:4px 0;list-style-position:outside}
aside details.sec{margin-top:10px}
aside ul{list-style:none;margin:2px 0 6px;padding-left:10px}
aside li a{display:block;padding:2px 8px;border-radius:6px;color:var(--ink);text-decoration:none}
aside li a:hover{background:var(--accent-soft)}aside li a.active{background:var(--accent);color:var(--fw-on-primary)}
aside > h3{display:block;margin-top:14px}
.n{color:var(--muted);font-weight:400;font-size:11px}
#results{margin-bottom:8px}#results a{display:block;padding:3px 8px;border-radius:6px;color:var(--ink);text-decoration:none}#results a:hover{background:var(--accent-soft)}#results small{color:var(--muted)}
main{padding:32px 48px 80px;max-width:1080px;width:100%;min-width:0;overflow-wrap:break-word}
.crumb{font-size:13px;color:var(--muted);margin-bottom:6px}
h1{font-size:34px;line-height:1.2;margin:.2em 0 .5em}h2{margin-top:1.8em;padding-bottom:4px;border-bottom:1px solid var(--line);font-size:22px}h3{font-size:18px}
a{color:var(--accent)}
main img{max-width:100%;height:auto;border-radius:10px;display:block}
main p > img:first-child{max-height:460px;object-fit:cover;width:100%}
td img{border-radius:6px}
blockquote{margin:1em 0;padding:12px 16px;background:var(--accent-soft);border-left:4px solid var(--accent);border-radius:0 8px 8px 0}
blockquote p{margin:0}
table{border-collapse:collapse;width:100%;margin:1em 0;font-size:14.5px;display:block;overflow-x:auto}
th,td{border-bottom:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:middle}
th{background:var(--code);font-weight:600;white-space:nowrap}
tr:hover td{background:color-mix(in srgb,var(--accent-soft) 50%,transparent)}
code{background:var(--code);padding:1px 5px;border-radius:4px;font-size:.9em}
em{color:var(--muted)}
.back{margin-top:3em;padding-top:1em;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}
.back a{margin-right:.6em}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;margin:1em 0 2em}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;text-decoration:none;color:var(--ink);transition:transform .15s ease,box-shadow .15s ease}
.card:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.08)}
.card img{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:0}
.card div{padding:8px 12px 10px}.card b{display:block;font-size:14.5px}.card small{color:var(--muted);font-size:12.5px}
.stats{display:flex;gap:12px;flex-wrap:wrap;margin:1em 0}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 16px}.stat b{font-size:24px;display:block}.stat span{color:var(--muted);font-size:13px}
.menu{display:none}
@media (max-width:860px){body{grid-template-columns:minmax(0,1fr)}aside{position:static;height:auto;display:none}aside.open{display:block}main{padding:16px}.menu{display:block;margin:12px 16px 0;padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink);font:inherit}}
"""

JS = """
const box=document.getElementById('q'),res=document.getElementById('results');
box.addEventListener('input',()=>{const q=box.value.trim().toLowerCase();res.innerHTML='';if(q.length<2)return;
 SEARCH.filter(p=>(p.t+' '+p.s+' '+(p.h||'')).toLowerCase().includes(q)).slice(0,25)
 .forEach(p=>{const a=document.createElement('a');a.href=p.u;a.innerHTML=p.t+' <small>'+p.s+'</small>';res.appendChild(a)});});
document.querySelector('.menu').addEventListener('click',()=>document.querySelector('aside').classList.toggle('open'));
document.querySelector('.ask').addEventListener('click',()=>window.FahrzeugWikiChat&&window.FahrzeugWikiChat.open());
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap">')
BOLT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.2 2.5 4.8 13.1h5.9l-2.4 8.4 9-11.4h-5.8l1.7-7.6z" fill="currentColor"/></svg>'


def page_html(title, content, navhtml, search_json):
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Fahrzeug-Wiki</title>
<link rel="icon" href="../ci/signet.svg" type="image/svg+xml">
{FONTS}<link rel="stylesheet" href="../ci/tokens.css"><style>{CSS}</style></head>
<body><button class="menu">☰ Navigation</button>
<aside><a class="brand" href="index.html"><img src="../ci/signet.svg" alt="">Fahrzeug<b>Wiki</b></a>
<p class="claim">Jede Batterie. Jede Variante. Belegt.</p>
<button class="ask" type="button">{BOLT}Ampere fragen</button>
<input id="q" type="search" placeholder="Suchen … (Modell, Begriff, Marke)" autocomplete="off"><div id="results"></div>
{navhtml}</aside>
<main>{content}</main>
<script>const SEARCH={search_json};{JS}</script>
<script src="../chat/widget/fw-chat.js" defer></script></body></html>"""


def landing(pages):
    vehicles = [s for s, p in pages.items() if p["section"] == "Fahrzeuge"]
    by_brand = defaultdict(list)
    for s in vehicles:
        by_brand[pages[s]["meta"].get("hersteller", "?")].append(s)
    n_var = sum(int(pages[s]["meta"].get("varianten", 0)) for s in vehicles)
    parts = ["<div class='crumb'>Knowledge Base</div><h1>Jede Batterie. Jede Variante. Belegt.</h1>",
             "<p>Alle Elektrofahrzeuge aus dem Batteriecheck-Bestand – mit Bild, Einordnung, Brutto-/Nettokapazität "
             "jeder Variante und Erklärungen der Fachbegriffe. Fragen? <a href='#' onclick='FahrzeugWikiChat.open();return false'>"
             "Frag Ampere</a>, den Wiki-Assistenten.</p>",
             "<div class='stats'>"
             f"<div class='stat'><b>{len(vehicles)}</b><span>Modellreihen</span></div>"
             f"<div class='stat'><b>{n_var}</b><span>Varianten</span></div>"
             f"<div class='stat'><b>{len(by_brand)}</b><span>Hersteller</span></div>"
             f"<div class='stat'><b>{sum(1 for p in pages.values() if p['section'] == 'Fachbegriffe')}</b><span>Fachbegriffe</span></div></div>",
             "<p><a href='fahrzeuguebersicht.html'>Fahrzeugübersicht</a> · <a href='puffer-analyse.html'>Puffer-Analyse</a> · "
             "<a href='datenqualitaet.html'>Datenqualität</a> · <a href='tn-batterycheck-alle-daten.html'>Rohquelle</a></p>"]
    for brand in sorted(by_brand):
        bslug = next((s for s, p in pages.items() if p["section"] == "Hersteller" and p["title"] == brand), None)
        head = f"<a href='{bslug}.html'>{html.escape(brand)}</a>" if bslug else html.escape(brand)
        parts.append(f"<h2>{head}</h2><div class='cards'>")
        for s in by_brand[brand]:
            m = pages[s]["meta"]
            img = f"<img src='../{m['bild']}' alt='' loading='lazy'>" if m.get("bild") else ""
            netto = f"{m.get('netto_min')}–{m.get('netto_max')}" if m.get("netto_min") != m.get("netto_max") else f"{m.get('netto_min')}"
            netto = netto.replace(".", ",")
            parts.append(f"<a class='card' href='{s}.html'>{img}<div><b>{html.escape(pages[s]['title'])}</b>"
                         f"<small>{html.escape(str(m.get('segment', '')))} · netto {netto} kWh</small></div></a>")
        parts.append("</div>")
    return "\n".join(parts)


def main():
    pages = load_pages()
    back = backlinks(pages)
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    search = json.dumps([{"t": p["title"], "s": p["section"] if p["section"] != "Fahrzeuge" else p["meta"].get("hersteller", ""),
                          "h": " ".join(p["meta"].get("tags", [])) if isinstance(p["meta"].get("tags"), list) else "",
                          "u": f"{s}.html"} for s, p in pages.items()], ensure_ascii=False)
    for slug, p in pages.items():
        content = f"<div class='crumb'>{html.escape(p['section'])}</div>" + to_html(slug, p, pages)
        if back.get(slug):
            links = " ".join(f"<a href='{b}.html'>{html.escape(pages[b]['title'])}</a>"
                             for b in sorted(back[slug], key=lambda b: pages[b]["title"].lower()))
            content += f"<div class='back'><b>Verlinkt von ({len(back[slug])}):</b> {links}</div>"
        name = "katalog" if slug == "index" else slug
        (OUT / f"{name}.html").write_text(page_html(p["title"], content.replace("href='index.html'", "href='katalog.html'")
                                                    .replace('href="index.html"', 'href="katalog.html"'),
                                                    nav(pages, slug).replace("href='index.html'", "href='katalog.html'"),
                                                    search.replace('"index.html"', '"katalog.html"')), encoding="utf-8")
    navhtml = nav(pages, None).replace("href='index.html'", "href='katalog.html'")
    (OUT / "index.html").write_text(page_html("Start", landing(pages), navhtml, search.replace('"index.html"', '"katalog.html"')), encoding="utf-8")
    (ROOT / "index.html").write_text('<!doctype html><meta http-equiv="refresh" content="0; url=site/index.html">'
                                     '<a href="site/index.html">Fahrzeug-Wiki öffnen</a>', encoding="utf-8")
    print(f"{len(pages) + 1} HTML-Seiten in {OUT}")


if __name__ == "__main__":
    main()
