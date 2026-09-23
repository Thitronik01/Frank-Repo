"""Fahrzeug-Wiki Server: statische Wiki-Seite + Chat-API mit RAG über anymize.

  python chat/server.py            ->  http://localhost:8765

Konfiguration (Umgebungsvariablen oder chat/.env, siehe chat/.env.example):
  ANYMIZE_API_KEY      API-Key von app.anymize.ai (Pflicht für KI-Antworten; ohne Key nur Suchtreffer)
  ANYMIZE_BASE_URL     Standard https://app.anymize.ai/api/v1/llm  (Alternative: .../api/v1/llm-anonymous)
  ANYMIZE_MODEL        Standard fountain-1.0  (verfügbare Modelle: GET /api/models)
  FW_PORT              Standard 8765
  FW_HOST              Standard 127.0.0.1 (nur lokal erreichbar)
  FW_ALLOWED_ORIGINS   Kommagetrennte Origins, die das Widget einbetten dürfen (CORS), z. B. https://intranet.example.de

Der API-Key bleibt auf dem Server – der Browser sieht ihn nie.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import rag  # noqa: E402


# ---------------------------------------------------------------- Konfiguration
def load_env(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env(HERE / ".env")
API_KEY = os.environ.get("ANYMIZE_API_KEY", "").strip()
BASE_URL = os.environ.get("ANYMIZE_BASE_URL", "https://app.anymize.ai/api/v1/llm").rstrip("/")
MODEL = os.environ.get("ANYMIZE_MODEL", "fountain-1.0")
PORT = int(os.environ.get("FW_PORT", "8765"))
HOST = os.environ.get("FW_HOST", "127.0.0.1")
ALLOWED_ORIGINS = {o.strip() for o in os.environ.get("FW_ALLOWED_ORIGINS", "").split(",") if o.strip()}

# Nur diese Pfade werden ausgeliefert (kein Zugriff auf .env, raw/, tools/ …)
PUBLIC_PREFIXES = ("/site/", "/Bilder/", "/ci/", "/chat/widget/")
MAX_BODY = 64 * 1024
MAX_QUESTION = 2000
CONTEXT_BUDGET = 9000

INDEX = rag.load()

SYSTEM_PROMPT = """Du bist Ampere, der Assistent des Fahrzeug-Wikis – einer Wissensbasis über Elektrofahrzeuge und ihre Traktionsbatterien.

