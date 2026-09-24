/* Fahrzeug-Wiki · App-Verhalten
 * Schnellsuche (Strg+K), Farbschema, mobile Navigation, Inhaltsverzeichnis, sortier-/filterbare Tabellen, Fahrzeug-Explorer.
 * Funktioniert ohne Server (file://) – der Suchindex kommt aus search.js.
 */
(() => {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const escHtml = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const norm = (s) => String(s ?? "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ß/g, "ss");
  const svg = (p) => `<svg class="i" viewBox="0 0 24 24" aria-hidden="true">${p}</svg>`;
  const ICON = {
    Fahrzeug: svg('<path d="M5 17H3a1 1 0 0 1-1-1v-3.4a2 2 0 0 1 .2-.9l1.6-3.3A2 2 0 0 1 5.6 7h9.2a2 2 0 0 1 1.5.7L19 11l1.8.5A1.6 1.6 0 0 1 22 13v3a1 1 0 0 1-1 1h-2"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M9 17h6"/>'),
    Hersteller: svg('<path d="M2 20V8l6 4V8l6 4V4h8v16a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2Z"/><path d="M7 18h1M12 18h1M17 18h1"/>'),
    Fachbegriff: svg('<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>'),
    "Übersicht": svg('<path d="M3 3v18h18"/><path d="M8 17v-4M13 17V7M18 17v-7"/>'),
    Quelle: svg('<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>'),
    Wiki: svg('<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>'),
    sort: svg('<path d="m7 15 5 5 5-5M7 9l5-5 5 5"/>'),
    sortDir: svg('<path d="M12 5v14M6 13l6 6 6-6"/>'),
    bolt: '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M13.2 2.5 4.8 13.1h5.9l-2.4 8.4 9-11.4h-5.8l1.7-7.6z" fill="currentColor" stroke="none"/></svg>',
  };
  const ask = (q) => {
    const chat = window.FahrzeugWikiChat;
    if (!chat) return alert("Der Chat-Assistent ist nicht geladen. Läuft chat/server.py?");
    q ? chat.ask(q) : chat.open();
  };
  $$("[data-ask]").forEach((b) => b.addEventListener("click", () => ask()));

  // ------------------------------------------------------------ Farbschema
  const themeBtn = $(".theme");
  const mq = matchMedia("(prefers-color-scheme: dark)");
  const effective = () => root.dataset.theme || (mq.matches ? "dark" : "light");
  const syncTheme = () => {
    if (!themeBtn) return;
    const dark = effective() === "dark";
    themeBtn.dataset.mode = dark ? "dark" : "light";
    themeBtn.setAttribute("aria-label", dark ? "Helles Farbschema aktivieren" : "Dunkles Farbschema aktivieren");
    themeBtn.title = themeBtn.getAttribute("aria-label");
  };
  themeBtn?.addEventListener("click", () => {
    const next = effective() === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("fw-theme", next); } catch { /* privater Modus */ }
    syncTheme();
  });
  mq.addEventListener?.("change", syncTheme);
  syncTheme();

  // ------------------------------------------------------------ Mobile Navigation
  const menuBtn = $(".menubtn"), sidebar = $("#sidebar");
  const setNav = (open) => {
    document.body.classList.toggle("nav-open", open);
    menuBtn?.setAttribute("aria-expanded", String(open));
    if (open) setTimeout(() => sidebar.querySelector("[aria-current] , a")?.focus({ preventScroll: true }), 60);
    else menuBtn?.focus();
  };
  menuBtn?.addEventListener("click", () => setNav(!document.body.classList.contains("nav-open")));
  $$("[data-close-nav]").forEach((el) => el.addEventListener("click", () => setNav(false)));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.body.classList.contains("nav-open")) setNav(false);
  });
  // aktiven Eintrag in der Seitenleiste sichtbar machen (ohne die Seite zu scrollen)
  const active = sidebar?.querySelector("[aria-current='page']");
  if (active && sidebar.scrollHeight > sidebar.clientHeight) {
    const top = active.getBoundingClientRect().top - sidebar.getBoundingClientRect().top;
    sidebar.scrollTop = Math.max(0, top - sidebar.clientHeight / 3);
  }

  // ------------------------------------------------------------ Schnellsuche
  const DATA = (window.FW_SEARCH || []).map((e) => ({ ...e, _t: norm(e.t), _x: norm([e.t, e.b, e.d, e.x, e.k].join(" ")) }));
  const pal = $(".palette"), pin = pal?.querySelector("input"), plist = $("#pal-list");
  const ORDER = ["Fahrzeug", "Hersteller", "Fachbegriff", "Übersicht", "Quelle", "Wiki"];
  const SUGGEST = ["fahrzeuguebersicht.html", "datenqualitaet.html", "puffer-analyse.html", "nettokapazitaet.html", "state-of-health.html", "plattform-meb.html"];
  let sel = -1;

  function score(e, toks) {
    let s = 0;
    for (const t of toks) {
      if (e._t.startsWith(t)) s += 100;
      else if (new RegExp("(^|[\\s.\\-/(])" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).test(e._t)) s += 70;
      else if (e._t.includes(t)) s += 45;
      else if (e._x.includes(t)) s += 15;
      else return 0;
    }
    return s + (6 - ORDER.indexOf(e.k));
  }
  function mark(text, toks) {
    let out = escHtml(text);
    toks.filter((t) => t.length > 1).forEach((t) => {
      const re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "i");
      out = out.replace(re, "<mark>$1</mark>");
    });
    return out;
  }
  function itemHtml(e, toks, id) {
    const media = e.i ? `<img src="${escHtml(e.i)}" alt="" loading="lazy">` : `<span class="ic">${ICON[e.k] || ""}</span>`;
    return `<li class="pal-item" role="option" id="${id}" aria-selected="false"><a href="${escHtml(e.u)}">${media}
      <span class="tx"><b>${mark(e.t, toks)}</b><small>${escHtml(e.b ? e.b + " · " : "")}${escHtml(e.d || "")}</small></span>
      <span class="kind">${escHtml(e.k)}</span></a></li>`;
  }
  function renderPalette(q) {
    const toks = norm(q).split(/\s+/).filter(Boolean);
    let html = "";
    let n = 0;
    if (!toks.length) {
      html += `<li class="pal-sec" role="presentation">Vorschläge</li>`;
      SUGGEST.map((u) => DATA.find((e) => e.u === u)).filter(Boolean).forEach((e) => { html += itemHtml(e, [], "po" + n++); });
    } else {
      const hits = DATA.map((e) => [score(e, toks), e]).filter(([s]) => s > 0).sort((a, b) => b[0] - a[0]);
      const groups = {};
      hits.forEach(([, e]) => { (groups[e.k] ||= []).push(e); });
      ORDER.forEach((k) => {
        if (!groups[k]) return;
        html += `<li class="pal-sec" role="presentation">${k === "Übersicht" ? "Übersichten" : k === "Fahrzeug" ? "Fahrzeuge" : k === "Fachbegriff" ? "Fachbegriffe" : k}</li>`;
        groups[k].slice(0, k === "Fahrzeug" ? 8 : 5).forEach((e) => { html += itemHtml(e, toks, "po" + n++); });
      });
      if (!hits.length) {
        html += `<li class="pal-empty" role="presentation"><b>Keine Treffer für „${escHtml(q)}“.</b><br>
          Prüfe die Schreibweise – oder frag Ampere, der Assistent durchsucht auch die Texte.</li>`;
      }
      html += `<li class="pal-sec" role="presentation">Assistent</li>
        <li class="pal-item" role="option" id="po${n++}" aria-selected="false"><button type="button" data-ask-q="${escHtml(q)}">
        <span class="ic ask">${ICON.bolt}</span><span class="tx"><b>Ampere fragen: „${escHtml(q)}“</b>
        <small>Antwort mit Quellen aus dem Wiki</small></span></button></li>`;
    }
    plist.innerHTML = html;
    sel = -1;
    move(0);
  }
  function options() { return $$(".pal-item", plist); }
  function move(to) {
    const opts = options();
    if (!opts.length) { pin.removeAttribute("aria-activedescendant"); return; }
    sel = (to + opts.length) % opts.length;
    opts.forEach((o, i) => o.setAttribute("aria-selected", String(i === sel)));
    pin.setAttribute("aria-activedescendant", opts[sel].id);
    opts[sel].scrollIntoView({ block: "nearest" });
  }
  function openPalette(prefill = "") {
    if (!pal) return;
    if (!pal.open) pal.showModal();
    pin.value = prefill;
    renderPalette(prefill);
    pin.focus();
  }
  $$("[data-open-search]").forEach((b) => b.addEventListener("click", () => openPalette()));
  pal?.addEventListener("click", (e) => { if (e.target === pal) pal.close(); });
  $(".pal-close")?.addEventListener("click", () => pal.close());
  pin?.addEventListener("input", () => renderPalette(pin.value));
  pin?.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") { e.preventDefault(); move(sel + 1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); move(sel - 1); }
    else if (e.key === "Enter") {
      const o = options()[sel];
      if (o) { e.preventDefault(); o.querySelector("a,button").click(); }
    }
  });
  plist?.addEventListener("mousemove", (e) => {
    const o = e.target.closest(".pal-item");
    if (o) { const i = options().indexOf(o); if (i !== sel) move(i); }
  });
  plist?.addEventListener("click", (e) => {
    const b = e.target.closest("[data-ask-q]");
    if (b) { pal.close(); ask(b.dataset.askQ); }
  });
  document.addEventListener("keydown", (e) => {
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName) || document.activeElement?.isContentEditable;
    if ((e.key === "k" || e.key === "K") && (e.ctrlKey || e.metaKey)) { e.preventDefault(); openPalette(); }
    else if (e.key === "/" && !typing && !pal?.open) { e.preventDefault(); openPalette(); }
  });

  // ------------------------------------------------------------ Tabellen: sortieren, filtern, Puffer-Balken
  const num = (t) => {
    const m = t.replace(/ /g, " ").match(/-?\d+(?:[.,]\d+)?/);
    return m ? parseFloat(m[0].replace(",", ".")) : NaN;
  };
  $$(".prose table").forEach((table, ti) => {
    const body = table.tBodies[0];
    if (!body || !table.tHead) return;
    const rows = [...body.rows];
    const wrap = document.createElement("div");
    wrap.className = "table-wrap" + (rows.length > 14 ? " tall" : "");
    wrap.tabIndex = 0;
    wrap.setAttribute("role", "region");
    wrap.setAttribute("aria-label", "Tabelle, horizontal scrollbar");
    table.before(wrap);
    wrap.appendChild(table);
    table.classList.add("enhanced");
    const heads = [...table.tHead.rows[0].cells];

    // Puffer-Balken
    heads.forEach((th, ci) => {
      if (!/^Puffer/i.test(th.textContent.trim())) return;
      rows.forEach((r) => {
        const cell = r.cells[ci];
        const m = cell?.textContent.match(/(-?\d+(?:,\d+)?)\s*%/);
        if (!m) return;
        const p = parseFloat(m[1].replace(",", "."));
        const bar = document.createElement("span");
        bar.className = "pbar" + (p > 12 ? " hi" : p < 1 ? " lo" : "");
        bar.setAttribute("aria-hidden", "true");
        bar.innerHTML = `<i style="width:${Math.max(3, Math.min(100, (p / 20) * 100))}%"></i>`;
        cell.prepend(bar);
      });
    });

    if (rows.length < 4) return;
    // Sortierung
    heads.forEach((th, ci) => {
      const label = escHtml(th.textContent.trim());
      th.innerHTML = `<button type="button" class="sort" title="Nach ${label} sortieren">${label}${ICON.sort}</button>`;
      th.setAttribute("aria-sort", "none");
      th.querySelector("button").addEventListener("click", () => {
        const dir = th.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
        heads.forEach((h) => { h.setAttribute("aria-sort", "none"); h.querySelector(".sort .i").outerHTML = ICON.sort; });
        th.setAttribute("aria-sort", dir);
        th.querySelector(".sort .i").outerHTML = ICON.sortDir;
        const val = (r) => r.cells[ci]?.textContent.trim() ?? "";
        const numeric = rows.every((r) => !val(r) || !isNaN(num(val(r))));
        const sorted = [...rows].sort((a, b) => {
          const x = val(a), y = val(b);
          const c = numeric ? (num(x) || 0) - (num(y) || 0) : x.localeCompare(y, "de", { numeric: true });
          return dir === "ascending" ? c : -c;
        });
        sorted.forEach((r) => body.appendChild(r));
      });
    });

    // Filter für lange Tabellen
    if (rows.length >= 10) {
      const bar = document.createElement("div");
      bar.className = "tbar";
      bar.innerHTML = `<label class="field"><svg class="i" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7.5"/><path d="m20.5 20.5-4.2-4.2"/></svg>
        <span class="sr-only">Tabelle filtern</span><input type="search" placeholder="Tabelle filtern …" autocomplete="off"></label>
        <span class="cnt" aria-live="polite">${rows.length} Zeilen</span>`;
      wrap.before(bar);
      const inp = bar.querySelector("input"), cnt = bar.querySelector(".cnt");
      const empty = document.createElement("tr");
      empty.className = "norows";
      empty.innerHTML = `<td colspan="${heads.length}">Keine Zeile passt zum Filter.</td>`;
      inp.addEventListener("input", () => {
        const toks = norm(inp.value).split(/\s+/).filter(Boolean);
        let n = 0;
        rows.forEach((r) => {
          const ok = toks.every((t) => norm(r.textContent).includes(t));
          r.hidden = !ok;
          if (ok) n++;
        });
        cnt.textContent = toks.length ? `${n} von ${rows.length} Zeilen` : `${rows.length} Zeilen`;
        if (!n) body.appendChild(empty); else empty.remove();
      });
    }
  });

  // ------------------------------------------------------------ Inhaltsverzeichnis: aktiver Abschnitt
  const tocLinks = $$(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    const map = new Map(tocLinks.map((a) => [decodeURIComponent(a.hash.slice(1)), a]));
    const heads = [...map.keys()].map((id) => document.getElementById(id)).filter(Boolean);
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          tocLinks.forEach((a) => a.classList.remove("active"));
          map.get(en.target.id)?.classList.add("active");
        }
      });
    }, { rootMargin: "-70px 0px -70% 0px" });
    heads.forEach((h) => io.observe(h));
  }

  // ------------------------------------------------------------ Fahrzeug-Explorer (Startseite)
  const grid = $("#grid");
  if (grid) {
    const cards = [...grid.children];
    const q = $("#fz-q"), sortSel = $("#fz-sort"), count = $("#fz-count"), empty = $("#fz-empty");
    const chips = $$(".chip");
    let brand = "";
    const params = new URLSearchParams(location.search);
    if (params.get("q")) q.value = params.get("q");
    if (params.get("sort")) sortSel.value = params.get("sort");
    if (params.get("marke")) brand = params.get("marke");
    const cmp = {
      brand: () => 0,
      name: (a, b) => a.dataset.t.localeCompare(b.dataset.t, "de"),
      "netto-desc": (a, b) => b.dataset.n - a.dataset.n,
      "netto-asc": (a, b) => a.dataset.nmin - b.dataset.nmin,
      var: (a, b) => b.dataset.v - a.dataset.v,
    };
    function apply(push = true) {
      const toks = norm(q.value).split(/\s+/).filter(Boolean);
      chips.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.brand === brand)));
      const vis = cards.filter((c) => (!brand || c.dataset.b === brand) && toks.every((t) => norm(c.dataset.s).includes(t)));
      const order = sortSel.value === "brand" ? cards : [...cards].sort(cmp[sortSel.value] || cmp.brand);
      order.forEach((c) => grid.appendChild(c));
      cards.forEach((c) => { c.hidden = !vis.includes(c); });
      count.textContent = vis.length === cards.length ? `${cards.length} Modelle` : `${vis.length} von ${cards.length} Modellen`;
      empty.hidden = vis.length > 0;
      if (push) {
        const p = new URLSearchParams();
        if (q.value.trim()) p.set("q", q.value.trim());
        if (brand) p.set("marke", brand);
        if (sortSel.value !== "brand") p.set("sort", sortSel.value);
        history.replaceState(null, "", location.pathname + (p.toString() ? "?" + p : "") + location.hash);
      }
    }
    chips.forEach((c) => c.addEventListener("click", () => { brand = c.dataset.brand; apply(); }));
    q.addEventListener("input", () => apply());
    sortSel.addEventListener("change", () => apply());
    $("[data-reset]")?.addEventListener("click", () => { q.value = ""; brand = ""; sortSel.value = "brand"; apply(); q.focus(); });
    $("[data-ask-filter]")?.addEventListener("click", () => ask(q.value.trim() || undefined));
    apply(false);
  }
})();
