# Corporate Identity

**Fahrzeug-Wiki** – die Wissensbasis für Traktionsbatterien. Dieser Leitfaden legt fest, wie Wiki, Chat-Assistent und alle
künftigen Ableger aussehen und klingen. Technische Quelle aller Werte: `ci/tokens.css`.

## Markenkern

| | |
|---|---|
| **Name** | Fahrzeug-Wiki (Schreibweise immer mit Bindestrich, im Logo als Fahrzeug**Wiki**) |
| **Claim** | Jede Batterie. Jede Variante. Belegt. |
| **Versprechen** | Belastbare Kapazitätswerte zu jedem Elektrofahrzeug – mit Quelle, Zeilennummer und offen benannten Unsicherheiten. |
| **Werte** | **Präzise** (Zahlen immer mit Einheit und Beleg) · **Transparent** (Fehler werden gezeigt, nicht versteckt) · **Zugänglich** (Fachbegriffe werden erklärt) |
| **Zielgruppe** | Batteriecheck-Team, Gebrauchtwagen-Bewertung, Werkstatt, interessierte Laien |

## Logo

<div style="display:flex;gap:24px;flex-wrap:wrap;align-items:center;margin:1em 0">
<div style="background:#FFFFFF;border:1px solid var(--fw-line);border-radius:12px;padding:24px 28px"><img src="../ci/logo.svg" alt="Fahrzeug-Wiki Logo" style="height:48px;width:auto;border-radius:0;display:block"></div>
<div style="background:#F6F5F1;border:1px solid var(--fw-line);border-radius:12px;padding:20px"><img src="../ci/signet.svg" alt="Signet" style="height:64px;width:64px;border-radius:0;display:block"></div>
<div style="background:#14171C;border-radius:12px;padding:20px"><img src="../ci/signet.svg" alt="Signet auf dunkel" style="height:64px;width:64px;border-radius:0;display:block"></div>
</div>

**Signet:** Eine Batterie mit Ladeblitz auf ladegrünem Quadrat mit runden Ecken. Die Batterie steht für das Thema, der Blitz in Voltgelb
für Energie und für den „Aha“-Moment, wenn ein Wert belegt ist. Das Signet funktioniert allein als App-Icon, Favicon und Chat-Avatar.

**Wortmarke:** „Fahrzeug“ in Space Grotesk Medium, „Wiki“ in Space Grotesk Bold und Ladegrün, ohne Leerzeichen gesetzt.

- **Schutzzone:** rundherum mindestens ¼ der Signet-Höhe frei lassen.
- **Mindestgröße:** Signet 16 px (Favicon), Logo mit Wortmarke 120 px breit.
- **Nicht erlaubt:** Farben tauschen, Blitz entfernen, Signet drehen oder verzerren, Schatten/Verläufe hinzufügen, Wortmarke in anderer Schrift setzen.

Dateien: `ci/logo.svg` (Signet + Wortmarke), `ci/signet.svg` (Signet allein).

## Farben

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin:1em 0">
<div style="border:1px solid var(--fw-line);border-radius:12px;overflow:hidden"><div style="background:#0A6B4E;height:64px"></div><div style="padding:8px 12px;font-size:13px"><b>Ladegrün</b><br><code>#0A6B4E</code><br>Primärfarbe</div></div>
<div style="border:1px solid var(--fw-line);border-radius:12px;overflow:hidden"><div style="background:#064A36;height:64px"></div><div style="padding:8px 12px;font-size:13px"><b>Ladegrün tief</b><br><code>#064A36</code><br>Hover, gedrückt</div></div>
<div style="border:1px solid var(--fw-line);border-radius:12px;overflow:hidden"><div style="background:#E1F0EA;height:64px"></div><div style="padding:8px 12px;font-size:13px"><b>Ladegrün hell</b><br><code>#E1F0EA</code><br>Flächen, Zitate</div></div>
<div style="border:1px solid var(--fw-line);border-radius:12px;overflow:hidden"><div style="background:#F4B82E;height:64px"></div><div style="padding:8px 12px;font-size:13px"><b>Voltgelb</b><br><code>#F4B82E</code><br>Akzent, sparsam</div></div>
<div style="border:1px solid var(--fw-line);border-radius:12px;overflow:hidden"><div style="background:#14171C;height:64px"></div><div style="padding:8px 12px;font-size:13px"><b>Graphit</b><br><code>#14171C</code><br>Text, Logo einfarbig</div></div>
<div style="border:1px solid var(--fw-line);border-radius:12px;overflow:hidden"><div style="background:#F6F5F1;height:64px"></div><div style="padding:8px 12px;font-size:13px"><b>Papier</b><br><code>#F6F5F1</code><br>Seitenhintergrund</div></div>
</div>

**Zustandsfarben** – für State of Health, Datenqualität und Hinweise, immer zusammen mit Text oder Symbol (nie Farbe allein):

<div style="display:flex;gap:10px;flex-wrap:wrap;margin:.5em 0 1em">
<span style="background:#17744A;color:#fff;padding:4px 12px;border-radius:999px;font-size:13px">✓ Gut · #17744A</span>
<span style="background:#8F5E00;color:#fff;padding:4px 12px;border-radius:999px;font-size:13px">! Warnung · #8F5E00</span>
<span style="background:#C23B3B;color:#fff;padding:4px 12px;border-radius:999px;font-size:13px">✕ Kritisch · #C23B3B</span>
</div>

