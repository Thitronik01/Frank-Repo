"""Legt die Issues aus issues.json im GitHub-Repo an (einmalig ausführen).

Voraussetzung: GitHub-CLI angemeldet (gh auth login).
Aufruf:  python issues/create_issues.py            -> legt an
         python issues/create_issues.py --dry-run  -> zeigt nur an
Bereits vorhandene Issues mit gleichem Titel werden übersprungen.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = "Thitronik01/Frank-Repo"
LABEL_COLORS = {"datenfehler": "d73a4a", "widerspruch": "e99695", "unklar": "fbca04",
                "bezeichnung": "c5def5", "struktur": "5319e7", "dokumentation": "0075ca", "niedrig": "ededed"}
DRY = "--dry-run" in sys.argv


def gh(*args):
    return subprocess.run(["gh", *args, "--repo", REPO], capture_output=True, text=True, encoding="utf-8")


def body(i):
    return f"""**Quelle:** `Fahrzeug-Wiki/raw/tn_batterycheck_alle_daten.xlsx`, Blatt „Fahrzeuge“, Zeile(n) {i['zeilen']}

### Ist-Zustand
{i['ist']}

### Problem
{i['problem']}

### Zu klären
{i['klaeren']}

### Vorschlag
{i['vorschlag']}

---
- [ ] Entscheidung / korrekter Wert: 
- [ ] Beleg (Datenblatt, URL, Datum): 

Nach Klärung wird der Wert in der bereinigten Tabelle korrigiert und im Änderungsprotokoll vermerkt. Siehe auch `Fahrzeug-Wiki/wiki/synthesis/datenqualitaet.md`.
"""


def main():
    issues = json.loads((Path(__file__).parent / "issues.json").read_text(encoding="utf-8"))
    existing = set()
    if not DRY:
        for label, color in LABEL_COLORS.items():
            gh("label", "create", label, "--color", color, "--force")
        r = gh("issue", "list", "--state", "all", "--limit", "500", "--json", "title")
        existing = {x["title"] for x in json.loads(r.stdout or "[]")}
    for i in issues:
        if i["title"] in existing:
            print("übersprungen:", i["title"])
            continue
        if DRY:
            print(f"[{', '.join(i['labels'])}] {i['title']}")
            continue
        args = ["issue", "create", "--title", i["title"], "--body", body(i)]
        for l in i["labels"]:
            args += ["--label", l]
        r = gh(*args)
        print(r.stdout.strip() or r.stderr.strip())


if __name__ == "__main__":
    main()
