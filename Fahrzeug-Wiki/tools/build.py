"""Baut das Wiki aus Rohdaten + LLM-gepflegten Metadaten.

Eingaben:
  tools/families.json        (aus raw/ via families.py)
  tools/images.json          (via images.py)
  tools/meta/*.json          (Fahrzeug- und Herstellertexte)
  tools/concepts_src.py      (Fachbegriffe)
Ausgabe: wiki/**, index.md
"""
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from concepts_src import C as CONCEPTS, KATEGORIEN  # noqa: E402

TODAY = "2026-09-23"
SRC = "tn-batterycheck-alle-daten"
WIKI = ROOT / "wiki"

BRAND_SLUG = {b: b.lower() for b in ["Audi", "BMW", "Citroen", "Cupra", "Dacia", "Ford", "Hyundai", "Kia",
                                     "Mercedes", "MG", "Mini", "Peugeot", "Porsche", "Renault", "Seat", "Skoda",
                                     "Tesla", "Volkswagen", "Volvo"]}

# Bildhinweise, wo das Foto nicht exakt die Elektroversion zeigt
IMG_NOTE = {
    "hyundai-ioniq-electric": "Abgebildet ist die Hybridversion; Karosserie identisch mit dem IONIQ Elektro.",
    "renault-city-k-ze": "Abgebildet ist der baugleiche Dacia Spring (Europa-Version des City K-ZE).",
    "bmw-i5": "Abgebildet ist die Messe-Präsentation 2023.",
    "hyundai-ioniq-6": "Abgebildet ist die Sportversion IONIQ 6 N (nicht im Bestand).",
    "mini-cooper-electric": "Abgebildet ist der Cooper SE der Generation F56 (bis 2023).",
    "kia-niro-ev": "Abgebildet ist die zweite Generation (Niro EV, SG2).",
}


