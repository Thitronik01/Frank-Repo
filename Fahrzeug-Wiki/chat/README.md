# Ampere – Chat-Widget mit RAG

Chat-Assistent für das Fahrzeug-Wiki. Beantwortet Fragen ausschließlich aus dem Wiki und nennt die Quellen.

```
Browser (fw-chat.js)  ──POST /api/chat──▶  chat/server.py
                                              │ 1. Suche im Wiki-Index (rag.py, BM25, lokal)
                                              │ 2. Top-6-Abschnitte + Frage + Systemprompt
                                              ▼
                                   anymize  /api/v1/llm/chat/completions  (Streaming)
                                              │
Browser  ◀── SSE: sources · delta … · done ───┘
```

- **Nur die passenden Wiki-Abschnitte** und die Frage gehen an anymize, nicht das ganze Wiki.
- **Der API-Key bleibt auf dem Server.** Der Browser sieht ihn nie; `.env`, `raw/`, `tools/` werden nicht ausgeliefert.
- **Ohne Key** läuft der Chat im Modus „nur Suche“ und zeigt die passendsten Wiki-Stellen.

## Einrichten

1. `chat/.env.example` nach `chat/.env` kopieren
2. `ANYMIZE_API_KEY=` eintragen (Key aus app.anymize.ai → Einstellungen → API)
3. Optional: `ANYMIZE_BASE_URL` auf `https://app.anymize.ai/api/v1/llm-anonymous` setzen, um die eingebaute Anonymisierung zu nutzen
4. Server starten: `python chat/server.py` → http://localhost:8765
5. Verfügbare Modelle prüfen: http://localhost:8765/api/models → gewünschtes Modell als `ANYMIZE_MODEL` eintragen

## Auf anderen Seiten einbetten

```html
<script src="http://localhost:8765/chat/widget/fw-chat.js" defer></script>
```

Optionen per `data-*`: `data-api`, `data-title`, `data-open="true"`, `data-position="left"`.
Die einbettende Domain muss in `FW_ALLOWED_ORIGINS` stehen (CORS). Per JavaScript steuerbar:
`FahrzeugWikiChat.open()`, `.close()`, `.ask("Frage")`.

Das Widget kapselt sich per Shadow DOM – es übernimmt keine Styles der Gastseite und verändert sie nicht.
Farben und Schriften folgen der Corporate Identity (`ci/tokens.css`), inklusive Dunkelmodus.

## Index aktualisieren

Nach Änderungen am Wiki (`python tools/build.py`):

```
python chat/rag.py build        # Index neu bauen
python chat/rag.py "EQA 250+"   # Suche testen
```

Danach den Server neu starten.

## Endpunkte

| Methode | Pfad | Zweck |
|---|---|---|
| POST | `/api/chat` | `{"messages":[{"role":"user","content":"…"}]}` → Server-Sent Events `sources`, `delta`, `done`, `error` |
| GET | `/api/status` | Verbindungsstatus, Modell, Indexgröße |
| GET | `/api/models` | Modelle von anymize (braucht Key) |

## Dateien

| Datei | Inhalt |
|---|---|
| `server.py` | HTTP-Server: Wiki-Seite, Chat-API, anymize-Anbindung (nur Python-Standardbibliothek) |
| `rag.py` | Chunking des Wikis nach Abschnitten, BM25-Suche mit deutscher Normalisierung |
| `index.json` | erzeugter Suchindex (~900 Abschnitte) |
| `widget/fw-chat.js` | einbettbares Chat-Widget |
| `.env.example` | Konfigurationsvorlage |
