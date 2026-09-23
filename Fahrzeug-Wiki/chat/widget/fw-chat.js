/*!
 * Fahrzeug-Wiki Chat-Widget („Ampere“) – RAG-Chat über das Fahrzeug-Wiki
 *
 * Einbinden (eine Zeile, beliebige Seite):
 *   <script src="http://localhost:8765/chat/widget/fw-chat.js" defer></script>
 *
 * Optionale data-Attribute am <script>-Tag:
 *   data-api="https://…/api/chat"   Chat-Endpunkt (Standard: gleicher Server wie das Skript)
 *   data-title="Ampere"             Name im Kopf
 *   data-open="true"                beim Laden geöffnet
 *   data-position="left"            Starter links statt rechts
 */
(() => {
  "use strict";
  if (window.__fwChatLoaded) return;
  window.__fwChatLoaded = true;

  const script = document.currentScript;
  const origin = script && script.src ? new URL(script.src, location.href).origin : location.origin;
  const cfg = {
    api: script?.dataset.api || origin + "/api/chat",
    status: (script?.dataset.api ? new URL(script.dataset.api, location.href).origin : origin) + "/api/status",
    title: script?.dataset.title || "Ampere",
    open: script?.dataset.open === "true",
    left: script?.dataset.position === "left",
  };
  const STORE = "fw-chat-v1";
  const SUGGESTIONS = [
    "Wie groß ist die Batterie im VW ID.3?",
    "Was ist der Unterschied zwischen brutto und netto?",
    "Welche Fahrzeuge nutzen LFP-Zellen?",
    "Welche Datenfehler gibt es in der Quelle?",
  ];

  const BOLT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.2 2.5 4.8 13.1h5.9l-2.4 8.4 9-11.4h-5.8l1.7-7.6z" fill="currentColor"/></svg>';
  const SIGNET = '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="15" fill="#0A6B4E"/><rect x="11" y="20" width="36" height="24" rx="5.5" fill="none" stroke="#fff" stroke-width="3.5"/><rect x="48.5" y="27" width="4.5" height="10" rx="1.8" fill="#fff"/><path d="M31.5 23.5 L22.5 34 H28.8 L26.2 40.5 L36 29.8 H29.8 L32.8 23.5 Z" fill="#F4B82E"/></svg>';
  const ICON = {
    close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    reset: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.4-5.7M4 4v4.5h4.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    send: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h14M12 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    stop: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="7" y="7" width="10" height="10" rx="2" fill="currentColor"/></svg>',
  };

  const CSS = `
  :host{all:initial;
    --fw-primary:#0A6B4E;--fw-primary-strong:#064A36;--fw-primary-soft:#E1F0EA;--fw-on-primary:#fff;--fw-accent:#F4B82E;
    --fw-bg:#F6F5F1;--fw-surface:#fff;--fw-surface-2:#EFEDE7;--fw-line:#E2DFD8;--fw-ink:#14171C;--fw-muted:#5B616C;--fw-kritisch:#C23B3B;
    --fw-shadow:0 1px 2px rgba(20,23,28,.06),0 12px 40px rgba(20,23,28,.18);
    --fw-font-text:"Inter","Segoe UI",system-ui,-apple-system,Roboto,sans-serif;--fw-font-display:"Space Grotesk","Segoe UI",system-ui,sans-serif;
    --ease:cubic-bezier(.2,.8,.2,1)}
  @media (prefers-color-scheme:dark){:host{--fw-primary:#45C79B;--fw-primary-strong:#6DD8B2;--fw-primary-soft:#14332A;--fw-on-primary:#0B1F18;
    --fw-bg:#111317;--fw-surface:#1A1D22;--fw-surface-2:#22262C;--fw-line:#2B3037;--fw-ink:#ECEDEF;--fw-muted:#9CA3AE;--fw-kritisch:#F07A7A;
    --fw-shadow:0 1px 2px rgba(0,0,0,.4),0 12px 40px rgba(0,0,0,.5)}}
  *{box-sizing:border-box}
  .wrap{position:fixed;bottom:20px;${cfg.left ? "left" : "right"}:20px;z-index:2147483000;font:15px/1.55 var(--fw-font-text);color:var(--fw-ink)}
  .launcher{width:60px;height:60px;border-radius:50%;border:0;cursor:pointer;background:var(--fw-primary);color:var(--fw-accent);
    box-shadow:var(--fw-shadow);display:grid;place-items:center;transition:transform .16s var(--ease),background .16s}
  .launcher svg{width:30px;height:30px}
  .launcher:hover{background:var(--fw-primary-strong)}
  .launcher:active{transform:scale(.94)}
  .launcher:focus-visible,button:focus-visible,textarea:focus-visible,a:focus-visible{outline:3px solid var(--fw-accent);outline-offset:2px}
  .panel{position:absolute;bottom:76px;${cfg.left ? "left" : "right"}:0;width:390px;height:min(620px,calc(100vh - 110px));
    background:var(--fw-bg);border:1px solid var(--fw-line);border-radius:18px;box-shadow:var(--fw-shadow);display:flex;flex-direction:column;overflow:hidden;
    transform-origin:bottom ${cfg.left ? "left" : "right"};transition:opacity .18s var(--ease),transform .18s var(--ease)}
  .panel[hidden]{display:flex;opacity:0;transform:scale(.96) translateY(8px);pointer-events:none;visibility:hidden}
  header{display:flex;align-items:center;gap:10px;padding:12px 12px 12px 14px;background:var(--fw-surface);border-bottom:1px solid var(--fw-line)}
  header .avatar{width:36px;height:36px;flex:none}
  header .who{flex:1;min-width:0}
  header b{font:600 16px/1.2 var(--fw-font-display);display:block}
  header small{color:var(--fw-muted);font-size:12px;display:flex;align-items:center;gap:6px}
  header small i{width:7px;height:7px;border-radius:50%;background:var(--fw-muted);display:inline-block}
  header small i.on{background:#2FBF7F}
  .icon{width:34px;height:34px;border:0;background:transparent;color:var(--fw-muted);border-radius:8px;cursor:pointer;display:grid;place-items:center}
  .icon:hover{background:var(--fw-surface-2);color:var(--fw-ink)}
  .icon svg{width:18px;height:18px}
  .log{flex:1;overflow-y:auto;padding:16px 14px 8px;scroll-behavior:smooth}
  .msg{display:flex;gap:8px;margin:0 0 14px;animation:in .2s var(--ease)}
  @keyframes in{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
  .msg .avatar{width:26px;height:26px;flex:none;margin-top:2px}
  .bubble{max-width:86%;padding:10px 13px;border-radius:14px;background:var(--fw-surface);border:1px solid var(--fw-line);overflow-wrap:break-word;min-width:0}
  .user{justify-content:flex-end}
  .user .bubble{background:var(--fw-primary);color:var(--fw-on-primary);border-color:transparent;border-bottom-right-radius:4px;white-space:pre-wrap}
  .bot .bubble{border-bottom-left-radius:4px}
  .bubble p{margin:0 0 .6em}.bubble p:last-child{margin-bottom:0}
  .bubble ul,.bubble ol{margin:.2em 0 .6em;padding-left:1.2em}
  .bubble li{margin:.15em 0}
  .bubble code{background:var(--fw-surface-2);padding:1px 5px;border-radius:4px;font-size:.9em}
  .bubble table{border-collapse:collapse;font-size:13px;margin:.4em 0;display:block;overflow-x:auto;font-variant-numeric:tabular-nums}
  .bubble th,.bubble td{border-bottom:1px solid var(--fw-line);padding:3px 8px;text-align:left;white-space:nowrap}
  .bubble th{background:var(--fw-surface-2)}
  .bubble a{color:var(--fw-primary)}
  .cite{font-size:11px;font-weight:600;text-decoration:none;background:var(--fw-primary-soft);color:var(--fw-primary);
    border-radius:4px;padding:0 4px;margin:0 1px;vertical-align:1px}
  .sources{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
  .sources a{font-size:12px;text-decoration:none;color:var(--fw-ink);background:var(--fw-surface-2);border:1px solid var(--fw-line);
    border-radius:999px;padding:3px 10px;max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .sources a:hover{border-color:var(--fw-primary);color:var(--fw-primary)}
  .sources a b{color:var(--fw-primary);margin-right:4px}
  .error{color:var(--fw-kritisch);font-size:13.5px}
  .dots{display:inline-flex;gap:4px;padding:4px 0}
  .dots span{width:7px;height:7px;border-radius:50%;background:var(--fw-muted);animation:blink 1.2s infinite}
  .dots span:nth-child(2){animation-delay:.15s}.dots span:nth-child(3){animation-delay:.3s}
  @keyframes blink{0%,80%,100%{opacity:.25}40%{opacity:1}}
  .chips{display:flex;flex-direction:column;align-items:flex-start;gap:6px;margin:4px 0 12px 34px}
  .chips button{font:inherit;font-size:13.5px;text-align:left;cursor:pointer;background:var(--fw-surface);color:var(--fw-ink);
    border:1px solid var(--fw-line);border-radius:12px;padding:7px 12px;transition:border-color .12s,background .12s}
  .chips button:hover{border-color:var(--fw-primary);background:var(--fw-primary-soft)}
  form{display:flex;gap:8px;align-items:flex-end;padding:10px 12px 12px;background:var(--fw-surface);border-top:1px solid var(--fw-line)}
  textarea{flex:1;resize:none;font:inherit;color:var(--fw-ink);background:var(--fw-bg);border:1px solid var(--fw-line);border-radius:12px;
    padding:10px 12px;max-height:130px;height:42px;line-height:1.4;overflow-y:hidden;scrollbar-width:thin}
  textarea::placeholder{color:var(--fw-muted)}
  .send{width:42px;height:42px;flex:none;border:0;border-radius:12px;background:var(--fw-primary);color:var(--fw-on-primary);cursor:pointer;display:grid;place-items:center}
  .send:hover{background:var(--fw-primary-strong)}
  .send:disabled{opacity:.45;cursor:default}
  .send svg{width:20px;height:20px}
  .foot{font-size:11px;color:var(--fw-muted);text-align:center;padding:0 12px 8px;background:var(--fw-surface)}
  @media (max-width:520px){.wrap{bottom:14px;${cfg.left ? "left" : "right"}:14px}
    .panel{position:fixed;inset:0;width:auto;height:auto;border-radius:0;bottom:0}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
  `;

  // ------------------------------------------------------------ DOM
  const host = document.createElement("div");
  host.id = "fw-chat";
  const root = host.attachShadow({ mode: "open" });
  root.innerHTML = `<style>${CSS}</style>
  <div class="wrap">
    <section class="panel" role="dialog" aria-label="Chat mit ${esc(cfg.title)}" hidden>
      <header>
        <span class="avatar">${SIGNET}</span>
        <div class="who"><b>${esc(cfg.title)}</b><small><i></i><span class="state">Wiki-Assistent</span></small></div>
        <button class="icon reset" title="Neuer Chat" aria-label="Neuer Chat">${ICON.reset}</button>
        <button class="icon close" title="Schließen" aria-label="Chat schließen">${ICON.close}</button>
      </header>
      <div class="log" role="log" aria-live="polite"></div>
      <form>
        <textarea rows="1" placeholder="Fahrzeug oder Begriff fragen …" aria-label="Nachricht"></textarea>
        <button class="send" type="submit" aria-label="Senden">${ICON.send}</button>
      </form>
      <div class="foot">Antworten basieren auf dem Fahrzeug-Wiki · Quellen prüfen</div>
    </section>
    <button class="launcher" aria-label="Chat mit ${esc(cfg.title)} öffnen" aria-expanded="false">${BOLT}</button>
  </div>`;
  (document.body ? Promise.resolve() : new Promise((r) => addEventListener("DOMContentLoaded", r))).then(() =>
    document.body.appendChild(host));

  const $ = (s) => root.querySelector(s);
  const panel = $(".panel"), log = $(".log"), form = $("form"), input = $("textarea"), sendBtn = $(".send"),
    launcher = $(".launcher"), stateEl = $(".state"), dot = $("header small i");

  let history = load();
  let controller = null;

  // ------------------------------------------------------------ Hilfen
  function esc(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
  function load() {
    try { return JSON.parse(sessionStorage.getItem(STORE)) || []; } catch { return []; }
  }
  function save() {
    try { sessionStorage.setItem(STORE, JSON.stringify(history.slice(-20))); } catch { /* privater Modus */ }
  }
  function safeUrl(u) {
    return /^(https?:\/\/|\/)/.test(u) ? u : "#";
  }

  // Kleines, sicheres Markdown: erst escapen, dann Formatierung
  function inline(s, sources) {
    return s
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>")
      .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, t, u) => `<a href="${safeUrl(u)}" target="_blank" rel="noopener">${t}</a>`)
      .replace(/\[(\d{1,2})\]/g, (m, n) => {
        const src = sources[n - 1];
        return src ? `<a class="cite" href="${safeUrl(src.url)}" target="_blank" rel="noopener" title="${esc(src.title + " › " + src.section)}">${n}</a>` : m;
      });
  }
  function markdown(text, sources = []) {
    const lines = esc(text).split("\n");
    let html = "", list = null, para = [], table = [];
    const flushPara = () => { if (para.length) { html += `<p>${inline(para.join("<br>"), sources)}</p>`; para = []; } };
    const flushList = () => { if (list) { html += `</${list}>`; list = null; } };
    const flushTable = () => {
      if (!table.length) return;
      const rows = table.filter((r) => !/^\|?[\s:|-]+\|?$/.test(r)).map((r) => r.replace(/^\||\|$/g, "").split("|"));
      html += "<table>" + rows.map((c, i) => "<tr>" + c.map((x) => `<${i ? "td" : "th"}>${inline(x.trim(), sources)}</${i ? "td" : "th"}>`).join("") + "</tr>").join("") + "</table>";
      table = [];
    };
    for (const raw of lines) {
      const line = raw.trimEnd();
      if (/^\s*\|.*\|\s*$/.test(line)) { flushPara(); flushList(); table.push(line.trim()); continue; }
      flushTable();
      const ul = line.match(/^\s*[-*•]\s+(.*)/), ol = line.match(/^\s*\d+[.)]\s+(.*)/), h = line.match(/^#{1,4}\s+(.*)/);
      if (ul || ol) {
        flushPara();
        const tag = ul ? "ul" : "ol";
        if (list !== tag) { flushList(); html += `<${tag}>`; list = tag; }
        html += `<li>${inline((ul || ol)[1], sources)}</li>`;
      } else if (h) { flushPara(); flushList(); html += `<p><strong>${inline(h[1], sources)}</strong></p>`; }
      else if (!line.trim()) { flushPara(); flushList(); }
      else { flushList(); para.push(line); }
    }
    flushPara(); flushList(); flushTable();
    return html;
  }

  // ------------------------------------------------------------ Darstellung
  function addMessage(role, content = "", sources = []) {
    const el = document.createElement("div");
    el.className = `msg ${role === "user" ? "user" : "bot"}`;
    el.innerHTML = role === "user" ? `<div class="bubble"></div>` : `<span class="avatar">${SIGNET}</span><div class="bubble"></div>`;
    const bubble = el.querySelector(".bubble");
    if (role === "user") bubble.textContent = content;
    else render(bubble, content, sources);
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return bubble;
  }
  function render(bubble, content, sources, error) {
    const cited = new Set([...content.matchAll(/\[(\d{1,2})\]/g)].map((m) => +m[1]));
    const shown = sources.filter((s) => cited.has(s.n));
    const list = (shown.length ? shown : sources.slice(0, 3));
    bubble.innerHTML = (content ? markdown(content, sources) : `<span class="dots" aria-label="Ampere schreibt"><span></span><span></span><span></span></span>`) +
      (error ? `<p class="error">${esc(error)}</p>` : "") +
      (content && list.length ? `<div class="sources">${list.map((s) =>
        `<a href="${safeUrl(s.url)}" target="_blank" rel="noopener" title="${esc(s.title + " › " + s.section)}"><b>${s.n}</b>${esc(s.title)}</a>`).join("")}</div>` : "");
  }
  function welcome() {
    log.innerHTML = "";
    addMessage("assistant", `Hallo, ich bin **${cfg.title}**. Ich beantworte Fragen zu allen Fahrzeugen, Batterien und Fachbegriffen im Fahrzeug-Wiki – mit Quellenangabe.`);
    const chips = document.createElement("div");
    chips.className = "chips";
    SUGGESTIONS.forEach((q) => {
      const b = document.createElement("button");
      b.type = "button"; b.textContent = q;
      b.onclick = () => { chips.remove(); send(q); };
      chips.appendChild(b);
    });
    log.appendChild(chips);
  }
  function restore() {
    if (!history.length) return welcome();
    log.innerHTML = "";
    history.forEach((m) => addMessage(m.role, m.content, m.sources || []));
  }

  // ------------------------------------------------------------ Senden (SSE über fetch)
  async function send(text) {
    text = text.trim();
    if (!text || controller) return;
    root.querySelector(".chips")?.remove();
    addMessage("user", text);
    history.push({ role: "user", content: text });
    save();
    input.value = ""; autosize();
    const bubble = addMessage("assistant", "");
    let answer = "", sources = [], error = "";
    controller = new AbortController();
    setBusy(true);
    try {
      const res = await fetch(cfg.api, {
        method: "POST", headers: { "Content-Type": "application/json" }, signal: controller.signal,
        body: JSON.stringify({ messages: history.map(({ role, content }) => ({ role, content })) }),
      });
      if (!res.ok || !res.body) {
        const j = await res.json().catch(() => ({}));
        throw new Error(j.error || `Serverfehler ${res.status}`);
      }
      const reader = res.body.getReader(), dec = new TextDecoder();
      let buf = "";
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        let i;
        while ((i = buf.indexOf("\n\n")) >= 0) {
          const block = buf.slice(0, i); buf = buf.slice(i + 2);
          const ev = (block.match(/^event: (.*)$/m) || [])[1];
          const data = JSON.parse((block.match(/^data: (.*)$/m) || [, "null"])[1]);
          if (ev === "sources") sources = data;
          else if (ev === "delta") { answer += data.text; render(bubble, answer, sources); stick(); }
          else if (ev === "error") error = data.message;
        }
      }
    } catch (e) {
      if (e.name !== "AbortError") error = e.message === "Failed to fetch" ? "Server nicht erreichbar. Läuft chat/server.py?" : e.message;
    } finally {
      controller = null;
      setBusy(false);
      if (!answer && !error) error = "Abgebrochen.";
      render(bubble, answer, sources, error);
      if (answer) { history.push({ role: "assistant", content: answer, sources }); save(); }
      else { history.pop(); save(); }
      stick();
      input.focus();
    }
  }
  function stick() {
    if (log.scrollHeight - log.scrollTop - log.clientHeight < 120) log.scrollTop = log.scrollHeight;
  }
  function setBusy(busy) {
    sendBtn.innerHTML = busy ? ICON.stop : ICON.send;
    sendBtn.setAttribute("aria-label", busy ? "Antwort stoppen" : "Senden");
    sendBtn.type = busy ? "button" : "submit";
  }
  function autosize() {
    input.style.height = "42px";
    const h = Math.min(input.scrollHeight + 2, 130);
    input.style.height = h + "px";
    input.style.overflowY = input.scrollHeight + 2 > 130 ? "auto" : "hidden";
  }

  // ------------------------------------------------------------ Ereignisse
  function toggle(open = panel.hidden) {
    panel.hidden = !open;
    launcher.setAttribute("aria-expanded", String(open));
    launcher.setAttribute("aria-label", open ? "Chat schließen" : `Chat mit ${cfg.title} öffnen`);
    if (open) { if (!log.children.length) restore(); setTimeout(() => input.focus(), 50); }
  }
  launcher.onclick = () => toggle();
  $(".close").onclick = () => { toggle(false); launcher.focus(); };
  $(".reset").onclick = () => { controller?.abort(); history = []; save(); welcome(); input.focus(); };
  sendBtn.onclick = (e) => { if (controller) { e.preventDefault(); controller.abort(); } };
  form.onsubmit = (e) => { e.preventDefault(); send(input.value); };
  input.addEventListener("input", autosize);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); send(input.value); }
  });
  root.addEventListener("keydown", (e) => { if (e.key === "Escape" && !panel.hidden) { toggle(false); launcher.focus(); } });

  fetch(cfg.status).then((r) => r.json()).then((s) => {
    stateEl.textContent = s.llm ? `Wiki-Assistent · ${s.model}` : "Wiki-Assistent · nur Suche";
    dot.classList.toggle("on", !!s.llm);
  }).catch(() => { stateEl.textContent = "Wiki-Assistent · offline"; });

  if (cfg.open) toggle(true);
  window.FahrzeugWikiChat = { open: () => toggle(true), close: () => toggle(false), ask: (q) => { toggle(true); send(q); } };
})();
