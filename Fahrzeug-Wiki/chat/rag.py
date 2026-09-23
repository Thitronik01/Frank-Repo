"""RAG-Retrieval über das Fahrzeug-Wiki – ohne externe Abhängigkeiten.

anymize bietet keinen Embeddings-Endpunkt; deshalb lexikalische Suche (BM25) mit deutscher Normalisierung.
Für 150 Seiten mit vielen Eigennamen (ID.3, EQA 250+, 77,0 kWh) ist das präzise und schnell.

  python chat/rag.py build                 # Index neu bauen  -> chat/index.json
  python chat/rag.py "Akku vom ID.3?"      # Suche testen
"""
import json
import math
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = Path(__file__).resolve().parent / "index.json"
SOURCES = [("wiki/entities/fahrzeuge", "Fahrzeug"), ("wiki/entities/hersteller", "Hersteller"),
           ("wiki/concepts", "Fachbegriff"), ("wiki/synthesis", "Übersicht"), ("wiki/sources", "Quelle")]
MAX_CHARS = 1600

STOP = set("""der die das den dem des ein eine einer eines einem einen und oder aber auch als an auf aus bei bis
durch fuer gegen im in ins ist sind war waren wird werden wurde wurden mit nach ohne ueber um unter von vor zu zum zur
nicht nur noch schon sehr so wie was wer wo wann warum welche welcher welches wieviel viel viele es er sie ich du wir ihr
man hat haben hatte kann koennen muss soll sich sein seine ihre dies diese dieser dieses dass denn doch mal gibt
bitte mir mich dir dich uns euch am vom beim hier da dann""".split())


# ---------------------------------------------------------------- Text-Normalisierung
def fold(text):
    t = text.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c))


def stem(tok):
    if tok.isdigit() or len(tok) <= 4:
        return tok
    for suf in ("ungen", "ung", "en", "er", "es", "e", "n", "s"):
        if tok.endswith(suf) and len(tok) - len(suf) >= 4:
            return tok[: -len(suf)]
    return tok


def tokenize(text):
    t = fold(text)
    t = re.sub(r"(\d),(\d)", r"\1.\2", t)               # 77,0 -> 77.0
    # Modellcodes zusätzlich zusammengezogen: ID.3 / EV-6 / Model 3 -> id3 / ev6 / model3
    out = [a + b for a, b in re.findall(r"\b([a-z]{1,5})[.\- ](\d{1,3})\b(?!\.\d)", t) if a not in STOP]
    for tok in re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", t):
        if tok in STOP:
            continue
        if re.fullmatch(r"\d+\.0", tok):
            tok = tok[:-2]                              # 77.0 == 77
        out.append(stem(tok))
    return out


# ---------------------------------------------------------------- Chunking
LINK = re.compile(r"\[\[([^\]|\\]+)(?:\\?\|([^\]]+))?\]\]")


def clean(md):
    md = re.sub(r"!\[\[[^\]]+\]\]", "", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)                       # Bilder
    md = re.sub(r"^\*Bild:.*$", "", md, flags=re.M)                    # Bildnachweis
    md = LINK.sub(lambda m: m.group(2) or m.group(1), md)
    md = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"^\|[-| :]+\|$", "", md, flags=re.M)                   # Tabellentrenner
    md = re.sub(r"<[^>]+>", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def split_long(text, limit=MAX_CHARS):
    if len(text) <= limit:
        return [text]
    parts, cur = [], ""
    header = next((ln for ln in text.split("\n") if ln.startswith("|")), "")
    for ln in text.split("\n"):
        if len(cur) + len(ln) > limit and cur:
            parts.append(cur.strip())
            cur = (header + "\n") if ln.startswith("|") and header and ln != header else ""
        cur += ln + "\n"
    if cur.strip():
        parts.append(cur.strip())
    return parts


def page_chunks(path, kind):
    raw = path.read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"\A---\n(.*?)\n---\n", raw, re.S)
    if m:
        for ln in m.group(1).splitlines():
            k, _, v = ln.partition(":")
            meta[k.strip()] = v.strip().strip('"')
        raw = raw[m.end():]
    title = re.search(r"^# (.+)$", raw, re.M).group(1).strip()
    facts = " · ".join(f"{k}: {meta[k]}" for k in ("hersteller", "segment", "plattform", "bauzeit") if meta.get(k))
    sections = re.split(r"^## ", raw, flags=re.M)
    chunks = []
    intro = clean(re.sub(r"^# .+$", "", sections[0], flags=re.M))
    if intro or facts:
        chunks.append(("Überblick", (facts + "\n" + intro).strip()))
    for sec in sections[1:]:
        head, _, body = sec.partition("\n")
        if head.strip() in ("Quellen", "Belege"):
            continue
        body = clean(body)
        if body:
            for part in split_long(body):
                chunks.append((head.strip(), part))
    return [{"slug": path.stem, "title": title, "kind": kind, "section": h, "text": t,
             "url": f"/site/{path.stem}.html"} for h, t in chunks]


