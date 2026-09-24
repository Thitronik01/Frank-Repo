"""Erzeugt aus dem Markdown-Wiki die HTML-App unter site/ (für localhost).

Aufruf:  python tools/site.py   →  danach  python chat/server.py  (oder python -m http.server 8765 im Wiki-Root)
Gestaltung: CI-Tokens aus ci/tokens.css, Layout/Komponenten in tools/site_assets/app.css, Verhalten in app.js.
Die Bilder werden nicht kopiert, sondern relativ aus ../Bilder/ geladen.
"""
import hashlib
import html
import json
import re
import shutil
import unicodedata
from collections import defaultdict
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
ASSETS = Path(__file__).resolve().parent / "site_assets"
REPO_ISSUES = "https://github.com/Thitronik01/Frank-Repo/issues"

SECTIONS = [  # (Ordner, Bereichsname)
    ("wiki/synthesis", "Übersichten"),
    ("wiki/entities/hersteller", "Hersteller"),
    ("wiki/entities/fahrzeuge", "Fahrzeuge"),
    ("wiki/concepts", "Fachbegriffe"),
    ("wiki/sources", "Quellen"),
]
KIND = {"Fahrzeuge": "Fahrzeug", "Hersteller": "Hersteller", "Fachbegriffe": "Fachbegriff",
        "Übersichten": "Übersicht", "Quellen": "Quelle", "Wiki": "Wiki"}

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
EMBED = re.compile(r"!\[\[([^\]|\\]+)(?:\\?\|(\d+))?\]\]")
WIKILINK = re.compile(r"\[\[([^\]|\\#]+)(?:\\?\|([^\]]+))?\]\]")
H1 = re.compile(r"^# (.+)$", re.M)
H2 = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.S)
esc = html.escape

# ---------------------------------------------------------------- Icons (Lucide-Stil, 24×24, Strich)
_ICON_PATHS = {
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "search": '<circle cx="11" cy="11" r="7.5"/><path d="m20.5 20.5-4.2-4.2"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "chev": '<path d="m9 18 6-6-6-6"/>',
    "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2h-4v-7H9v7H5a2 2 0 0 1-2-2z"/>',
    "car": '<path d="M5 17H3a1 1 0 0 1-1-1v-3.4a2 2 0 0 1 .2-.9l1.6-3.3A2 2 0 0 1 5.6 7h9.2a2 2 0 0 1 1.5.7L19 11l1.8.5A1.6 1.6 0 0 1 22 13v3a1 1 0 0 1-1 1h-2"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M9 17h6"/>',
    "factory": '<path d="M2 20V8l6 4V8l6 4V4h8v16a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2Z"/><path d="M7 18h1M12 18h1M17 18h1"/>',
    "book": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M8 17v-4M13 17V7M18 17v-7"/>',
    "table": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
    "alert": '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/>',
    "db": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "battery": '<rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 11v2M6 11v2M10 11v2"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
    "percent": '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "external": '<path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
}


