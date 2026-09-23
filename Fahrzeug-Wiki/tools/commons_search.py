"""Hilfsskript: listet Commons-Dateikandidaten je Suchbegriff (für image_overrides.json)."""
import json, sys, time, urllib.parse, urllib.request
UA = {"User-Agent": "FahrzeugWiki/1.0 (local knowledge base build; python-urllib)"}
queries = json.loads(open(sys.argv[1], encoding="utf-8").read())
out = {}
for slug, q in queries.items():
    params = dict(action="query", list="search", srsearch=q + " filetype:bitmap", srnamespace=6, srlimit=8,
                  format="json", formatversion=2)
    for attempt in range(6):
        try:
            req = urllib.request.Request("https://commons.wikimedia.org/w/api.php",
                                         data=urllib.parse.urlencode(params).encode(), headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                hits = [h["title"] for h in json.load(r)["query"]["search"]]
            break
        except Exception as e:
            time.sleep(10 * (attempt + 1))
    out[slug] = hits
    print(slug, "|", " || ".join(h[5:] for h in hits), flush=True)
    time.sleep(4)
json.dump(out, open("tools/commons_candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
