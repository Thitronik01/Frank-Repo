# Fahrzeug-Wiki

Persistentes Wiki über Elektrofahrzeuge und ihre Traktionsbatterien. Gepflegt vom LLM, kuratiert von Frank.
Angelegt am 2026-09-23 nach dem LLM-Wiki-Muster von Andrej Karpathy.

## Zweck

Jedes Fahrzeug aus dem Batteriecheck-Bestand hat einen eigenen Artikel mit Bild, Einordnung und
allen Varianten samt Brutto-/Nettokapazität. Fachbegriffe haben eigene Artikel. Das Wiki soll Fragen
beantworten wie: *Welche Referenzkapazität gilt für Fahrzeug X? Welche Modelle teilen sich eine Batterie?
Wo sind die Daten unsicher? Was bedeutet Begriff Y?*

## Struktur

- `raw/` — Rohquellen. **Immutabel. Niemals bearbeiten.**
- `wiki/sources/` — eine Seite je Rohquelle
- `wiki/entities/fahrzeuge/` — eine Seite je Modellreihe (alle Varianten als Tabelle)
- `wiki/entities/hersteller/` — eine Seite je Marke
- `wiki/concepts/` — Fachbegriffe (Batterie, Laden, Antrieb, Plattformen, Bezeichnungen)
- `wiki/synthesis/` — Übersicht, Puffer-Analyse, Datenqualität
- `index.md` — Katalog aller Seiten · `log.md` — Protokoll
- `Bilder/` — lokale Fahrzeugfotos (`<slug>.jpg`, von Wikimedia Commons)
- `ci/` — Corporate Identity (Leitfaden, Tokens, Logo, Signet)
- `chat/` — Chat-Assistent: Server, RAG-Index, Widget
- `tools/` — Generator und LLM-gepflegte Quelltexte (siehe unten)

## Wichtig: Seiten werden generiert

Die Seiten unter `wiki/` und `index.md` erzeugt `python tools/build.py`. **Nicht direkt in `wiki/` editieren** –
Änderungen gehen beim nächsten Build verloren. Stattdessen:

| Was ändern | Wo |
|---|---|
| Zuordnung Variante → Modellreihe | `tools/families.py` (RULES), dann `python tools/families.py` |
| Fahrzeug- und Herstellertexte | `tools/meta/*.json` |
| Fachbegriffe | `tools/concepts_src.py` |
| Bildauswahl | `tools/image_overrides.json` (Wikipedia-Titel oder `File:…`), dann `python tools/images.py` und `python tools/download_images.py --force` |
| Seitenlayout, Synthesen | `tools/build.py` |

Danach immer `python tools/build.py` ausführen – das Skript meldet kaputte Wikilinks und Waisenseiten.
Anschließend `python tools/site.py` (HTML-Fassung unter `site/`) und `python chat/rag.py build` (Suchindex für den Chat),
dann `python chat/server.py` neu starten (localhost:8765).

## Corporate Identity und Chat

- Erscheinungsbild: `ci/CI-Leitfaden.md`, Tokens in `ci/tokens.css` – neue Oberflächen nutzen nur diese Tokens
- Chat-Assistent „Ampere“: `chat/` (Server, RAG, Widget) – siehe `chat/README.md`
- Der anymize-Key steht nur in `chat/.env` und wird nie ausgeliefert oder ins Wiki geschrieben

## Konventionen

- Wikilinks `[[slug]]` bzw. `[[slug|Anzeigetext]]`; in Tabellen `[[slug\|Text]]` (macht build.py automatisch)
- Dateinamen kebab-case ohne Umlaute
- **Kapazitätswerte nur aus Rohquellen**, immer mit Zeilennummer belegt. Beschreibungen aus Fachwissen
  werden als solche gekennzeichnet (Fußnote ¹).
- Widersprüche und Datenfehler werden markiert (Abschnitt „Offene Punkte“ + [[datenqualitaet]]), nie still korrigiert
- Bilder nur von Wikimedia Commons, immer mit Urheber und Lizenz; lokal in `Bilder/` abgelegt und relativ eingebunden
- Zahlen im Text mit Dezimalkomma; Datumsangaben absolut
- Frontmatter: `type`, `updated`, `sources`, `tags`; Fahrzeuge zusätzlich `hersteller`, `segment`, `plattform`,
  `brutto_min/max`, `netto_min/max`, `bild` (für Obsidian Dataview)

## Workflow: Ingest

1. Neue Datei nach `raw/` legen und vollständig lesen
2. Kernaussagen mit Frank besprechen, **bevor** geschrieben wird
3. Neue Tabelle mit Fahrzeugdaten: `families.py` erweitern bzw. zweite Quelle als eigenes Feld einlesen;
   neue Modellreihen → Texte in `tools/meta/`, Bild in `image_overrides.json`
4. Quellseite unter `wiki/sources/` anlegen (in `build.py` oder als Handseite in `wiki/sources/`, die build.py nicht überschreibt)
5. Abweichungen zur bestehenden Quelle als Widerspruch markieren
6. `python tools/build.py`
7. `log.md` ergänzen: `## [JJJJ-MM-TT] ingest | <Titel>`
8. Kurz berichten: neu / geändert / Widersprüche

## Workflow: Query

1. `index.md` lesen, Kandidaten finden
2. Seiten lesen, bei Bedarf in `raw/` absteigen
3. Antwort mit Verweisen auf Wiki-Seiten und Rohquelle (Zeilennummer)
4. Bei substanzieller Antwort fragen, ob sie unter `wiki/synthesis/` abgelegt wird

## Workflow: Lint

`python tools/build.py` prüft Links und Waisen mechanisch. Inhaltlich prüfen: Widersprüche zwischen Seiten,
Datenlücken (fehlendes Modelljahr!), Fahrzeuge ohne passendes Bild, Fachbegriffe, die oft vorkommen, aber keine
Seite haben. Befund + Vorschlagsliste liefern, Reparaturen erst nach Freigabe.

## Aktuelle Schwerpunkte

- Nur eine Rohquelle – eine zweite (Herstellerdatenblätter, EV-Database) würde die Werte absichern
- Herausgeber und Stichtag der Rohquelle klären
- Offene Datenfehler: siehe [[datenqualitaet]]