# ---------------------------------------------------------------- Hilfen
def num(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def pct(v):
    return f"{v:.1f}".replace(".", ",")


def raw_kwh(s):
    return str(s).replace(".", ",")


def span(vals):
    lo, hi = min(vals), max(vals)
    return f"{num(lo)} kWh" if lo == hi else f"{num(lo)}–{num(hi)} kWh"


TABLE_LINK = re.compile(r"\[\[([^\]|]+)\|([^\]]+)\]\]")


def escape_table_links(text):
    """In Tabellenzeilen muss das | im Wikilink escaped sein, sonst bricht Obsidian die Spalte."""
    return "\n".join(TABLE_LINK.sub(r"[[\1\|\2]]", ln) if ln.startswith("|") else ln
                     for ln in text.split("\n"))


def write(path: Path, text: str):
    text = escape_table_links(text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def fm(**kw):
    lines = ["---"]
    for k, v in kw.items():
        if isinstance(v, list):
            lines.append(f"{k}: [{', '.join(json.dumps(x, ensure_ascii=False) for x in v)}]")
        elif v is None:
            continue
        else:
            lines.append(f"{k}: {json.dumps(v, ensure_ascii=False) if isinstance(v, str) else v}")
    lines.append("---\n")
    return "\n".join(lines)


def tagify(s):
    return re.sub(r"[^a-z0-9äöüß-]+", "-", s.lower()).strip("-")


# ---------------------------------------------------------------- Daten laden
fams = json.loads((ROOT / "tools" / "families.json").read_text(encoding="utf-8"))
images = json.loads((ROOT / "tools" / "images.json").read_text(encoding="utf-8"))
BILDER = ROOT / "Bilder"
for _slug, _im in images.items():
    if _im.get("thumb"):
        _im["thumb"] = _im["thumb"].split("?")[0]  # Tracking-Parameter entfernen
    # lokale Kopie aus tools/download_images.py (Bilder/<slug>.jpg)
    _local = next(BILDER.glob(f"{_slug}.*"), None) if BILDER.exists() else None
    if _local:
        _im["local"] = _local.name
meta, brands = {}, {}
for f in sorted((ROOT / "tools" / "meta").glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    meta.update(d["fahrzeuge"])
    brands.update(d["hersteller"])
missing = set(fams) - set(meta)
if missing:
    raise SystemExit(f"Metadaten fehlen für: {sorted(missing)}")

for slug, f in fams.items():
    for r in f["rows"]:
        r["puffer"] = r["brutto"] - r["netto"]
        r["puffer_pct"] = r["puffer"] / r["brutto"] * 100

all_rows = [(slug, r) for slug, f in fams.items() for r in f["rows"]]

# ---------------------------------------------------------------- Auto-Befunde Datenqualität
auto_issues = defaultdict(list)
for slug, f in fams.items():
    seen = Counter((r["modell"], r["brutto"], r["netto"]) for r in f["rows"])
    for (m, b, n), c in seen.items():
        if c > 1:
            zeilen = [str(r["zeile"]) for r in f["rows"] if (r["modell"], r["brutto"], r["netto"]) == (m, b, n)]
            auto_issues[slug].append(f"**Duplikat:** „{m}“ {num(b)}/{num(n)} kWh steht {c}× in der Quelle (Zeilen {', '.join(zeilen)}).")
    for r in f["rows"]:
        if r["netto"] > r["brutto"]:
            auto_issues[slug].append(f"**Netto > Brutto:** „{r['modell']}“ {raw_kwh(r['brutto_raw'])} brutto / {raw_kwh(r['netto_raw'])} netto (Zeile {r['zeile']}) – physikalisch unmöglich, vermutlich vertauschte oder falsche Werte.")
        if r["ca"]:
            auto_issues[slug].append(f"**Näherungswert:** „{r['modell']}“ ist in der Quelle als „{r['brutto_raw']}“ angegeben (Zeile {r['zeile']}).")

# ---------------------------------------------------------------- Konzept-Rückverweise
concept_users = defaultdict(set)
link_re = re.compile(r"\[\[([^\]|#]+)")
for slug, m in meta.items():
    for c in m.get("konzepte", []):
        concept_users[c].add(slug)
    for c in link_re.findall(m.get("beschreibung", "") + m.get("varianten", "")):
        if c in CONCEPTS:
            concept_users[c].add(slug)

# ---------------------------------------------------------------- Bildblock
def image_block(slug, name, width=None):
    im = images.get(slug) or {}
    if not im.get("local"):
        return ""
    alt = name.replace("[", "").replace("]", "")
    note = f" {IMG_NOTE[slug]}" if slug in IMG_NOTE else ""
    artist = im.get("artist") or "unbekannt"
    # relativer Pfad von wiki/entities/fahrzeuge/ nach Bilder/ – funktioniert in Obsidian, VS Code und GitHub
    return (f"![{alt}](../../../Bilder/{im['local']})\n"
            f"*Bild: [{im['file'][5:]}]({im['page']}) · Urheber: {artist} · Lizenz: {im.get('license', '?')} · "
            f"via Wikimedia Commons.{note}*\n")


# ---------------------------------------------------------------- Fahrzeugseiten
def vehicle_page(slug):
    f, m = fams[slug], meta[slug]
    rows = f["rows"]
    brand = f["brand"]
    bslug = BRAND_SLUG[brand]
    bname = brands.get(brand, {}).get("name", brand)
    br = [r["brutto"] for r in rows]
    ne = [r["netto"] for r in rows]
    pp = [r["puffer_pct"] for r in rows if r["puffer_pct"] >= 0]
    zeilen = f"{min(r['zeile'] for r in rows)}–{max(r['zeile'] for r in rows)}" if len(rows) > 1 else str(rows[0]["zeile"])

    out = [fm(type="entity", kategorie="fahrzeug", hersteller=bname, segment=m.get("segment"),
              karosserie=m.get("karosserie"), bauzeit=m.get("bauzeit"), plattform=m.get("plattform"),
              varianten=len(rows), brutto_min=min(br), brutto_max=max(br), netto_min=min(ne), netto_max=max(ne),
              bild=f"Bilder/{images[slug]['local']}" if (images.get(slug) or {}).get("local") else None, updated=TODAY, sources=1,
              tags=["fahrzeug", tagify(brand)] + ([tagify(m["segment"])] if m.get("segment") else []))]
    out.append(f"# {f['name']}\n")
    out.append(image_block(slug, f["name"]))
    out.append(f"> {m['kurz']}\n")

    out.append("## Steckbrief\n")
    out.append("| Feld | Wert | Beleg |\n|---|---|---|")
    out.append(f"| Hersteller | [[{bslug}|{bname}]] | [[{SRC}]] |")
    for label, key in [("Segment", "segment"), ("Karosserie", "karosserie"), ("Bauzeit", "bauzeit"), ("Plattform", "plattform")]:
        if m.get(key):
            out.append(f"| {label} | {m[key]} | Fachwissen¹ |")
    out.append(f"| Varianten im Bestand | {len(rows)} | [[{SRC}]] |")
    out.append(f"| [[bruttokapazitaet|Bruttokapazität]] | {span(br)} | [[{SRC}]] |")
    out.append(f"| [[nettokapazitaet|Nettokapazität]] | {span(ne)} | [[{SRC}]] |")
    if pp:
        out.append(f"| [[batteriepuffer|Puffer]] | {pct(min(pp))}–{pct(max(pp))} % | berechnet |" if min(pp) != max(pp)
                   else f"| [[batteriepuffer|Puffer]] | {pct(pp[0])} % | berechnet |")
    out.append("")

    out.append("## Beschreibung\n")
    out.append(m["beschreibung"].strip() + "\n")

    out.append("## Varianten und Batterien\n")
    if m.get("varianten"):
        out.append(m["varianten"].strip() + "\n")
    out.append("| Variante | Brutto | Netto | Puffer | Zeile |\n|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: (r["modell"].lower(), r["brutto"], r["netto"])):
        puffer = f"{num(r['puffer'])} kWh ({pct(r['puffer_pct'])} %)" if r["puffer"] >= 0 else "⚠️ negativ"
        out.append(f"| {r['modell']} | {raw_kwh(r['brutto_raw'])} | {raw_kwh(r['netto_raw'])} | {puffer} | {r['zeile']} |")
    out.append(f"\nQuelle: [[{SRC}]], Blatt „Fahrzeuge“, Zeilen {zeilen}. Puffer = Brutto − Netto (berechnet).\n")

    konz = [c for c in m.get("konzepte", []) if c in CONCEPTS]
    if konz:
        out.append("## Fachbegriffe\n")
        for c in konz:
            out.append(f"- [[{c}|{CONCEPTS[c][0]}]] — {CONCEPTS[c][1]}")
        out.append("")

    rel = [g for g in m.get("geschwister", []) if g in fams and g != slug]
    same_brand = [s for s in fams if fams[s]["brand"] == brand and s != slug and s not in rel]
    if rel or same_brand:
        out.append("## Verwandte Fahrzeuge\n")
        for g in rel:
            out.append(f"- [[{g}|{fams[g]['name']}]] — technisch verwandt / gleiche Plattform oder Batterie")
        if same_brand:
            out.append(f"- Weitere Modelle von {bname}: " + ", ".join(f"[[{s}|{fams[s]['name']}]]" for s in same_brand))
        out.append("")

    issues = auto_issues.get(slug, []) + [h for h in m.get("hinweise", []) if h]
    if issues:
        out.append("## Offene Punkte\n")
        out.extend(f"- {h}" for h in issues)
        out.append("\nSiehe auch [[datenqualitaet]].\n")

    out.append("## Quellen\n")
    out.append(f"- [[{SRC}]] — Brutto-/Nettokapazität aller Varianten (Zeilen {zeilen})")
    wp = (images.get(slug) or {}).get("wikipedia")
    if wp:
        out.append(f"- Weiterlesen: [Wikipedia – {wp}](https://en.wikipedia.org/wiki/{wp.replace(' ', '_')})")
    out.append("\n¹ *Beschreibung und Steckbrief-Felder ohne Quellseite beruhen auf allgemeinem Fachwissen des LLM "
               f"(Stand {TODAY}) und sind nicht durch eine Rohquelle im Bestand belegt. Zahlenwerte zur Batterie stammen "
               "ausschließlich aus der Rohquelle.*")
    return "\n".join(out)


# ---------------------------------------------------------------- Herstellerseiten
def brand_page(brand):
    b = brands.get(brand, {"name": brand, "kurz": "", "beschreibung": ""})
    slugs = [s for s in fams if fams[s]["brand"] == brand]
    rows = [r for s in slugs for r in fams[s]["rows"]]
    out = [fm(type="entity", kategorie="hersteller", modelle=len(slugs), varianten=len(rows), updated=TODAY,
              sources=1, tags=["hersteller", tagify(brand)])]
    out.append(f"# {b['name']}\n")
    if b.get("kurz"):
        out.append(f"> {b['kurz']}\n")
    out.append("## Profil\n")
    out.append("| Feld | Wert | Beleg |\n|---|---|---|")
    out.append(f"| Modellreihen im Bestand | {len(slugs)} | [[{SRC}]] |")
    out.append(f"| Varianten im Bestand | {len(rows)} | [[{SRC}]] |")
    out.append(f"| Bruttokapazität | {span([r['brutto'] for r in rows])} | [[{SRC}]] |")
    out.append(f"| Nettokapazität | {span([r['netto'] for r in rows])} | [[{SRC}]] |")
    pp = [r["puffer_pct"] for r in rows if r["puffer_pct"] >= 0]
    out.append(f"| Puffer im Mittel | {pct(statistics.mean(pp))} % | berechnet |\n")
    if b.get("beschreibung"):
        out.append("## Über den Hersteller\n")
        out.append(b["beschreibung"].strip() + "\n")
    out.append("## Fahrzeuge\n")
    out.append("| Bild | Modell | Varianten | Brutto | Netto |\n|---|---|---|---|---|")
    for s in slugs:
        im = images.get(s) or {}
        pic = f"![[{im['local']}|160]]" if im.get("local") else ""
        fr = fams[s]["rows"]
        out.append(f"| {pic} | [[{s}|{fams[s]['name']}]] | {len(fr)} | {span([r['brutto'] for r in fr])} | {span([r['netto'] for r in fr])} |")
    out.append(f"\nBilder: lokal in `Bilder/`, Quelle Wikimedia Commons – Urheber und Lizenz auf der jeweiligen Fahrzeugseite.\n")
    out.append("## Quellen\n")
    out.append(f"- [[{SRC}]] — Fahrzeugliste und Kapazitäten")
    out.append("- Herstellerbeschreibung: allgemeines Fachwissen des LLM, nicht durch Rohquelle belegt.")
    return "\n".join(out)


# ---------------------------------------------------------------- Konzeptseiten
def concept_page(slug):
    title, kurz, body, verwandt, tags = CONCEPTS[slug]
    out = [fm(type="concept", updated=TODAY, sources=1 if SRC in body else 0, tags=["fachbegriff"] + tags)]
    out.append(f"# {title}\n")
    out.append(f"**Kurzdefinition:** {kurz}\n")
    out.append("## Erläuterung\n")
    out.append(body.strip() + "\n")
    rel = [v for v in verwandt if v in CONCEPTS]
    if rel:
        out.append("## Verwandte Begriffe\n")
        out.extend(f"- [[{v}|{CONCEPTS[v][0]}]] — {CONCEPTS[v][1]}" for v in rel)
        out.append("")
    users = sorted(concept_users.get(slug, []), key=lambda s: fams[s]["name"])
    if users:
        out.append(f"## Fahrzeuge im Bestand ({len(users)})\n")
        out.append(", ".join(f"[[{s}|{fams[s]['name']}]]" for s in users) + "\n")
    out.append("## Belege\n")
    if SRC in body:
        out.append(f"- [[{SRC}]] — Zahlenbeispiele in diesem Artikel")
    out.append("- Begriffserklärung: allgemeines Fachwissen des LLM (Stand " + TODAY + "), keine Rohquelle im Bestand.")
    return "\n".join(out)


# ---------------------------------------------------------------- Synthese: Übersicht
def overview_page():
    out = [fm(type="synthesis", updated=TODAY, tags=["uebersicht"])]
    out.append("# Fahrzeugübersicht\n")
    out.append(f"**Anlass:** laufende Übersicht über alle Modellreihen im Bestand · Stand {TODAY}\n")
    out.append(f"{len(fams)} Modellreihen, {len(all_rows)} Varianten, {len(BRAND_SLUG)} Hersteller – Quelle: [[{SRC}]].\n")
    for brand in BRAND_SLUG:
        slugs = [s for s in fams if fams[s]["brand"] == brand]
        bname = brands.get(brand, {}).get("name", brand)
        out.append(f"## [[{BRAND_SLUG[brand]}|{bname}]]\n")
        out.append("| Modell | Segment | Plattform | Varianten | Brutto | Netto |\n|---|---|---|---|---|---|")
        for s in slugs:
            m, fr = meta[s], fams[s]["rows"]
            out.append(f"| [[{s}|{fams[s]['name']}]] | {m.get('segment') or ''} | {m.get('plattform') or ''} | {len(fr)} | "
                       f"{span([r['brutto'] for r in fr])} | {span([r['netto'] for r in fr])} |")
        out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- Synthese: Puffer-Analyse
def buffer_page():
    valid = [(s, r) for s, r in all_rows if r["puffer"] >= 0]
    pcts = [r["puffer_pct"] for _, r in valid]
    out = [fm(type="synthesis", updated=TODAY, tags=["analyse", "batteriepuffer"])]
    out.append("# Puffer-Analyse: Brutto vs. Netto\n")
    out.append(f"**Anlass:** Auswertung aller {len(valid)} plausiblen Varianten aus [[{SRC}]] · Stand {TODAY}\n")
    out.append("## Stand\n")
    out.append(f"Der [[batteriepuffer]] (Brutto − Netto, relativ zur [[bruttokapazitaet]]) liegt im Bestand im **Median bei "
               f"{pct(statistics.median(pcts))} %**, im Mittel bei {pct(statistics.mean(pcts))} %. Die Spanne reicht von "
               f"{pct(min(pcts))} % bis {pct(max(pcts))} %. Eine Variante mit negativem Puffer (netto > brutto) ist ausgeschlossen "
               "und in [[datenqualitaet]] dokumentiert.\n")
    out.append("Muster, die sich zeigen:\n")
    out.append("- **Sehr kleine Puffer (< 2 %)** treten vor allem bei [[lfp-zellchemie|LFP]]-Batterien und bei Herstellern auf, die "
               "offenbar den nutzbaren Wert nahe am Brutto angeben (z. B. [[citroen-e-c3]], [[mg4-electric]] 51 kWh). "
               "Solche Werte sollten vor einem [[batteriecheck]] besonders geprüft werden.")
    out.append("- **Große Puffer (> 12 %)** finden sich bei frühen Konstruktionen ([[bmw-i3]] mit 33,2 kWh, [[vw-e-golf]]), bei den 41-kWh-Transportern von Mercedes ([[mercedes-evito]], [[mercedes-esprinter]]), bei "
               "[[software-lock|softwarebegrenzten]] Batterien (Tesla Model S/X 60) und bei der ersten MEB-Einstiegsbatterie "
               "(VW ID.3 Pure 55 → 45 kWh laut Quelle – Bruttowert fraglich, siehe [[datenqualitaet]]).")
    out.append("- **Plattform-Geschwister** haben identische Puffer – siehe [[plattform-geschwister]].\n")

    out.append("## Verteilung\n")
    buckets = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12), (12, 15), (15, 100)]
    out.append("| Puffer | Varianten | |\n|---|---|---|")
    for lo, hi in buckets:
        n = sum(lo <= p < hi for p in pcts)
        label = f"≥ {lo} %" if hi == 100 else f"{lo}–{hi} %"
        out.append(f"| {label} | {n} | {'█' * max(1, round(n / 4)) if n else ''} |")
    out.append("")

    out.append("## Nach Hersteller\n")
    out.append("| Hersteller | Varianten | Puffer Median | Min | Max |\n|---|---|---|---|---|")
    by_brand = defaultdict(list)
    for s, r in valid:
        by_brand[fams[s]["brand"]].append(r["puffer_pct"])
    for brand, ps in sorted(by_brand.items(), key=lambda x: statistics.median(x[1])):
        bname = brands.get(brand, {}).get("name", brand)
        out.append(f"| [[{BRAND_SLUG[brand]}|{bname}]] | {len(ps)} | {pct(statistics.median(ps))} % | {pct(min(ps))} % | {pct(max(ps))} % |")
    out.append("")

    def table(items, title):
        out.append(f"## {title}\n")
        out.append("| Fahrzeug | Variante | Brutto | Netto | Puffer |\n|---|---|---|---|---|")
        seen = set()
        for s, r in items:
            key = (r["modell"], r["brutto"], r["netto"])
            if key in seen:
                continue
            seen.add(key)
            out.append(f"| [[{s}|{fams[s]['name']}]] | {r['modell']} | {raw_kwh(r['brutto_raw'])} | {raw_kwh(r['netto_raw'])} | {pct(r['puffer_pct'])} % |")
            if len(seen) == 12:
                break
        out.append("")

    table(sorted(valid, key=lambda x: -x[1]["puffer_pct"]), "Größte Puffer")
    table(sorted(valid, key=lambda x: x[1]["puffer_pct"]), "Kleinste Puffer")
    out.append("## Belastbarkeit\n")
    out.append(f"- **Gut belegt:** Die Werte selbst stammen aus einer Quelle ([[{SRC}]]), die intern abgeglichen ist (Blatt „Übersicht“: alle Marken „OK“).")
    out.append("- **Dünn:** Es gibt nur diese eine Quelle. Herstellerangaben und unabhängige Messungen fehlen als Gegenprobe.")
    out.append("- **Strittig:** Sehr kleine Puffer (< 1 %) und die in [[datenqualitaet]] gelisteten Zeilen.\n")
    out.append("## Was fehlt\n")
    out.append("- Herstellerdatenblätter oder eine zweite Datenbank (z. B. EV-Database) als Abgleich")
    out.append("- Modelljahr/Batterie-Generation je Zeile – ohne sie sind gleichnamige Varianten mit verschiedenen Werten nicht eindeutig zuzuordnen")
    return "\n".join(out)


# ---------------------------------------------------------------- Synthese: Datenqualität
def quality_page():
    out = [fm(type="synthesis", updated=TODAY, tags=["datenqualitaet", "lint"])]
    out.append("# Datenqualität der Rohquelle\n")
    out.append(f"**Anlass:** Befunde beim Ingest von [[{SRC}]] am {TODAY}\n")
    out.append("## Stand\n")
    n_auto = sum(len(v) for v in auto_issues.values())
    n_hint = sum(len([h for h in m.get('hinweise', []) if h]) for m in meta.values())
    out.append(f"Die Quelle ist formal vollständig: Das Blatt „Übersicht“ bestätigt für alle 19 Marken, dass die extrahierten Zeilen der Quellangabe entsprechen (469/469). "
               f"Inhaltlich gibt es aber **{n_auto} automatisch erkannte Auffälligkeiten** (Duplikate, unmögliche Werte, Näherungswerte) "
               f"und **{n_hint} fachliche Hinweise** aus der Einordnung der einzelnen Fahrzeuge.\n")
    out.append("## Automatisch erkannte Befunde\n")
    for s in fams:
        for h in auto_issues.get(s, []):
            out.append(f"- [[{s}|{fams[s]['name']}]]: {h}")
    out.append("")
    out.append("## Uneinheitliche Schreibweisen\n")
    out.append("- Hersteller „Citroen“ ohne Trema (offiziell Citroën), Modelle „e-C4“ statt „ë-C4“; „E-Berlingo Multispace“ mit großem E neben „e-Berlingo“.")
    out.append("- „Mercedes“ statt „Mercedes-Benz“; „Skoda“ statt „Škoda“.")
    out.append("- Leerzeichen uneinheitlich: BMW „iX xDrive 40“ vs. „iX1 xDrive30“.")
    out.append("- Werte teils mit, teils ohne Nachkommastelle („71 kWh“ vs. „71.0 kWh“); Dezimalpunkt statt Komma.\n")
    out.append("## Fachliche Hinweise je Fahrzeug\n")
    for s in fams:
        hs = [h for h in meta[s].get("hinweise", []) if h]
        if hs:
            out.append(f"### [[{s}|{fams[s]['name']}]]\n")
            out.extend(f"- {h}" for h in hs)
            out.append("")
    out.append("## Empfehlungen\n")
    out.append("1. Cupra Born Zeile 99 (53/60 kWh) korrigieren – Brutto und Netto sind so unmöglich; gegen Herstellerangabe prüfen.")
    out.append("2. Exakte Duplikate entfernen (Porsche Taycan Sport Turismo 93,4/83,7).")
    out.append("3. Spalte **Modelljahr / Batterie-Generation** ergänzen – viele gleichnamige Varianten haben mehrere Werte.")
    out.append("4. „ca.“-Werte (Mercedes eSprinter LFP) durch Herstellerangaben ersetzen.")
    out.append("5. Werte mit Puffer < 1 % gegen Herstellerdatenblätter prüfen.")
    return "\n".join(out)


# ---------------------------------------------------------------- Quellseite
def source_page():
    br = Counter(fams[s]["brand"] for s, _ in all_rows)
    out = [fm(type="source", updated=TODAY, tags=["rohquelle", "tabelle", "batteriekapazitaet"])]
    out.append("# TN Batterycheck – alle Daten (Excel)\n")
    out.append(f"**Herausgeber:** nicht angegeben · **Eingang:** {TODAY} · **Art:** Tabelle (xlsx, 2 Blätter)")
    out.append("**Raw:** `raw/tn_batterycheck_alle_daten.xlsx`\n")
    out.append("## Kernaussagen\n")
    out.append(f"- Referenztabelle mit **Brutto- und Nettokapazität** der [[traktionsbatterie]] für **{len(all_rows)} Fahrzeugvarianten** von **{len(br)} Herstellern**.")
    out.append(f"- Die Varianten lassen sich zu **{len(fams)} Modellreihen** zusammenfassen – jede hat in diesem Wiki eine eigene Seite.")
    out.append("- Zweck ist offenbar ein [[batteriecheck]]: Die [[nettokapazitaet]] ist der Referenzwert, gegen den der [[state-of-health]] einer gebrauchten Batterie gerechnet wird.")
    out.append("- Das Blatt „Übersicht“ belegt einen internen Abgleich: extrahierte Zeilen = Zeilen laut Quellangabe, für alle Marken „OK“.")
    out.append("- Einzelne Zeilen sind fehlerhaft oder doppelt, siehe [[datenqualitaet]].\n")
    out.append("## Aufbau\n")
    out.append("| Blatt | Inhalt |\n|---|---|")
    out.append("| Fahrzeuge | 469 Zeilen: Marke, Modell, Kapazität brutto, Kapazität netto (Text mit Einheit „kWh“, Dezimalpunkt) |")
    out.append("| Übersicht | je Marke: extrahierte Zeilen, Quellangabe, Abgleich (alle „OK“), Summe 469 |\n")
    out.append("## Zeilen je Hersteller\n")
    out.append("| Hersteller | Varianten | Modellreihen |\n|---|---|---|")
    for brand, n in br.most_common():
        bname = brands.get(brand, {}).get("name", brand)
        out.append(f"| [[{BRAND_SLUG[brand]}|{bname}]] | {n} | {sum(1 for s in fams if fams[s]['brand'] == brand)} |")
    out.append("")
    out.append("## Zusammenfassung\n")
    b_all = [r["brutto"] for _, r in all_rows]
    out.append(f"Die Tabelle deckt praktisch den gesamten europäischen Elektroauto-Markt von 2011 (Mitsubishi-i-MiEV-Ableger [[citroen-c-zero]], [[peugeot-ion]]) "
               f"bis 2025 ab, vom Kleinstwagen mit {num(min(b_all))} kWh bis zum Pick-up [[ford-f-150-lightning]] mit {num(max(b_all))} kWh brutto. "
               "Tesla (63), Porsche (41), Volkswagen (41) und Audi (40) sind am stärksten vertreten – bei Porsche vor allem, weil jede Taycan-Karosserie und "
               "Leistungsstufe einzeln mit beiden Batteriegenerationen gelistet ist.\n")
    out.append("Es fehlt eine Angabe zu Modelljahr oder Batterie-Generation. Deshalb erscheinen gleichnamige Varianten mehrfach mit unterschiedlichen "
               "Werten (z. B. Audi e-tron 55 quattro mit drei Nettowerten, Hyundai IONIQ 5 Long Range mit 72,6 und 77,4 kWh). Für einen [[batteriecheck]] "
               "muss die Generation also aus anderen Fahrzeugdaten bestimmt werden. Die Werte sind in sich weitgehend plausibel; "
               "Ausreißer sind in [[datenqualitaet]] gesammelt.\n")
    out.append("## Berührte Seiten\n")
    out.append(f"- Alle {len(fams)} Fahrzeugseiten — Kapazitätstabellen (siehe [[fahrzeuguebersicht]])")
    out.append(f"- Alle {len(BRAND_SLUG)} Herstellerseiten — Kennzahlen je Marke")
    out.append("- [[bruttokapazitaet]], [[nettokapazitaet]], [[batteriepuffer]], [[software-lock]], [[lfp-zellchemie]], [[plattform-geschwister]] — Zahlenbeispiele")
    out.append("- [[puffer-analyse]], [[datenqualitaet]] — Auswertungen\n")
    out.append("## Widersprüche und Spannungen\n")
    out.append("- Cupra Born Zeile 99: netto (60 kWh) > brutto (53 kWh) — widerspricht der Definition in [[nettokapazitaet]].")
    out.append("- [[mercedes-eqt]] (50/45 kWh) vs. baugleicher [[renault-kangoo-electric|Renault Kangoo E-Tech]] (48/45 kWh) — gleiche Batterie, verschiedene Bruttowerte.")
    out.append("- [[renault-city-k-ze]] (30/26,8 kWh) vs. baugleicher [[dacia-spring]] (26,8/25 kWh).\n")
    out.append("## Offene Fragen\n")
    out.append("- Wer ist der Herausgeber (Präfix „tn“)? Aus welcher Primärquelle stammen die Werte (Herstellerangaben, eigene Messungen, Datenbank)?")
    out.append("- Stichtag der Daten? Neueste Modelle (Kia EV4, Hyundai IONIQ 9, Škoda Elroq) deuten auf Stand 2025 hin.")
    out.append("- Sind die Tesla-Nettowerte gemessen oder berechnet? Viele liegen exakt bei 95 % des Bruttowerts.")
    return "\n".join(out)


# ---------------------------------------------------------------- Index
def index_page():
    n_pages = len(fams) + len(BRAND_SLUG) + len(CONCEPTS) + 3 + 1
    out = ["# Index\n", f"1 Quelle · {n_pages} Seiten · Stand {TODAY}\n",
           "Katalog aller Seiten des Fahrzeug-Wikis. Einstieg: [[fahrzeuguebersicht]].\n"]
    out.append("## Synthese\n")
    out.append("- [[fahrzeuguebersicht]] — alle Modellreihen mit Segment, Plattform und Kapazitätsspanne")
    out.append("- [[puffer-analyse]] — Brutto vs. Netto: Verteilung, Extremwerte, Hersteller-Vergleich")
    out.append("- [[datenqualitaet]] — Fehler, Duplikate und Unklarheiten in der Rohquelle\n")
    out.append("## Hersteller\n")
    for brand, bslug in BRAND_SLUG.items():
        b = brands.get(brand, {})
        n = sum(1 for s in fams if fams[s]["brand"] == brand)
        out.append(f"- [[{bslug}|{b.get('name', brand)}]] — {b.get('kurz', '')} · {n} Modellreihen")
    out.append("")
    out.append("## Fahrzeuge\n")
    for brand, bslug in BRAND_SLUG.items():
        out.append(f"### {brands.get(brand, {}).get('name', brand)}\n")
        for s in fams:
            if fams[s]["brand"] == brand:
                fr = fams[s]["rows"]
                out.append(f"- [[{s}|{fams[s]['name']}]] — {meta[s].get('segment') or ''} · {len(fr)} Varianten · netto {span([r['netto'] for r in fr])}")
        out.append("")
    out.append("## Fachbegriffe\n")
    for kat, slugs in KATEGORIEN.items():
        out.append(f"### {kat}\n")
        for c in slugs:
            out.append(f"- [[{c}|{CONCEPTS[c][0]}]] — {CONCEPTS[c][1]}")
        out.append("")
    out.append("## Quellen\n")
    out.append(f"- [[{SRC}]] — Excel-Tabelle, {len(all_rows)} Varianten, Eingang {TODAY} — Brutto-/Nettokapazität aller Fahrzeuge")
    return "\n".join(out)


# ---------------------------------------------------------------- Schreiben + Linkprüfung
def main():
    missing_concepts = set(c for cs in KATEGORIEN.values() for c in cs) ^ set(CONCEPTS)
    if missing_concepts:
        raise SystemExit(f"Kategorien/Konzepte inkonsistent: {missing_concepts}")
    pages = {}
    for s in fams:
        pages[WIKI / "entities" / "fahrzeuge" / f"{s}.md"] = vehicle_page(s)
    for brand, bslug in BRAND_SLUG.items():
        pages[WIKI / "entities" / "hersteller" / f"{bslug}.md"] = brand_page(brand)
    for c in CONCEPTS:
        pages[WIKI / "concepts" / f"{c}.md"] = concept_page(c)
    pages[WIKI / "synthesis" / "fahrzeuguebersicht.md"] = overview_page()
    pages[WIKI / "synthesis" / "puffer-analyse.md"] = buffer_page()
    pages[WIKI / "synthesis" / "datenqualitaet.md"] = quality_page()
    pages[WIKI / "sources" / f"{SRC}.md"] = source_page()
    pages[ROOT / "index.md"] = index_page()

    names = {p.stem for p in pages if p.name != "index.md"}
    broken = Counter()
    for p, text in pages.items():
        for target in link_re.findall(text):
            if Path(target).suffix.lower() in (".jpg", ".png"):
                if not (BILDER / target).exists():
                    broken[(p.stem, target)] += 1
                continue
            if target not in names:
                broken[(p.stem, target)] += 1
    for p, text in pages.items():
        write(p, text)
    print(f"{len(pages)} Seiten geschrieben")
    if broken:
        print("KAPUTTE LINKS:")
        for (src, tgt), n in broken.items():
            print(f"  {src} -> {tgt} ({n}x)")
    # Waisen
    incoming = Counter(t for p, text in pages.items() for t in set(link_re.findall(text)) if t != p.stem)
    orphans = [n for n in names if incoming[n] == 0]
    print("Waisenseiten:", orphans or "keine")


if __name__ == "__main__":
    main()
