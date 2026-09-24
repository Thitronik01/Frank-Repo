"""Liest die bereinigte Tabelle (data/, erzeugt von tools/clean.py) und ordnet jede Zeile einer Modellreihe zu.

Die Zuordnung (RULES) arbeitet mit Marke/Modell der Rohquelle, damit sie von Umbenennungen unabhängig bleibt.
Ausgabe: tools/families.json  ->  {slug: {brand, name, rows: [{zeile, modell, brutto, netto, status, …}]}}
"""
import json
import re
from collections import OrderedDict
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "tn_batterycheck_bereinigt.xlsx"

# (Marke, Regex auf Modellbezeichnung, Slug, Artikelname) — erste passende Regel gewinnt
RULES = [
    ("Audi", r"^(RS )?e-tron GT", "audi-e-tron-gt", "Audi e-tron GT"),
    ("Audi", r"^e-tron", "audi-e-tron", "Audi e-tron"),
    ("Audi", r"^S?Q8", "audi-q8-e-tron", "Audi Q8 e-tron"),
    ("Audi", r"^Q4", "audi-q4-e-tron", "Audi Q4 e-tron"),
    ("Audi", r"^S?Q6", "audi-q6-e-tron", "Audi Q6 e-tron"),
    ("BMW", r"^i3", "bmw-i3", "BMW i3"),
    ("BMW", r"^i4", "bmw-i4", "BMW i4"),
    ("BMW", r"^i5", "bmw-i5", "BMW i5"),
    ("BMW", r"^i7", "bmw-i7", "BMW i7"),
    ("BMW", r"^iX1", "bmw-ix1", "BMW iX1"),
    ("BMW", r"^iX2", "bmw-ix2", "BMW iX2"),
    ("BMW", r"^iX3", "bmw-ix3", "BMW iX3"),
    ("BMW", r"^iX", "bmw-ix", "BMW iX"),
    ("Citroen", r"^C-Zero", "citroen-c-zero", "Citroën C-Zero"),
    ("Citroen", r"(?i)^e-Berlingo", "citroen-e-berlingo", "Citroën ë-Berlingo"),
    ("Citroen", r"^e-C3 Aircross", "citroen-e-c3-aircross", "Citroën ë-C3 Aircross"),
    ("Citroen", r"^e-C3", "citroen-e-c3", "Citroën ë-C3"),
    ("Citroen", r"^e-C4 X", "citroen-e-c4-x", "Citroën ë-C4 X"),
    ("Citroen", r"^e-C4", "citroen-e-c4", "Citroën ë-C4"),
    ("Citroen", r"^e-Jumpy", "citroen-e-jumpy", "Citroën ë-Jumpy Combi"),
    ("Citroen", r"^e-Spacetourer", "citroen-e-spacetourer", "Citroën ë-SpaceTourer"),
    ("Cupra", r"^Born", "cupra-born", "Cupra Born"),
    ("Cupra", r"^Tavascan", "cupra-tavascan", "Cupra Tavascan"),
    ("Dacia", r"^Spring", "dacia-spring", "Dacia Spring Electric"),
    ("Ford", r"^F-150", "ford-f-150-lightning", "Ford F-150 Lightning"),
    ("Ford", r"^Mustang Mach-E", "ford-mustang-mach-e", "Ford Mustang Mach-E"),
    ("Hyundai", r"^INSTER", "hyundai-inster", "Hyundai Inster"),
    ("Hyundai", r"^IONIQ 5", "hyundai-ioniq-5", "Hyundai IONIQ 5"),
    ("Hyundai", r"^IONIQ 6", "hyundai-ioniq-6", "Hyundai IONIQ 6"),
    ("Hyundai", r"^IONIQ 9", "hyundai-ioniq-9", "Hyundai IONIQ 9"),
    ("Hyundai", r"^IONIQ Electric", "hyundai-ioniq-electric", "Hyundai IONIQ Elektro"),
    ("Hyundai", r"^Kona", "hyundai-kona-electric", "Hyundai Kona Elektro"),
    ("Kia", r"^(e-Niro|Niro EV)", "kia-niro-ev", "Kia e-Niro / Niro EV"),
    ("Kia", r"^(e-Soul|Soul EV)", "kia-soul-ev", "Kia Soul EV / e-Soul"),
    ("Kia", r"^EV3", "kia-ev3", "Kia EV3"),
    ("Kia", r"^EV4", "kia-ev4", "Kia EV4"),
    ("Kia", r"^EV6", "kia-ev6", "Kia EV6"),
    ("Kia", r"^EV9", "kia-ev9", "Kia EV9"),
    ("Mercedes", r"^EQA", "mercedes-eqa", "Mercedes-Benz EQA"),
    ("Mercedes", r"^EQB", "mercedes-eqb", "Mercedes-Benz EQB"),
    ("Mercedes", r"^EQC", "mercedes-eqc", "Mercedes-Benz EQC"),
    ("Mercedes", r"^EQT", "mercedes-eqt", "Mercedes-Benz EQT"),
    ("Mercedes", r"^EQV", "mercedes-eqv", "Mercedes-Benz EQV"),
    ("Mercedes", r"^eSprinter", "mercedes-esprinter", "Mercedes-Benz eSprinter"),
    ("Mercedes", r"^eVito", "mercedes-evito", "Mercedes-Benz eVito"),
    ("MG", r"^Cyberster", "mg-cyberster", "MG Cyberster"),
    ("MG", r"^Marvel R", "mg-marvel-r", "MG Marvel R"),
    ("MG", r"^MG4", "mg4-electric", "MG4 Electric"),
    ("MG", r"^MG5", "mg5-electric", "MG5 Electric"),
    ("MG", r"^ZS EV", "mg-zs-ev", "MG ZS EV"),
    ("Mini", r"^Aceman", "mini-aceman", "Mini Aceman"),
    ("Mini", r"^Cooper", "mini-cooper-electric", "Mini Cooper E / SE"),
    ("Mini", r"^Countryman", "mini-countryman-electric", "Mini Countryman E / SE"),
    ("Peugeot", r"^e-2008", "peugeot-e-2008", "Peugeot e-2008"),
    ("Peugeot", r"^e-208", "peugeot-e-208", "Peugeot e-208"),
    ("Peugeot", r"^e-3008", "peugeot-e-3008", "Peugeot e-3008"),
    ("Peugeot", r"^e-308", "peugeot-e-308", "Peugeot e-308"),
    ("Peugeot", r"^e-408", "peugeot-e-408", "Peugeot e-408"),
    ("Peugeot", r"^e-Expert", "peugeot-e-expert", "Peugeot e-Expert Combi"),
    ("Peugeot", r"^e-Partner", "peugeot-e-partner", "Peugeot e-Partner"),
    ("Peugeot", r"^e-Rifter", "peugeot-e-rifter", "Peugeot e-Rifter"),
    ("Peugeot", r"^e-Traveller", "peugeot-e-traveller", "Peugeot e-Traveller"),
    ("Peugeot", r"^iOn", "peugeot-ion", "Peugeot iOn"),
    ("Peugeot", r"^Partner Tepee", "peugeot-partner-tepee-electric", "Peugeot Partner Tepee Electric"),
    ("Porsche", r"^Macan", "porsche-macan-electric", "Porsche Macan (Elektro)"),
    ("Porsche", r"^Taycan", "porsche-taycan", "Porsche Taycan"),
    ("Renault", r"^City K-ZE", "renault-city-k-ze", "Renault City K-ZE"),
    ("Renault", r"^Kangoo", "renault-kangoo-electric", "Renault Kangoo Z.E. / E-Tech"),
    ("Renault", r"^Master", "renault-master-electric", "Renault Master Z.E. / E-Tech"),
    ("Renault", r"^Scenic", "renault-scenic-e-tech", "Renault Scenic E-Tech"),
    ("Renault", r"^Twingo", "renault-twingo-electric", "Renault Twingo Electric"),
    ("Renault", r"^Zoe", "renault-zoe", "Renault Zoe"),
    ("Seat", r"^Mii", "seat-mii-electric", "Seat Mii electric"),
    ("Skoda", r"^Citigo", "skoda-citigo-e-iv", "Škoda Citigo e iV"),
    ("Skoda", r"^Elroq", "skoda-elroq", "Škoda Elroq"),
    ("Skoda", r"^Enyaq", "skoda-enyaq", "Škoda Enyaq"),
    ("Tesla", r"^Model 3", "tesla-model-3", "Tesla Model 3"),
    ("Tesla", r"^Model S", "tesla-model-s", "Tesla Model S"),
    ("Tesla", r"^Model X", "tesla-model-x", "Tesla Model X"),
    ("Tesla", r"^Model Y", "tesla-model-y", "Tesla Model Y"),
    ("Volkswagen", r"^e-Golf", "vw-e-golf", "VW e-Golf"),
    ("Volkswagen", r"^e-Up", "vw-e-up", "VW e-up!"),
    ("Volkswagen", r"^ID\.3", "vw-id-3", "VW ID.3"),
    ("Volkswagen", r"^ID\.4", "vw-id-4", "VW ID.4"),
    ("Volkswagen", r"^ID\.5", "vw-id-5", "VW ID.5"),
    ("Volkswagen", r"^ID\.7", "vw-id-7", "VW ID.7"),
    ("Volkswagen", r"^ID\.BUZZ", "vw-id-buzz", "VW ID. Buzz"),
    ("Volvo", r"^(C40|EC40)", "volvo-ec40", "Volvo EC40 (C40 Recharge)"),
    ("Volvo", r"^(XC40|EX40)", "volvo-ex40", "Volvo EX40 (XC40 Recharge)"),
    ("Volvo", r"^EX90", "volvo-ex90", "Volvo EX90"),
]


