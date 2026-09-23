# Fahrzeug-Wiki – Batterie-Referenzdaten für Elektrofahrzeuge

Knowledge Base zu **469 Fahrzeugvarianten** (19 Hersteller) aus `tn_batterycheck_alle_daten.xlsx`:
Brutto-/Nettokapazität der Traktionsbatterie als Referenz für den Batteriecheck (State of Health).

<table>
<tr><td align="center"><a href="Fahrzeug-Wiki/wiki/entities/fahrzeuge/porsche-taycan.md"><img src="Fahrzeug-Wiki/Bilder/porsche-taycan.jpg" width="190" alt="Porsche Taycan"><br><sub>Porsche Taycan</sub></a></td><td align="center"><a href="Fahrzeug-Wiki/wiki/entities/fahrzeuge/vw-id-3.md"><img src="Fahrzeug-Wiki/Bilder/vw-id-3.jpg" width="190" alt="VW ID.3"><br><sub>VW ID.3</sub></a></td><td align="center"><a href="Fahrzeug-Wiki/wiki/entities/fahrzeuge/tesla-model-3.md"><img src="Fahrzeug-Wiki/Bilder/tesla-model-3.jpg" width="190" alt="Tesla Model 3"><br><sub>Tesla Model 3</sub></a></td><td align="center"><a href="Fahrzeug-Wiki/wiki/entities/fahrzeuge/hyundai-ioniq-5.md"><img src="Fahrzeug-Wiki/Bilder/hyundai-ioniq-5.jpg" width="190" alt="Hyundai IONIQ 5"><br><sub>Hyundai IONIQ 5</sub></a></td></tr>
<tr><td align="center"><a href="Fahrzeug-Wiki/wiki/entities/fahrzeuge/bmw-i4.md"><img src="Fahrzeug-Wiki/Bilder/bmw-i4.jpg" width="190" alt="BMW i4"><br><sub>BMW i4</sub></a></td><td align="center"><a href="Fahrzeug-Wiki/wiki/entities/fahrzeuge/renault-zoe.md"><img src="Fahrzeug-Wiki/Bilder/renault-zoe.jpg" width="190" alt="Renault Zoe"><br><sub>Renault Zoe</sub></a></td><td align="center"><a href="Fahrzeug-Wiki/wiki/entities/fahrzeuge/audi-q4-e-tron.md"><img src="Fahrzeug-Wiki/Bilder/audi-q4-e-tron.jpg" width="190" alt="Audi Q4 e-tron"><br><sub>Audi Q4 e-tron</sub></a></td><td align="center"><a href="Fahrzeug-Wiki/wiki/entities/fahrzeuge/kia-ev6.md"><img src="Fahrzeug-Wiki/Bilder/kia-ev6.jpg" width="190" alt="Kia EV6"><br><sub>Kia EV6</sub></a></td></tr>
</table>

## Inhalt

| | |
|---|---|
| 🚗 **[90 Fahrzeugartikel](Fahrzeug-Wiki/wiki/entities/fahrzeuge/)** | je Modellreihe: Bild, Steckbrief, alle Varianten mit Brutto/Netto/Puffer |
| 🏭 **[19 Herstellerseiten](Fahrzeug-Wiki/wiki/entities/hersteller/)** | Kennzahlen und Bildergalerie je Marke |
| 📖 **[37 Fachbegriffe](Fahrzeug-Wiki/wiki/concepts/)** | Bruttokapazität, SoH, LFP/NMC, MEB, E-GMP, 800 Volt … |
| 📊 **[Fahrzeugübersicht](Fahrzeug-Wiki/wiki/synthesis/fahrzeuguebersicht.md)** · **[Puffer-Analyse](Fahrzeug-Wiki/wiki/synthesis/puffer-analyse.md)** | Auswertungen über alle Modelle |
| ⚠️ **[Datenqualität](Fahrzeug-Wiki/wiki/synthesis/datenqualitaet.md)** · **[Issues](../../issues)** | Fehler und Widersprüche in der Rohquelle, offene Klärungen |
| 🗂️ **[Index](Fahrzeug-Wiki/index.md)** | Katalog aller Seiten |

## Ordner

```
Fahrzeug-Wiki/
├── raw/        Rohquelle (Excel, unverändert)
├── wiki/       generierte Wiki-Seiten (Markdown, Obsidian-kompatibel)
├── Bilder/     90 Fahrzeugfotos (Wikimedia Commons, CC-Lizenzen)
├── tools/      Generator: families.py, images.py, build.py …
├── site/       HTML-Fassung
├── chat/       Chat-Assistent „Ampere“ (RAG über das Wiki)
├── ci/         Corporate Identity
└── issues/     Entwürfe der Klärungs-Issues
```

## Nutzung

- **Lesen:** direkt hier auf GitHub oder den Ordner `Fahrzeug-Wiki` in [Obsidian](https://obsidian.md) als Vault öffnen
- **Neu bauen:** `python Fahrzeug-Wiki/tools/build.py` (Details in [`Fahrzeug-Wiki/CLAUDE.md`](Fahrzeug-Wiki/CLAUDE.md))
- **Lokal mit Chat:** `python Fahrzeug-Wiki/chat/server.py` → http://localhost:8765 (siehe [`chat/README.md`](Fahrzeug-Wiki/chat/README.md))

## Bildnachweis

Alle Fahrzeugfotos stammen von Wikimedia Commons. Urheber und Lizenz stehen unter jedem Bild auf der jeweiligen Fahrzeugseite.