# ---------------------------------------------------------------- BM25
class Index:
    def __init__(self, chunks):
        self.chunks = chunks
        self.docs = []
        for c in chunks:
            # Titel doppelt gewichten, Abschnittsname einfach
            toks = tokenize(c["title"]) * 3 + tokenize(c["section"]) + tokenize(c["text"])
            self.docs.append(Counter(toks))
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / len(self.lens)
        df = Counter(t for d in self.docs for t in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.title_toks = [set(tokenize(c["title"])) for c in chunks]
        self.vocab = sorted(df)

    def expand(self, terms):
        """Komposita: 'brutto' trifft auch 'bruttokapazitaet' (halbes Gewicht)."""
        extra = []
        for t in terms:
            if len(t) >= 5 and not t.isdigit():
                extra += [v for v in self.vocab if v != t and v.startswith(t)][:8]
        return [x for x in dict.fromkeys(extra) if x not in terms]

    def search(self, query, k=6, history=""):
        q = tokenize(query)
        qh = [t for t in tokenize(history) if t not in q]   # Kontext aus Vorfragen, schwächer gewichtet
        if not q and not qh:
            return []
        qx = self.expand(q)
        # Definitionsfragen bevorzugen Fachbegriff-Artikel
        definitional = re.search(r"(was (ist|sind|bedeutet|heisst|versteht)|unterschied|erklae?r|definition|bedeutung)",
                                 fold(query)) is not None
        scores = []
        k1, b = 1.4, 0.75
        for i, d in enumerate(self.docs):
            s = 0.0
            for weight, terms in ((1.0, q), (0.8, qx), (0.35, qh)):
                for t in terms:
                    f = d.get(t)
                    if f:
                        s += weight * self.idf[t] * f * (k1 + 1) / (f + k1 * (1 - b + b * self.lens[i] / self.avg))
            # Bonus, wenn die Frage das Fahrzeug/den Begriff im Titel nennt
            hit = len(self.title_toks[i] & set(q)) + 1.0 * len(self.title_toks[i] & set(qx))
            if hit:
                s *= 1 + 0.5 * hit
            if definitional and self.chunks[i]["kind"] == "Fachbegriff":
                s *= 2.2
            if s > 0:
                scores.append((s, i))
        scores.sort(reverse=True)
        out, per_page = [], Counter()
        for s, i in scores:
            c = self.chunks[i]
            if per_page[c["slug"]] >= 3:
                continue
            per_page[c["slug"]] += 1
            out.append({**c, "score": round(s, 2)})
            if len(out) == k:
                break
        return out


def build():
    chunks = []
    for folder, kind in SOURCES:
        for p in sorted((ROOT / folder).glob("*.md")):
            chunks.extend(page_chunks(p, kind))
    INDEX.write_text(json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
    print(f"{len(chunks)} Abschnitte aus {len({c['slug'] for c in chunks})} Seiten -> {INDEX}")


def load():
    if not INDEX.exists():
        build()
    return Index(json.loads(INDEX.read_text(encoding="utf-8")))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build()
    elif len(sys.argv) > 1:
        for r in load().search(" ".join(sys.argv[1:])):
            print(f"{r['score']:7.2f}  {r['title']} › {r['section']}")
    else:
        print(__doc__)