def fmt(x):
    return ("%g" % x) + " kWh"


def main():
    ws = openpyxl.load_workbook(DATA, data_only=True)["Fahrzeuge"]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    fams = OrderedDict()
    for values in it:
        r = dict(zip(head, values))
        marke, modell = r["Marke (Rohquelle)"], r["Modell (Rohquelle)"]
        for b, pat, slug, name in RULES:
            if b == marke and re.search(pat, modell):
                f = fams.setdefault(slug, {"brand": marke, "name": name, "rows": []})
                ca = r["Status"] == "Näherungswert"
                f["rows"].append({
                    "zeile": r["Zeile (Rohquelle)"], "modell": r["Modell"], "modell_raw": modell,
                    "brutto": float(r["Brutto kWh"]), "netto": float(r["Netto kWh"]), "ca": ca,
                    "brutto_raw": ("ca. " if ca else "") + fmt(float(r["Brutto kWh"])),
                    "netto_raw": fmt(float(r["Netto kWh"])),
                    "brutto_alt": str(r["Brutto (Rohquelle)"]), "netto_alt": str(r["Netto (Rohquelle)"]),
                    "status": r["Status"], "alias_von": r["Alias von Zeile"] or None, "bemerkung": r["Bemerkung"] or "",
                    "issue": r["Issue"] or "", "quelle": r["Quelle"] or "",
                    "mj_von": r["Modelljahr von"] or "", "mj_bis": r["Modelljahr bis"] or "",
                    "generation": r["Batterie-Generation"] or "",
                })
                break
        else:
            raise SystemExit(f"Keine Regel fuer {marke} {modell}")
    (ROOT / "tools" / "families.json").write_text(json.dumps(fams, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(fams), "Modellreihen,", sum(len(f["rows"]) for f in fams.values()), "Zeilen")


if __name__ == "__main__":
    main()