def icon(name, cls=""):
    return (f'<svg class="i {cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            f'{_ICON_PATHS[name]}</svg>')


BOLT = ('<svg class="i bolt" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path d="M13.2 2.5 4.8 13.1h5.9l-2.4 8.4 9-11.4h-5.8l1.7-7.6z" fill="currentColor" stroke="none"/></svg>')


# ---------------------------------------------------------------- Laden
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
    for name, title in [("index", "Katalog"), ("log", "Protokoll")]:
        body = (ROOT / f"{name}.md").read_text(encoding="utf-8")
        pages[name] = {"title": title, "section": "Wiki", "meta": {}, "body": body}
    ci = ROOT / "ci" / "CI-Leitfaden.md"
    if ci.exists():
        pages["corporate-identity"] = {"title": "Corporate Identity", "section": "Wiki", "meta": {},
                                       "body": ci.read_text(encoding="utf-8")}
    return pages


def skey(text):
    """Sortierschlüssel ohne Akzente (Škoda neben Seat, Citroën neben Cupra)."""
    return unicodedata.normalize("NFD", str(text)).encode("ascii", "ignore").decode().lower()


def href(slug):
    return "katalog.html" if slug == "index" else f"{slug}.html"


def de(x):
    s = f"{float(x):.1f}"
    return (s[:-2] if s.endswith(".0") else s).replace(".", ",")


def rng(a, b):
    return de(a) if float(a) == float(b) else f"{de(a)}–{de(b)}"


def md_section(body, title):
    m = re.search(rf"^## {re.escape(title)}\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return m.group(1) if m else ""


def plain(md_text):
    t = WIKILINK.sub(lambda m: m.group(2) or m.group(1), md_text)
    return re.sub(r"[*_`>]", "", t).strip()


def build_info(pages):
    """Kennzahlen je Fahrzeug und Hersteller für Karten, Kacheln und Suche."""
    brand_slug = {p["title"]: s for s, p in pages.items() if p["section"] == "Hersteller"}
    vinfo = {}
    for s, p in pages.items():
        if p["section"] != "Fahrzeuge":
            continue
        m, body = p["meta"], p["body"]
        pm = re.search(r"batteriepuffer\\\|Puffer\]\]\s*\|\s*([^|]+?)\s*\|", body)
        kurz = re.search(r"^> (.+)$", body, re.M)
        issues = [l for l in md_section(body, "Offene Punkte").splitlines() if l.startswith("- ")]
        hard = any(k in l for l in issues for k in ("**Zu prüfen:**", "**Näherungswert:**"))
        variants = [l.split("|")[1].strip() for l in md_section(body, "Varianten und Batterien").splitlines()
                    if l.startswith("| ") and not l.startswith("| Variante")]
        vinfo[s] = {
            "title": p["title"], "brand": m.get("hersteller", ""), "bslug": brand_slug.get(m.get("hersteller")),
            "segment": m.get("segment", ""), "plattform": m.get("plattform", ""), "karosserie": m.get("karosserie", ""),
            "bauzeit": m.get("bauzeit", ""), "n": int(m.get("varianten", 0)),
            "bmin": m.get("brutto_min"), "bmax": m.get("brutto_max"), "nmin": m.get("netto_min"), "nmax": m.get("netto_max"),
            "puffer": pm.group(1).replace("%", "").strip() if pm else "", "img": m.get("bild", ""),
            "kurz": plain(kurz.group(1)) if kurz else "", "issues": len(issues), "hard": hard,
            "variants": sorted(set(variants)),
        }
    binfo = defaultdict(list)
    for s, v in vinfo.items():
        binfo[v["brand"]].append(s)
    return vinfo, binfo, brand_slug


# ---------------------------------------------------------------- Markdown → HTML
def render(page, pages):
    body = page["body"]
    body = EMBED.sub(lambda m: f'<img src="../Bilder/{m.group(1)}" width="{m.group(2) or 300}" alt="" loading="lazy">', body)
    body = body.replace("](../../../Bilder/", "](../Bilder/")

    def link(m):
        target, label = m.group(1).strip(), m.group(2)
        if target not in pages:
            return esc(label or target)
        return f"[{label or pages[target]['title']}]({href(target)})"

    body = WIKILINK.sub(link, body)
    body = re.sub(r"(\d) (kWh|%|km|kW)(?!\w)", r"\1&nbsp;\2", body)  # Zahl und Einheit nicht trennen
    return markdown.markdown(body, extensions=["tables", "sane_lists", "toc"],
                             extension_configs={"toc": {"slugify": slugify_unicode}}, output_format="html5")


def split_sections(h):
    parts = re.split(r'(?=<h2 id=")', h)
    secs = []
    for p in parts[1:]:
        m = H2.match(p)
        secs.append({"id": m.group(1), "title_html": m.group(2), "title": re.sub("<[^>]+>", "", m.group(2)).strip(),
                     "body": p[m.end():]})
    return parts[0], secs


def h2(sec, extra=""):
    return f'<h2 id="{sec["id"]}">{extra}{sec["title_html"]}</h2>'


def crumbs(items):
    out = []
    for label, url in items:
        out.append(f'<a href="{url}">{esc(label)}</a>' if url else f'<span aria-current="page">{esc(label)}</span>')
    return f'<nav class="crumbs" aria-label="Brotkrumen">{icon("chev").join(out)}</nav>'


# ---------------------------------------------------------------- Bausteine
def vcard(s, v, compact=False):
    img = (f'<img src="../{v["img"]}" alt="" loading="lazy" decoding="async" width="480" height="300">'
           if v["img"] else "")
    badge = f'<span class="badge">{icon("alert")}zu prüfen</span>' if v["hard"] else ""
    search = " ".join([v["title"], v["brand"], v["segment"], v["plattform"], " ".join(v["variants"])])
    return (f'<a class="vcard{" compact" if compact else ""}" href="{s}.html" data-t="{esc(v["title"])}" data-b="{esc(v["brand"])}" '
            f'data-n="{v["nmax"]}" data-nmin="{v["nmin"]}" data-v="{v["n"]}" data-s="{esc(search)}">'
            f'<div class="vimg">{img}{badge}</div><div class="vbody"><span class="eyebrow">{esc(v["brand"])}</span>'
            f'<b class="vtitle">{esc(v["title"])}</b>'
            f'<span class="vnet"><strong>{rng(v["nmin"], v["nmax"])}</strong>&nbsp;kWh netto</span>'
            f'<span class="vmeta">{esc(v["segment"])}{" · " if v["segment"] else ""}{v["n"]} Variante{"n" if v["n"] != 1 else ""}</span>'
            f'</div></a>')


def kpi(ic, label, value, unit="", cls="", concept=None, hint=""):
    lab = f'<a href="{concept}.html" title="Was ist das?">{label}</a>' if concept else label
    hint_html = f'<span class="h">{hint}</span>' if hint else ""
    return (f'<div class="kpi {cls}"><span class="k">{icon(ic)}{lab}</span>'
            f'<span class="v">{value}{f"<small>{unit}</small>" if unit else ""}</span>{hint_html}</div>')


def terms_block(body):
    items = re.findall(r'<li><a href="([^"]+)">(.*?)</a>\s*—\s*(.*?)</li>', body, re.S)
    if not items:
        return body
    return '<div class="terms">' + "".join(
        f'<a class="term" href="{h}"><b>{t}</b><span>{re.sub("<[^>]+>", "", d)}</span></a>' for h, t, d in items) + "</div>"


def backlinks_html(slug, back, pages):
    refs = sorted(back.get(slug, []), key=lambda b: pages[b]["title"].lower())
    if not refs:
        return ""
    chips = "".join(f'<a class="lchip" href="{href(b)}">{esc(pages[b]["title"])}</a>' for b in refs)
    inner = (f'<div class="lchips">{chips}</div>' if len(refs) <= 14 else
             f'<details class="more"><summary>Alle {len(refs)} Seiten anzeigen</summary><div class="lchips">{chips}</div></details>')
    return f'<section class="backrefs" aria-labelledby="rueckverweise"><h2 id="rueckverweise">{icon("link")}Verlinkt von</h2>{inner}</section>'


def toc_html(items):
    if len(items) < 3:
        return ""
    lis = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in items)
    return f'<nav class="toc" aria-label="Auf dieser Seite"><p>Auf dieser Seite</p><ul>{lis}</ul></nav>'


# ---------------------------------------------------------------- Seitentypen
def vehicle_page(slug, page, pages, vinfo):
    v = vinfo[slug]
    pre, secs = split_sections(render(page, pages))
    cap = re.search(r"<p><em>(Bild:.*?)</em></p>", pre, re.S)
    brand_href = f'{v["bslug"]}.html' if v["bslug"] else "katalog.html"
    facts = "".join(f"<dt>{k}</dt><dd>{esc(str(val))}</dd>" for k, val in
                    [("Segment", v["segment"]), ("Karosserie", v["karosserie"]), ("Bauzeit", v["bauzeit"]),
                     ("Plattform", v["plattform"])] if val)
    flag = (f'<a class="flag" href="#offene-punkte">{icon("alert")}<span><b>{v["issues"]} offene Punkte</b> zur Datenlage '
            f'– vor Verwendung der Werte prüfen</span>{icon("chev")}</a>') if v["issues"] else ""
    head = f"""{crumbs([("Start", "index.html"), (v["brand"], brand_href), (v["title"], None)])}
<header class="hero-v">
  <figure class="hero-img">{f'<img src="../{v["img"]}" alt="{esc(v["title"])}" width="960" height="600" fetchpriority="high">' if v["img"] else ""}
    {f"<figcaption>{cap.group(1)}</figcaption>" if cap else ""}</figure>
  <div class="hero-body">
    <a class="eyebrow" href="{brand_href}">{esc(v["brand"])}</a>
    <h1>{esc(v["title"])}</h1>
    <p class="lead">{esc(v["kurz"])}</p>
    <div class="kpis">
      {kpi("battery", "Netto", rng(v["nmin"], v["nmax"]), "kWh", "primary", "nettokapazitaet", "nutzbar · Referenz für den SoH")}
      {kpi("db", "Brutto", rng(v["bmin"], v["bmax"]), "kWh", "", "bruttokapazitaet", "verbaut")}
      {kpi("percent", "Puffer", v["puffer"] or "–", "%" if v["puffer"] else "", "", "batteriepuffer", "Brutto − Netto")}
      {kpi("layers", "Varianten", str(v["n"]), "", "", None, "im Bestand")}
    </div>
    {f'<dl class="facts">{facts}</dl><p class="note">Segment bis Plattform: allgemeines Fachwissen, nicht aus der Rohquelle. Kapazitäten: Rohquelle.</p>' if facts else ""}
    {flag}
  </div>
</header>"""
    out, toc = [], []
    for sec in secs:
        t = sec["title"].lower()
        if t == "steckbrief":
            continue
        toc.append((sec["id"], sec["title"]))
        if t == "fachbegriffe":
            out.append(h2(sec) + terms_block(sec["body"]))
        elif t == "verwandte fahrzeuge":
            related, same = [], []
            for li in re.findall(r"<li>(.*?)</li>", sec["body"], re.S):
                targets = [x for x in re.findall(r'href="([^"]+)\.html"', li) if x in vinfo]
                (same if "Weitere Modelle" in li else related).extend(targets)
            block = h2(sec)
            if related:
                block += '<p class="sub">Gleiche Plattform oder Batterie</p><div class="grid compact">' + \
                         "".join(vcard(s, vinfo[s], True) for s in related) + "</div>"
            if same:
                block += f'<h3>Weitere Modelle von {esc(v["brand"])}</h3><div class="grid compact">' + \
                         "".join(vcard(s, vinfo[s], True) for s in same) + "</div>"
            out.append(block)
        elif t == "korrekturen":
            out.append(f'<section class="callout good">{h2(sec, icon("check"))}{sec["body"]}</section>')
        elif t == "offene punkte":
            out.append(f'<section class="callout warn">{h2(sec, icon("alert"))}{sec["body"]}'
                       f'<p class="callout-foot">Die Klärung läuft über GitHub: <a href="{REPO_ISSUES}" target="_blank" rel="noopener">'
                       f'Issues ansehen{icon("external")}</a></p></section>')
        elif t == "quellen":
            out.append(f'<div class="small">{h2(sec)}{sec["body"]}</div>')
        else:
            out.append(h2(sec) + sec["body"])
    return head, "\n".join(out), toc


def brand_page(slug, page, pages, vinfo, binfo):
    title = page["title"]
    pre, secs = split_sections(render(page, pages))
    kurz = re.search(r"<blockquote>\s*<p>(.*?)</p>\s*</blockquote>", pre, re.S)
    slugs = binfo.get(title, [])
    vs = [vinfo[s] for s in slugs]
    profil = next((s["body"] for s in secs if s["title"].lower() == "profil"), "")
    pm = re.search(r"Puffer im Mittel</td>\s*<td>([^<]+)</td>", profil)
    head = f"""{crumbs([("Start", "index.html"), ("Hersteller", "katalog.html#hersteller"), (title, None)])}
<header class="hero-b">
  <span class="eyebrow">Hersteller</span><h1>{esc(title)}</h1>
  {f'<p class="lead">{kurz.group(1)}</p>' if kurz else ""}
  <div class="kpis four">
    {kpi("car", "Modellreihen", str(len(vs)), "", "primary")}
    {kpi("layers", "Varianten", str(sum(v["n"] for v in vs)))}
    {kpi("battery", "Netto", rng(min(v["nmin"] for v in vs), max(v["nmax"] for v in vs)) if vs else "–", "kWh", "", "nettokapazitaet")}
    {kpi("percent", "Puffer Ø", pm.group(1).replace("&nbsp;", " ").replace("%", "").strip() if pm else "–", "%", "", "batteriepuffer")}
  </div>
</header>"""
    out, toc = [], []
    for sec in secs:
        t = sec["title"].lower()
        if t == "profil":
            continue
        toc.append((sec["id"], sec["title"]))
        if t == "fahrzeuge":
            out.append(h2(sec) + '<div class="grid">' + "".join(vcard(s, vinfo[s]) for s in slugs) + "</div>")
        elif t == "quellen":
            out.append(f'<div class="small">{h2(sec)}{sec["body"]}</div>')
        else:
            out.append(h2(sec) + sec["body"])
    return head, "\n".join(out), toc


def concept_page(slug, page, pages, vinfo):
    pre, secs = split_sections(render(page, pages))
    kd = re.search(r"<p><strong>Kurzdefinition:</strong>\s*(.*?)</p>", pre, re.S)
    head = f"""{crumbs([("Start", "index.html"), ("Fachbegriffe", "katalog.html#fachbegriffe"), (page["title"], None)])}
<header class="hero-c"><span class="eyebrow">Fachbegriff</span><h1>{esc(page["title"])}</h1>
{f'<p class="definition">{icon("book")}<span>{kd.group(1)}</span></p>' if kd else ""}</header>"""
    out, toc = [], []
    for sec in secs:
        t = sec["title"].lower()
        toc.append((sec["id"], sec["title"]))
        if t == "verwandte begriffe":
            out.append(h2(sec) + terms_block(sec["body"]))
        elif t.startswith("fahrzeuge im bestand"):
            targets = [x for x in re.findall(r'href="([^"]+)\.html"', sec["body"]) if x in vinfo]
            chips = "".join(f'<a class="vchip" href="{s}.html"><img src="../{vinfo[s]["img"]}" alt="" loading="lazy" '
                            f'width="44" height="28">{esc(vinfo[s]["title"])}</a>' for s in targets)
            out.append(h2(sec) + f'<div class="vchips">{chips}</div>')
        elif t == "belege":
            out.append(f'<div class="small">{h2(sec)}{sec["body"]}</div>')
        else:
            out.append(h2(sec) + sec["body"])
    return head, "\n".join(out), toc


def generic_page(slug, page, pages):
    pre, secs = split_sections(render(page, pages))
    pre = re.sub(r"<h1[^>]*>.*?</h1>", "", pre, count=1, flags=re.S)
    section = page["section"]
    head = f"""{crumbs([("Start", "index.html"), (section, None if section == "Wiki" else "katalog.html"), (page["title"], None)])
               if section != "Wiki" else crumbs([("Start", "index.html"), (page["title"], None)])}
<header class="hero-c"><span class="eyebrow">{esc(KIND[section])}</span><h1>{esc(page["title"])}</h1></header>"""
    toc = [(s["id"], s["title"]) for s in secs]
    body = pre + "\n".join(h2(s) + s["body"] for s in secs)
    return head, body, toc


def landing(pages, vinfo, binfo, brand_slug, n_issues, stand):
    vehicles = list(vinfo)
    n_var = sum(v["n"] for v in vinfo.values())
    n_terms = sum(1 for p in pages.values() if p["section"] == "Fachbegriffe")
    mosaic = [s for s in ("porsche-taycan", "vw-id-buzz", "hyundai-ioniq-5") if s in vinfo and vinfo[s]["img"]]
    brands = sorted(binfo, key=skey)
    chips = [f'<button type="button" class="chip" aria-pressed="true" data-brand="">Alle <span class="count">{len(vehicles)}</span></button>']
    chips += [f'<button type="button" class="chip" aria-pressed="false" data-brand="{esc(b)}">{esc(b)} '
              f'<span class="count">{len(binfo[b])}</span></button>' for b in brands]
    cards = "".join(vcard(s, vinfo[s]) for b in brands for s in binfo[b])
    return f"""
<section class="home-hero">
  <div>
    <p class="eyebrow">Knowledge Base · Stand {stand}</p>
    <h1>Jede Batterie. Jede Variante. <span class="hl">Belegt.</span></h1>
    <p class="lead">Brutto- und Nettokapazität von {n_var} Varianten aus {len(vehicles)} Modellreihen – mit Bild, Einordnung,
      Quelle und offen benannten Unsicherheiten.</p>
    <button type="button" class="bigsearch" data-open-search>{icon("search")}<span>Modell, Variante oder Fachbegriff suchen …</span><kbd>Strg K</kbd></button>
    <div class="hero-actions">
      <a class="btn btn-secondary" href="#fahrzeuge">{icon("car")}Alle Fahrzeuge</a>
      <button type="button" class="btn btn-secondary" data-ask>{BOLT}Ampere fragen</button>
    </div>
  </div>
  <div class="mosaic" aria-hidden="true">{"".join(f'<img src="../{vinfo[s]["img"]}" alt="" width="640" height="400">' for s in mosaic)}</div>
</section>
<section class="stats" aria-label="Kennzahlen">
  <div class="stat"><span class="ic">{icon("car")}</span><div><b>{len(vehicles)}</b><span>Modellreihen</span></div></div>
  <div class="stat"><span class="ic">{icon("layers")}</span><div><b>{n_var}</b><span>Varianten</span></div></div>
  <div class="stat"><span class="ic">{icon("factory")}</span><div><b>{len(brands)}</b><span>Hersteller</span></div></div>
  <div class="stat"><span class="ic">{icon("book")}</span><div><b>{n_terms}</b><span>Fachbegriffe</span></div></div>
</section>
<section aria-labelledby="einstieg">
  <h2 id="einstieg" class="sec-title">Einstieg</h2>
  <div class="entry">
    <a class="ecard" href="fahrzeuguebersicht.html"><span class="ic">{icon("table")}</span><span><b>Fahrzeugübersicht</b><span>Alle Modelle mit Segment, Plattform und Kapazität in einer Tabelle</span></span></a>
    <a class="ecard" href="puffer-analyse.html"><span class="ic">{icon("chart")}</span><span><b>Puffer-Analyse</b><span>Brutto gegen Netto: Verteilung, Extremwerte, Hersteller im Vergleich</span></span></a>
    <a class="ecard warn" href="datenqualitaet.html"><span class="ic">{icon("alert")}</span><span><b>Datenqualität</b><span>Fehler und Widersprüche in der Rohquelle{f" · {n_issues} offene Klärungen" if n_issues else ""}</span></span></a>
    <a class="ecard" href="katalog.html#fachbegriffe"><span class="ic">{icon("book")}</span><span><b>Fachbegriffe</b><span>Von Bruttokapazität bis State of Health – verständlich erklärt</span></span></a>
  </div>
</section>
<section id="fahrzeuge" class="explorer" aria-labelledby="fz-title">
  <div class="sec-head"><h2 id="fz-title" class="sec-title">Alle Fahrzeuge</h2><p class="cnt" id="fz-count" aria-live="polite">{len(vehicles)} Modelle</p></div>
  <div class="toolbar">
    <label class="field">{icon("search")}<span class="sr-only">Modelle filtern</span>
      <input type="search" id="fz-q" placeholder="Filtern, z. B. ID.3, Taycan 4S, MEB" autocomplete="off"></label>
    <label class="select"><span class="sr-only">Sortierung</span>
      <select id="fz-sort">
        <option value="brand">Nach Hersteller</option><option value="name">Name A–Z</option>
        <option value="netto-desc">Netto: größte zuerst</option><option value="netto-asc">Netto: kleinste zuerst</option>
        <option value="var">Meiste Varianten</option>
      </select></label>
  </div>
  <div class="chips" role="group" aria-label="Nach Hersteller filtern">{"".join(chips)}</div>
  <div class="grid" id="grid">{cards}</div>
  <div class="empty" id="fz-empty" hidden>
    {icon("search")}<p><b>Kein Modell passt zu diesem Filter.</b><br>Prüfe die Schreibweise oder setze den Filter zurück.</p>
    <div class="empty-actions"><button type="button" class="btn btn-secondary" data-reset>Filter zurücksetzen</button>
    <button type="button" class="btn btn-primary" data-ask-filter>{BOLT}Ampere fragen</button></div>
  </div>
</section>"""


# ---------------------------------------------------------------- Rahmen
def sidebar(pages, current, vinfo, binfo, brand_slug):
    def item(s, label=None):
        cur = ' aria-current="page"' if s == current else ""
        return f'<li><a href="{href(s)}"{cur}>{esc(label or pages[s]["title"])}</a></li>'

    def group(name, ic, inner, count, open_):
        return (f'<details class="ng"{" open" if open_ else ""}><summary>{icon("chev", "chev")}{icon(ic)}<span>{name}</span>'
                f'<span class="count">{count}</span></summary>{inner}</details>')

    by_sec = defaultdict(list)
    for s, p in pages.items():
        by_sec[p["section"]].append(s)
    cur_sec = pages[current]["section"] if current in pages else None
    home_cur = ' aria-current="page"' if current == "__home__" else ""
    out = [f'<div class="sb-head"><span>Navigation</span><button type="button" class="iconbtn" data-close-nav aria-label="Navigation schließen">{icon("x")}</button></div>',
           f'<ul class="nav top"><li><a href="index.html"{home_cur}>{icon("home")}Start</a></li></ul>']
    syn = sorted(by_sec["Übersichten"], key=lambda s: skey(pages[s]["title"]))
    out.append(group("Übersichten", "chart", f'<ul class="nav">{"".join(item(s) for s in syn)}</ul>', len(syn), True))
    brands = []
    for b in sorted(binfo, key=skey):
        inner = "".join(item(s) for s in sorted(binfo[b], key=lambda s: skey(pages[s]["title"])))
        brands.append(f'<details class="nb"{" open" if current in binfo[b] else ""}><summary>{icon("chev", "chev")}'
                      f'<span>{esc(b)}</span><span class="count">{len(binfo[b])}</span></summary><ul class="nav">{inner}</ul></details>')
    out.append(group("Fahrzeuge", "car", "".join(brands), len(vinfo), True))
    hs = sorted(by_sec["Hersteller"], key=lambda s: skey(pages[s]["title"]))
    out.append(group("Hersteller", "factory", f'<ul class="nav">{"".join(item(s) for s in hs)}</ul>', len(hs), cur_sec == "Hersteller"))
    cs = sorted(by_sec["Fachbegriffe"], key=lambda s: skey(pages[s]["title"]))
    out.append(group("Fachbegriffe", "book", f'<ul class="nav">{"".join(item(s) for s in cs)}</ul>', len(cs), cur_sec == "Fachbegriffe"))
    wiki = by_sec["Quellen"] + [s for s in ("index", "corporate-identity", "log") if s in pages]
    out.append(group("Quellen &amp; Wiki", "db", f'<ul class="nav">{"".join(item(s) for s in wiki)}</ul>', len(wiki),
                     cur_sec in ("Quellen", "Wiki")))
    return "\n".join(out)


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap">')


ASSET_VER = {}


def ver(name):
    """Kurzer Inhalts-Hash als ?v=… – ändert sich nur, wenn sich die Datei ändert."""
    return ASSET_VER.get(name, "")


def shell(title, desc, content, navhtml, toc="", stand=""):
    footer = (f'<footer class="foot"><span>Fahrzeug<b>Wiki</b> · Stand {stand}</span>'
              f'<a href="tn-batterycheck-alle-daten.html">Rohquelle</a><a href="datenqualitaet.html">Datenqualität</a>'
              f'<a href="corporate-identity.html">Corporate Identity</a>'
              f'<a href="{REPO_ISSUES}" target="_blank" rel="noopener">GitHub-Issues{icon("external")}</a>'
              f'<span>Fotos: Wikimedia Commons (CC)</span></footer>')
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)} · Fahrzeug-Wiki</title><meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0A6B4E">
<script>try{{var t=localStorage.getItem("fw-theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="icon" href="../ci/signet.svg" type="image/svg+xml">
{FONTS}<link rel="stylesheet" href="../ci/tokens.css?v={ver('tokens')}"><link rel="stylesheet" href="app.css?v={ver('app.css')}"></head>
<body>
<a class="skip" href="#main">Zum Inhalt springen</a>
<header class="topbar">
  <button type="button" class="iconbtn menubtn" aria-label="Navigation öffnen" aria-expanded="false" aria-controls="sidebar">{icon("menu")}</button>
  <a class="brand" href="index.html" aria-label="Fahrzeug-Wiki – Startseite"><img src="../ci/signet.svg" alt="" width="32" height="32"><span class="word">Fahrzeug<b>Wiki</b></span></a>
  <button type="button" class="searchbtn" data-open-search aria-label="Suchen (Strg+K)">{icon("search")}<span>Fahrzeug, Variante oder Begriff suchen …</span><kbd>Strg K</kbd></button>
  <div class="tb-actions">
    <button type="button" class="iconbtn theme" aria-label="Farbschema wechseln">{icon("moon", "moon")}{icon("sun", "sun")}</button>
    <button type="button" class="btn btn-primary askbtn" data-ask>{BOLT}<span class="label">Ampere fragen</span></button>
  </div>
</header>
<div class="shell">
  <nav id="sidebar" class="sidebar" aria-label="Wiki-Navigation">{navhtml}</nav>
  <div class="scrim" data-close-nav></div>
  <main id="main" tabindex="-1"><div class="page{" with-toc" if toc else ""}"><article class="content">{content}{footer}</article>{toc}</div></main>
</div>
<dialog class="palette" aria-label="Suche">
  <div class="pal-head">{icon("search")}
    <input type="text" role="combobox" aria-expanded="true" aria-controls="pal-list" aria-autocomplete="list" placeholder="Fahrzeug, Variante, Marke oder Begriff …" autocomplete="off" spellcheck="false">
    <button type="button" class="iconbtn pal-close" aria-label="Suche schließen">{icon("x")}</button></div>
  <ul class="pal-list" id="pal-list" role="listbox" aria-label="Suchergebnisse"></ul>
  <div class="pal-foot"><span><kbd>↑</kbd><kbd>↓</kbd> auswählen</span><span><kbd>Enter</kbd> öffnen</span><span><kbd>Esc</kbd> schließen</span></div>
</dialog>
<script src="search.js?v={ver('search.js')}" defer></script><script src="app.js?v={ver('app.js')}" defer></script>
<script src="../chat/widget/fw-chat.js?v={ver('chat')}" defer></script>
</body></html>"""


# ---------------------------------------------------------------- Suche
def search_index(pages, vinfo):
    out = []
    for s, p in pages.items():
        k = KIND[p["section"]]
        e = {"t": p["title"], "k": k, "u": href(s)}
        if s in vinfo:
            v = vinfo[s]
            e.update(b=v["brand"], d=f'{v["segment"]} · netto {rng(v["nmin"], v["nmax"])} kWh · {v["n"]} Varianten',
                     x=" ".join([v["plattform"], v["karosserie"], " ".join(v["variants"])]), i=f'../{v["img"]}')
        elif k == "Fachbegriff":
            m = re.search(r"\*\*Kurzdefinition:\*\*\s*(.+)", p["body"])
            e["d"] = plain(m.group(1)) if m else ""
        elif k == "Hersteller":
            m = re.search(r"^> (.+)$", p["body"], re.M)
            e["d"] = plain(m.group(1)) if m else ""
        else:
            m = re.search(r"\*\*Anlass:\*\*\s*(.+)", p["body"])
            e["d"] = plain(m.group(1)) if m else {"index": "Alle Seiten des Wikis im Überblick", "log": "Änderungsprotokoll",
                                                  "corporate-identity": "Logo, Farben, Schrift und Tonalität"}.get(s, "Rohquelle")
        out.append(e)
    return out


# ---------------------------------------------------------------- Hauptprogramm
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


def main():
    pages = load_pages()
    vinfo, binfo, brand_slug = build_info(pages)
    back = backlinks(pages)
    dates = [p["meta"].get("updated") for p in pages.values() if p["meta"].get("updated")]
    stand = ".".join(reversed(max(dates).split("-"))) if dates else ""
    corr_file = ROOT / "tools" / "corrections.json"   # offene Klärungen = Issues, die nicht als erledigt vermerkt sind
    n_issues = sum(1 for e in json.loads(corr_file.read_text(encoding="utf-8")).get("offene_issues", [])
                   if "kann geschlossen werden" not in e["stand"]) if corr_file.exists() else 0

    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    for f in ("app.css", "app.js"):
        shutil.copyfile(ASSETS / f, OUT / f)
    (OUT / "search.js").write_text("window.FW_SEARCH=" + json.dumps(search_index(pages, vinfo), ensure_ascii=False) + ";",
                                   encoding="utf-8")
    for name, path in [("app.css", OUT / "app.css"), ("app.js", OUT / "app.js"), ("search.js", OUT / "search.js"),
                       ("tokens", ROOT / "ci" / "tokens.css"), ("chat", ROOT / "chat" / "widget" / "fw-chat.js")]:
        ASSET_VER[name] = hashlib.sha1(path.read_bytes()).hexdigest()[:8] if path.exists() else ""

    for slug, p in pages.items():
        sec = p["section"]
        if sec == "Fahrzeuge":
            head, body, toc = vehicle_page(slug, p, pages, vinfo)
            desc = vinfo[slug]["kurz"]
        elif sec == "Hersteller":
            head, body, toc = brand_page(slug, p, pages, vinfo, binfo)
            desc = f"{p['title']}: Elektrofahrzeuge und Batteriekapazitäten"
        elif sec == "Fachbegriffe":
            head, body, toc = concept_page(slug, p, pages, vinfo)
            desc = f"Fachbegriff: {p['title']}"
        else:
            head, body, toc = generic_page(slug, p, pages)
            desc = p["title"]
        content = head + f'<div class="prose">{body}</div>' + backlinks_html(slug, back, pages)
        (OUT / href(slug)).write_text(
            shell(p["title"], desc, content, sidebar(pages, slug, vinfo, binfo, brand_slug), toc_html(toc), stand),
            encoding="utf-8")
    (OUT / "index.html").write_text(
        shell("Start", "Batterie-Referenzdaten für Elektrofahrzeuge", landing(pages, vinfo, binfo, brand_slug, n_issues, stand),
              sidebar(pages, "__home__", vinfo, binfo, brand_slug), "", stand), encoding="utf-8")
    (ROOT / "index.html").write_text('<!doctype html><meta http-equiv="refresh" content="0; url=site/index.html">'
                                     '<a href="site/index.html">Fahrzeug-Wiki öffnen</a>', encoding="utf-8")
    print(f"{len(pages) + 1} HTML-Seiten in {OUT}")


if __name__ == "__main__":
    main()
