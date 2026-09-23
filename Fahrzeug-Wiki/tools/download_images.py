"""Lädt die in tools/images.json ausgewählten Commons-Bilder (960 px) nach Bilder/<slug>.<ext>.

Bereits vorhandene Dateien werden übersprungen; mit --force neu laden.
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Bilder"
UA = {"User-Agent": "FahrzeugWiki/1.0 (local knowledge base build; python-urllib)"}


def local_name(slug, im):
    ext = Path(im["thumb"].split("?")[0]).suffix.lower() or ".jpg"
    return f"{slug}{'.jpg' if ext == '.jpeg' else ext}"


def main():
    force = "--force" in sys.argv
    images = json.loads((ROOT / "tools" / "images.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    total = 0
    for slug, im in images.items():
        if not im.get("thumb"):
            print("kein Bild:", slug)
            continue
        target = OUT / local_name(slug, im)
        if target.exists() and not force:
            total += target.stat().st_size
            continue
        for attempt in range(5):
            try:
                req = urllib.request.Request(im["thumb"].split("?")[0], headers=UA)
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = r.read()
                break
            except Exception as e:
                print(f"  {slug}: {e} – neuer Versuch")
                time.sleep(10 * (attempt + 1))
        else:
            print("FEHLGESCHLAGEN:", slug)
            continue
        target.write_bytes(data)
        total += len(data)
        print(f"{target.name:45} {len(data) // 1024:5} KB")
        time.sleep(1)
    print(f"Gesamt: {total / 1024 / 1024:.1f} MB in {OUT}")


if __name__ == "__main__":
    main()
