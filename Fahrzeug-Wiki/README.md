# Fahrzeug-Wiki

Knowledge Base zu allen 469 Fahrzeugvarianten aus `tn_batterycheck_alle_daten.xlsx` –
90 Fahrzeugartikel mit Bild, 19 Herstellerseiten, 37 Fachbegriffe.

## Öffnen

**Empfohlen: [Obsidian](https://obsidian.md)** → „Ordner als Vault öffnen“ → diesen Ordner wählen → `index.md` öffnen.
Wikilinks, Bilder, Graph-Ansicht und Backlinks funktionieren sofort – auch offline.
Die Fahrzeugfotos liegen lokal im Ordner `Bilder/` (90 Dateien, `<fahrzeug-slug>.jpg`, 960 px, ca. 16 MB).

**Im Browser mit Chat-Assistent (localhost):** im Wiki-Ordner ausführen

    python chat/server.py

und http://localhost:8765 öffnen. Rechts unten sitzt **Ampere**, der Chat-Assistent (RAG über das Wiki, Sprachmodell über anymize).
Für KI-Antworten den anymize-Key in `chat/.env` eintragen – siehe `chat/README.md`. Ohne Key zeigt der Chat die passenden Wiki-Stellen.

Die HTML-Fassung unter `site/` erzeugt `python tools/site.py` (benötigt `pip install markdown`).
Erscheinungsbild: `ci/CI-Leitfaden.md` (auch als Seite „Corporate Identity“ im Wiki).

Einstiegsseiten:
- `index.md` – Katalog aller Seiten
- `wiki/synthesis/fahrzeuguebersicht.md` – alle Modelle auf einen Blick
- `wiki/synthesis/datenqualitaet.md` – Fehler in der Excel-Quelle

## Aktualisieren

Siehe `CLAUDE.md`. Kurz: Texte in `tools/meta/*.json` bzw. `tools/concepts_src.py` ändern, dann
`python tools/build.py`. Seiten in `wiki/` nicht direkt bearbeiten – sie werden neu generiert.

## Bildnachweis

Alle Fahrzeugfotos in `Bilder/` stammen von Wikimedia Commons. Urheber und Lizenz (überwiegend CC BY-SA)
stehen unter jedem Bild auf der jeweiligen Fahrzeugseite.
