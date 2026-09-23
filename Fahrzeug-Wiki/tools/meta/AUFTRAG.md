# Auftrag: Metadaten für Fahrzeugartikel

Wiki-Root: C:\Users\Rüpprich\OneDrive\Desktop\Frank\Fahrzeug-Wiki
Die Rohdaten je Modellreihe stehen in tools/families.json (Slug -> brand, name, rows[modell, brutto, netto]).
Du schreibst NUR die Datei tools/meta/<gruppe>.json (UTF-8, gültiges JSON). Keine anderen Dateien anfassen.

## Format

{
  "fahrzeuge": {
    "<slug aus families.json>": {
      "kurz": "1–2 Sätze: Was ist das für ein Fahrzeug (Segment, Hersteller, Besonderheit).",
      "segment": "z. B. Kompakt-SUV | Kleinwagen | Oberklasse-Limousine | Transporter",
      "karosserie": "z. B. SUV, SUV-Coupé (Sportback)",
      "bauzeit": "z. B. 2019–2024 oder seit 2021 (nur wenn du sicher bist, sonst null)",
      "plattform": "Name der Plattform im Klartext, z. B. MEB, PPE, E-GMP, J1, e-CMP, Verbrenner-Plattform MFA2 (oder null)",
      "beschreibung": "2–3 Absätze Markdown auf Deutsch (Absätze mit \n\n getrennt). Eigener Text, kein Kopieren aus Wikipedia. Einordnung, Technik, Batterie-Generationen, Besonderheiten. Fachbegriffe beim ersten Auftreten als Wikilink [[konzept-slug|Anzeigetext]] – NUR Slugs aus der Liste unten.",
      "varianten": "Markdown (1 Absatz oder kurze Liste): Wie sind die Variantenbezeichnungen in families.json zu lesen? Warum gibt es mehrere Batteriegrößen (Generationen, Modellpflege)? Beziehe dich konkret auf die Zeilen.",
      "konzepte": ["konzept-slugs, die für dieses Fahrzeug relevant sind (3–8)"],
      "geschwister": ["andere Fahrzeug-Slugs aus families.json mit gleicher Technik/Plattform/Batterie (auch markenübergreifend)"],
      "hinweise": ["Auffälligkeiten in den Rohdaten dieses Fahrzeugs, z. B. netto > brutto, Duplikate, ungewöhnlich großer/kleiner Puffer, 'ca.'-Werte, Schreibweisen. Leer lassen, wenn nichts auffällt."]
    }
  },
  "hersteller": {
    "<Marke genau wie in families.json 'brand'>": {
      "name": "Anzeigename (z. B. Citroën, Mercedes-Benz, Škoda)",
      "kurz": "1 Satz",
      "beschreibung": "1–2 Absätze Markdown: Konzernzugehörigkeit, E-Strategie, Plattformen. Wikilinks nur auf Konzept-Slugs."
    }
  }
}

## Regeln
- Deutsch, sachlich, lexikalisch. Keine Werbesprache.
- Keine erfundenen Zahlen. Kapazitäten kommen aus den Rohdaten (werden automatisch als Tabelle ergänzt) – im Text nur darauf Bezug nehmen, nicht neu erfinden. Weitere Zahlen (Leistung, Ladeleistung, Baujahre) nur, wenn du sehr sicher bist; sonst weglassen.
- Wenn du unsicher bist, schreibe es in "hinweise" statt es zu behaupten.
- Wikilinks auf andere Fahrzeuge: [[<fahrzeug-slug>|Name]] (nur Slugs aus families.json).

## Erlaubte Konzept-Slugs
bruttokapazitaet, nettokapazitaet, batteriepuffer, kilowattstunde, traktionsbatterie, lithium-ionen-akku,
nmc-zellchemie, lfp-zellchemie, batteriemanagementsystem, state-of-health, state-of-charge, batteriealterung,
batteriecheck, software-lock, zellformat, 800-volt-architektur, dc-schnellladen, ac-laden, rekuperation,
range-extender, wltp, allradantrieb, hinterradantrieb, frontantrieb, elektromotor, bev,
plattform-meb, plattform-ppe, plattform-j1, plattform-e-gmp, plattform-stellantis, konversionsfahrzeug,
typbezeichnungen, karosserieformen, plattform-geschwister, elektro-transporter, modellpflege