Regeln:
- Antworte ausschließlich auf Basis der nummerierten Wiki-Auszüge unten. Erfinde keine Werte.
- Belege jede Aussage mit der Quellnummer in eckigen Klammern, z. B. [1] oder [2][3].
- Steht die Antwort nicht in den Auszügen, sag das offen („Dazu steht im Wiki nichts.“) und schlage eine passende Wiki-Seite vor, falls es eine gibt.
- Kapazitäten immer mit Einheit und Dezimalkomma (77,0 kWh) und – wenn relevant – ob brutto oder netto.
- Weise auf Datenfehler oder offene Punkte hin, wenn die Auszüge welche nennen.
- Sprich den Nutzer mit „du“ an. Kurz und sachlich: erst die direkte Antwort, dann bei Bedarf Details. Markdown ist erlaubt (Listen, **fett**, kleine Tabellen).
- Keine Kauf-, Rechts- oder Finanzberatung."""


# ---------------------------------------------------------------- RAG
def retrieve(messages):
    users = [m["content"] for m in messages if m["role"] == "user"]
    question = users[-1]
    history = " ".join(users[-3:-1])
    hits = INDEX.search(question, k=6, history=history)
    context, sources, used = [], [], 0
    for h in hits:
        block = f"[{len(sources) + 1}] {h['title']} › {h['section']}\n{h['text']}"
        if used + len(block) > CONTEXT_BUDGET and sources:
            break
        used += len(block)
        context.append(block)
        sources.append({"n": len(sources) + 1, "title": h["title"], "section": h["section"], "url": h["url"], "kind": h["kind"]})
    return "\n\n".join(context), sources, hits


def build_messages(messages, context):
    system = SYSTEM_PROMPT + "\n\n# Wiki-Auszüge\n\n" + (context or "(keine passenden Auszüge gefunden)")
    return [{"role": "system", "content": system}] + messages[-8:]


def fallback_answer(hits):
    if not hits:
        return "Ich habe dazu im Wiki nichts gefunden. Versuch es mit einem Modellnamen oder Fachbegriff, z. B. „ID.3“ oder „Nettokapazität“."
    lines = ["**Hinweis:** Der Chat ist noch nicht mit anymize verbunden (`ANYMIZE_API_KEY` fehlt). "
             "Hier sind die passendsten Stellen aus dem Wiki:\n"]
    for n, h in enumerate(hits[:5], 1):
        snippet = " ".join(h["text"].split())[:220]
        lines.append(f"- **{h['title']} › {h['section']}** [{n}]: {snippet}…")
    return "\n".join(lines)


def stream_anymize(messages):
    """Generator über Text-Deltas von anymize (OpenAI-kompatibles Chat-Completions-Format)."""
    body = json.dumps({"model": MODEL, "messages": messages, "stream": True, "temperature": 0.2,
                       "max_tokens": 1200}).encode()
    req = urllib.request.Request(f"{BASE_URL}/chat/completions", data=body, method="POST", headers={
        "Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json", "Accept": "text/event-stream"})
    with urllib.request.urlopen(req, timeout=120) as r:
        if "event-stream" not in r.headers.get("Content-Type", ""):
            data = json.load(r)                                  # Server ignoriert stream=true
            yield data["choices"][0]["message"]["content"] or ""
            return
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload == "[DONE]":
                return
            try:
                chunk = json.loads(payload)
            except json.JSONDecodeError:
                continue
            if chunk.get("error"):
                raise RuntimeError(chunk["error"].get("message", "Fehler vom Modell"))
            for choice in chunk.get("choices", []):
                delta = (choice.get("delta") or {}).get("content")
                if delta:
                    yield delta


def upstream_error(e):
    if isinstance(e, urllib.error.HTTPError):
        detail = ""
        try:
            detail = json.loads(e.read().decode()).get("error", {}).get("message", "")
        except Exception:
            pass
        if e.code == 401:
            return "Der anymize-API-Key ist ungültig oder abgelaufen (401). Bitte ANYMIZE_API_KEY prüfen."
        if e.code == 404:
            return f"Modell oder Endpunkt nicht gefunden (404). Modell: {MODEL}. Verfügbare Modelle: /api/models"
        if e.code == 429:
            return "anymize meldet zu viele Anfragen (429). Bitte kurz warten."
        return f"anymize-Fehler {e.code}: {detail or e.reason}"
    if isinstance(e, urllib.error.URLError):
        return f"anymize nicht erreichbar: {e.reason}"
    return f"Fehler: {e}"


# ---------------------------------------------------------------- HTTP
class Handler(SimpleHTTPRequestHandler):
    server_version = "FahrzeugWiki/1.0"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, fmt, *args):
        sys.stderr.write(f"[{time.strftime('%H:%M:%S')}] {fmt % args}\n")

    # --- CORS für eingebettete Widgets auf freigegebenen Domains
    def cors(self):
        origin = self.headers.get("Origin")
        if origin and origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def end_headers(self):
        self.cors()
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def send_json(self, obj, code=200):
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/site/index.html")
            self.end_headers()
            return
        if path == "/favicon.ico":
            self.path = "/ci/signet.svg"
            return super().do_GET()
        if path == "/api/status":
            return self.send_json({"llm": bool(API_KEY), "model": MODEL, "endpoint": BASE_URL,
                                   "chunks": len(INDEX.chunks), "assistant": "Ampere"})
        if path == "/api/models":
            return self.models()
        if not path.startswith(PUBLIC_PREFIXES) or ".." in path or "/." in path:
            return self.send_error(404)
        return super().do_GET()

    def models(self):
        if not API_KEY:
            return self.send_json({"error": "ANYMIZE_API_KEY fehlt"}, 503)
        req = urllib.request.Request(f"{BASE_URL}/models", headers={"Authorization": f"Bearer {API_KEY}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return self.send_json(json.load(r))
        except Exception as e:
            return self.send_json({"error": upstream_error(e)}, 502)

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/api/chat":
            return self.send_error(404)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY:
                return self.send_json({"error": "Anfrage leer oder zu groß"}, 413)
            payload = json.loads(self.rfile.read(length))
            messages = [{"role": m["role"], "content": str(m["content"])[:MAX_QUESTION * 2]}
                        for m in payload.get("messages", []) if m.get("role") in ("user", "assistant") and m.get("content")]
            if not messages or messages[-1]["role"] != "user":
                return self.send_json({"error": "Letzte Nachricht muss vom Nutzer sein"}, 400)
            if len(messages[-1]["content"]) > MAX_QUESTION:
                return self.send_json({"error": f"Frage zu lang (max. {MAX_QUESTION} Zeichen)"}, 400)
        except (ValueError, KeyError, TypeError):
            return self.send_json({"error": "Ungültiges JSON"}, 400)

        context, sources, hits = retrieve(messages)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        def emit(event, data):
            self.wfile.write(f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n".encode())
            self.wfile.flush()

        try:
            emit("sources", sources)
            if not API_KEY:
                emit("delta", {"text": fallback_answer(hits)})
                emit("done", {"mode": "search-only"})
                return
            try:
                for delta in stream_anymize(build_messages(messages, context)):
                    emit("delta", {"text": delta})
                emit("done", {"mode": "llm", "model": MODEL})
            except (urllib.error.URLError, RuntimeError, KeyError, ValueError) as e:
                emit("error", {"message": upstream_error(e)})
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass  # Nutzer hat abgebrochen


def main():
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    mode = f"anymize ({MODEL})" if API_KEY else "nur Suche (ANYMIZE_API_KEY fehlt)"
    print(f"Fahrzeug-Wiki läuft auf http://localhost:{PORT}  ·  Chat: {mode}  ·  {len(INDEX.chunks)} Abschnitte im Index")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