**Mengenverhältnis:** rund 70 % Papier/Weiß, 20 % Graphit (Text), 8 % Ladegrün, höchstens 2 % Voltgelb.

**Kontrast (WCAG 2.1):** Alle Text-Farbpaare erfüllen AA (≥ 4,5 : 1) – z. B. Weiß auf Ladegrün 6,5 : 1, Ladegrün auf Papier 6,0 : 1,
Graphit auf Voltgelb 10,0 : 1. Voltgelb nie als Textfarbe auf hellem Grund. Im Dunkelmodus wird Ladegrün zu `#45C79B` aufgehellt
(8,8 : 1 auf dunklem Grund).

## Typografie

| Rolle | Schrift | Einsatz |
|---|---|---|
| Display | **Space Grotesk** 500/700 | Logo, Überschriften, Kennzahlen |
| Text | **Inter** 400/500/600 | Fließtext, Tabellen, Oberflächen |
| Zahlen & Code | **JetBrains Mono** | Dateinamen, Codes, technische Werte |

Fallback ohne Internet: Segoe UI / System-Schrift. Zahlen in Tabellen immer mit **Tabellenziffern** (`font-variant-numeric: tabular-nums`),
damit Kapazitäten untereinander stehen. Dezimalkomma, Einheit mit geschütztem Leerzeichen: `77,0 kWh`.

<div style="border:1px solid var(--fw-line);border-radius:12px;padding:16px 20px;margin:1em 0">
<div style="font-family:var(--fw-font-display);font-size:34px;font-weight:700;line-height:1.1">Porsche Taycan</div>
<div style="font-family:var(--fw-font-display);font-size:22px;font-weight:600;margin-top:10px">Varianten und Batterien</div>
<p style="margin:.4em 0">Fließtext in Inter: Die Nettokapazität ist der Teil der Batterie, den der Fahrer tatsächlich nutzen kann.</p>
<div style="font-family:var(--fw-font-display);font-size:28px;font-weight:700;color:var(--fw-primary)">97,0&nbsp;kWh <span style="font-size:14px;font-weight:500;color:var(--fw-muted)">netto</span></div>
</div>

## Bildsprache

- **Fahrzeugfotos** von Wikimedia Commons, freigestellt im Straßen- oder Messeumfeld, Dreiviertel-Frontansicht bevorzugt.
- Format **16 : 10**, Ecken 10 px gerundet. In Karten zugeschnitten (`object-fit: cover`), im Artikel volle Breite.
- **Bildnachweis ist Pflicht:** Datei, Urheber, Lizenz unter jedem Bild (CC BY-SA verlangt das).
- Keine Stockfotos, keine KI-generierten Fahrzeugbilder – das Wiki zeigt echte Fahrzeuge.
- Icons: schlichte Linien-Icons, 1,5–2 px Strich, gerundete Enden – passend zum Signet.

## Komponenten

| Element | Gestaltung |
|---|---|
| **Kurzbeschreibung** | Zitatblock: Ladegrün-hell, 4 px Ladegrün-Linie links |
| **Tabellen** | Kopfzeile Papier-dunkel, feine Linien, Tabellenziffern, horizontal scrollbar auf dem Handy |
| **Fahrzeugkarte** | Weiße Fläche, 1 px Linie, Radius 16 px, Bild 16 : 10 oben, Titel + Segment + Nettokapazität |
| **Hinweis „Offene Punkte“** | Warnfarbe nur als Linie/Symbol, Text bleibt Graphit |
| **Buttons** | Primär: Ladegrün mit weißer Schrift, Radius 10 px; Sekundär: Linie in Ladegrün |
| **Chat-Widget** | Runder Starter-Button in Ladegrün mit Signet-Blitz; Panel wie Karte, Nutzer-Nachrichten Ladegrün, Assistent Papier |

## Sprache und Tonalität

| | Wiki-Artikel | Chat-Assistent |
|---|---|---|
| **Anrede** | neutral, lexikalisch | Du, freundlich-sachlich |
| **Stil** | kurze Sätze, Fachbegriff beim ersten Auftreten verlinkt | kurze Antwort zuerst, Details danach |
| **Zahlen** | mit Einheit und Quelle | mit Einheit und Quellenverweis [1] |
| **Unsicherheit** | Abschnitt „Offene Punkte“ | offen sagen: „Dazu steht im Wiki nichts.“ |
| **Tabu** | Werbesprache, Superlative ohne Beleg | Erfundene Werte, Kaufberatung, Finanzberatung |

**Beispiel Chat:** „Der VW ID.3 Pro S hat laut Rohquelle 82 kWh brutto und 77,0 kWh netto [1]. Beim ID.3 Pure ist der Bruttowert fraglich [2].“

## Chat-Persona

**Ampere** – der Wiki-Assistent. Benannt nach der Einheit der Stromstärke: sachlich, messbar, nie laut. Ampere antwortet nur aus dem Wiki,
nennt immer die Quellen und sagt ehrlich, wenn etwas nicht belegt ist. Avatar ist das Signet.

## Dateien

| Datei | Inhalt |
|---|---|
| `ci/tokens.css` | Design-Tokens (Farben, Schriften, Radien) – hell und dunkel |
| `ci/logo.svg` | Logo mit Wortmarke |
| `ci/signet.svg` | Signet, auch Favicon und Chat-Avatar |
| `ci/CI-Leitfaden.md` | dieser Leitfaden |
