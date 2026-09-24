# Log

## [2026-09-23] setup | Fahrzeug-Wiki angelegt
Struktur nach LLM-Wiki-Muster (Karpathy): raw/, wiki/{sources,entities,concepts,synthesis}, index.md, log.md, CLAUDE.md.
Generator unter tools/ (families.py, images.py, build.py).

## [2026-09-23] ingest | TN Batterycheck – alle Daten (Excel)
Neu: [[tn-batterycheck-alle-daten]], 90 Fahrzeugseiten, 19 Herstellerseiten, 37 Fachbegriffe,
[[fahrzeuguebersicht]], [[puffer-analyse]], [[datenqualitaet]]
Bilder: 90 Fotos von Wikimedia Commons (via Wikidata P18 bzw. gezielte Auswahl), alle CC-lizenziert oder gemeinfrei
Widerspruch: Cupra Born Zeile 99 netto > brutto; Mercedes EQT vs. Renault Kangoo E-Tech und Renault City K-ZE vs. Dacia Spring
(baugleich, aber verschiedene Werte); Audi e-tron S quattro mit Taycan-Werten 105/97 kWh
Duplikat: Porsche Taycan Sport Turismo 93,4/83,7 kWh (Zeilen 281/282)

## [2026-09-23] maintenance | Bilder lokal gespeichert
90 Fahrzeugfotos (960 px, 15,6 MB) von Wikimedia Commons nach `Bilder/` geladen (tools/download_images.py).
Fahrzeugseiten binden sie per relativem Pfad ein, Herstellergalerien per `![[slug.jpg|160]]`. Wiki ist damit offline nutzbar.

## [2026-09-23] maintenance | HTML-Ansicht für localhost
tools/site.py erzeugt 153 HTML-Seiten unter `site/` (Navigation, Suche, Bildkarten, Rückverweise). Server: `python -m http.server 8765` im Wiki-Root, Einstieg http://localhost:8765.

## [2026-09-23] feature | Corporate Identity und Chat-Assistent „Ampere“
CI: Signet (Batterie mit Ladeblitz), Wortmarke, Farben Ladegrün/Voltgelb/Graphit (alle Textpaare WCAG AA), Space Grotesk + Inter, Leitfaden `ci/CI-Leitfaden.md`, Tokens `ci/tokens.css`; auf HTML-Seite angewendet.
Chat: RAG-Index über 901 Wiki-Abschnitte (BM25, lokal), Server `chat/server.py` mit anymize-Anbindung (OpenAI-kompatibel, Streaming), einbettbares Widget `chat/widget/fw-chat.js`. Ohne Key: Modus „nur Suche“.

## [2026-09-24] feature | HTML-App: UX/UI überarbeitet (UI/UX Pro Max)
Neu: Kopfleiste mit Schnellsuche (Strg+K bzw. /, Tastatursteuerung, Vorschaubilder, Ampere als Rückfalloption),
Fahrzeugseiten mit Kennzahlen-Kacheln (Netto/Brutto/Puffer/Varianten) und Steckbrief neben dem Bild,
sortier- und filterbare Tabellen mit Puffer-Balken, Inhaltsverzeichnis mit aktivem Abschnitt, Startseite mit
Fahrzeug-Explorer (Marken-Chips, Filter, Sortierung, Direktlinks per ?q=&marke=&sort=), Hersteller-Kacheln,
Fachbegriffe als Karten, verwandte Fahrzeuge mit Bild, Hinweisbox „Offene Punkte“ mit Link zu den GitHub-Issues,
Dunkelmodus-Umschalter (auch im Chat-Widget), mobiles Menü als Drawer, SVG-Icons statt Emoji, Skip-Link,
44-px-Touchziele, prefers-reduced-motion.
Technik: CSS/JS als eigene Dateien (tools/site_assets/) mit Inhalts-Hash im Link; Server sendet Cache-Control: no-cache.
Geprüft: 154 Seiten ohne tote Links/Anker, je eine h1, alle Bilder mit alt, keine doppelten IDs, keine Konsolenfehler; 390 px ohne Querscrollen.
