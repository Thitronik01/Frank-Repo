"""Ermittelt je Modellreihe ein frei lizenziertes Bild (Wikimedia Commons) samt Urheber und Lizenz.

Vorgehen (Sammelabfragen, weil die Wikimedia-APIs Einzelabfragen stark drosseln):
  1. Wikidata: Bild-Eigenschaft P18 des Objekts zum englischen Wikipedia-Artikel (tools/image_overrides.json)
  2. Commons: Urheber, Lizenz, Thumbnail-URL für alle Dateien in einem Rutsch
Einträge in image_overrides.json, die mit "File:" beginnen, geben die Datei direkt vor.
Bilder werden NICHT heruntergeladen, sondern per URL eingebunden.
Ausgabe: tools/images.json
"""
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "FahrzeugWiki/1.0 (local knowledge base build; python-urllib)"}


def api(host, **params):
    params.update(format="json", formatversion=2)
    body = urllib.parse.urlencode(params).encode()
    for attempt in range(6):
        try:
            req = urllib.request.Request(f"https://{host}/w/api.php", data=body, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            wait = 10 * (attempt + 1)
            print(f"  {host}: {e} – warte {wait}s")
            time.sleep(wait)
    raise RuntimeError(host)


def chunks(seq, n=45):
    seq = list(seq)
    return [seq[i:i + n] for i in range(0, len(seq), n)]


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def main():
    overrides = json.loads((ROOT / "tools" / "image_overrides.json").read_text(encoding="utf-8"))
    files = {slug: v[5:] for slug, v in overrides.items() if v.startswith("File:")}
    titles = {slug: v for slug, v in overrides.items() if not v.startswith("File:")}

    # 1. Wikidata P18
    p18 = {}
    for batch in chunks(set(titles.values())):
        d = api("www.wikidata.org", action="wbgetentities", sites="enwiki", titles="|".join(batch),
                props="claims|sitelinks", sitefilter="enwiki", redirects="yes")
        for ent in d.get("entities", {}).values():
            if "missing" in ent:
                continue
            en = ent.get("sitelinks", {}).get("enwiki", {}).get("title")
            claims = ent.get("claims", {}).get("P18", [])
            if en and claims:
                p18[en.lower()] = claims[0]["mainsnak"]["datavalue"]["value"]
        time.sleep(3)
    for slug, t in titles.items():
        if t.lower() in p18:
            files[slug] = p18[t.lower()]

    # 2. Commons-Metadaten
    info = {}
    for batch in chunks(set(files.values())):
        d = api("commons.wikimedia.org", action="query", titles="|".join("File:" + f for f in batch),
                prop="imageinfo", iiprop="extmetadata|url", iiurlwidth=800)
        norm = {n["to"]: n["from"] for n in d["query"].get("normalized", [])}
        for page in d["query"]["pages"]:
            if not page.get("imageinfo"):
                continue
            ii = page["imageinfo"][0]
            md = ii.get("extmetadata", {})
            entry = {
                "file": page["title"],
                "thumb": ii.get("thumburl"),
                "page": ii.get("descriptionurl"),
                "artist": strip_tags(md.get("Artist", {}).get("value"))[:120],
                "license": strip_tags(md.get("LicenseShortName", {}).get("value")),
            }
            info[page["title"][5:]] = entry
            info[norm.get(page["title"], page["title"])[5:]] = entry
        time.sleep(3)

    out = {}
    for slug in overrides:
        f = files.get(slug)
        out[slug] = {"wikipedia": titles.get(slug), **(info.get(f) or {})}
        print(f"{slug:32} | {f}")
    (ROOT / "tools" / "images.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ohne Bild:", [s for s, v in out.items() if not v.get("thumb")])


if __name__ == "__main__":
    main()
