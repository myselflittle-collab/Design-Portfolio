/* ButterSkin prototype. Fictional concept; all content comes from assets/data.js (generated from data/products.json).
   Routes use the URL hash so any screen or state can be opened directly, e.g. #/discover?cat=treat or #/shelf?demo=empty. */
(function () {
  "use strict";
  const D = window.BS_DATA;
  const P = Object.fromEntries(D.products.map(p => [p.id, p]));
  const CAT = Object.fromEntries(D.categories.map(c => [c.id, c]));
  const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  /* ---------- session state (in memory only; nothing is stored or sent) ---------- */
  const fresh = () => ({
    done: { AM: new Set(D.routines.demo_done_AM), PM: new Set() },
    saved: new Set(D.demo_saved),
    journal: D.journal.map(j => Object.assign({}, j)),
    profile: { skin_type: D.user.skin_type, focus: D.user.focus },
    checkin: null
  });
  let S = fresh();

  /* ---------- helpers ---------- */
  const $ = (sel, el) => (el || document).querySelector(sel);
  const $$ = (sel, el) => [...(el || document).querySelectorAll(sel)];
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const icon = (n, label) => `<svg class="ic" aria-hidden="true"${label ? "" : ""}><use href="#i-${n}"/></svg>`;
  const price = n => "₹" + n.toLocaleString("en-IN");
  const fmtDate = iso => { const [y, m, d] = iso.split("-").map(Number); return `${d} ${MONTHS[m - 1]}`; };
  const pack = (p, alt) => `<img src="assets/packaging/${p.id}.svg" alt="${alt ? esc(p.name + ", fictional concept packaging") : ""}">`;

  function toast(msg) {
    const t = $("#toast"); t.textContent = msg; t.classList.add("show");
    clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove("show"), 2600);
  }

  function parse() {
    const h = location.hash.replace(/^#/, "") || "/welcome/1";
    const [path, qs] = h.split("?");
    return { path, parts: path.split("/").filter(Boolean), q: new URLSearchParams(qs || "") };
  }
  const go = h => { location.hash = h; };
  const parseHash = h => { const [p, q] = (h || "").replace(/^#/, "").split("?"); return { path: p, parts: (p || "").split("/").filter(Boolean), q: new URLSearchParams(q || "") }; };
  const keyOf = r => (r.parts[0] === "journal" && r.parts[1] === "new") ? "journalNew" : (r.parts[0] || "welcome");

  /* ---------- reusable pieces ---------- */
  function productCard(p) {
    const saved = S.saved.has(p.id);
    return `<article class="pcard">
      <a class="open" href="#/product/${p.id}" aria-label="${esc(p.name)}, ${price(p.price)}. View details">
        <div class="shot bg-${p.category}">${pack(p)}</div></a>
      <div class="info"><span class="cat">${esc(CAT[p.category].name)} · ${esc(p.size)}</span>
        <span class="name">${esc(p.name)}</span>
        <div class="meta"><span class="price">${price(p.price)}</span>
          <button class="save" data-save="${p.id}" aria-pressed="${saved}" aria-label="${saved ? "Remove " + esc(p.name) + " from shelf" : "Save " + esc(p.name) + " to shelf"}">${icon("heart")}</button></div></div>
    </article>`;
  }

  function empty(title, text, action, href, art) {
    return `<div class="empty"><div class="art">${art ? pack(P[art]) : ""}</div>
      <h2 class="h3">${title}</h2><p class="muted small" style="max-width:360px;margin:8px auto 18px">${text}</p>
      ${action ? `<a class="btn ghost" href="${href}">${action}</a>` : ""}</div>`;
  }

  /* ---------- screens ---------- */
  const SCREENS = {};

  SCREENS.welcome = r => {
    const n = Math.min(3, Math.max(1, Number(r.parts[1] || 1)));
    const slides = [
      { bg: "bg-moisturise", art: ["cloud-milk-cleanser", "butter-balm-cream", "daylight-spf-50"], eyebrow: "Welcome to ButterSkin",
        h: "Your skin, understood.", p: "A calm place to keep a simple routine, find everyday essentials and notice how your skin feels. No pressure, no perfection." },
      { bg: "bg-cleanse", art: ["soft-gel-cleanser", "dewdrop-hydration-serum", "soft-cloud-moisturiser"], eyebrow: "Small steps",
        h: "Skipping a step is fine.", p: "Routines are checklists, not scores. There are no streaks to keep and nothing to lose if you miss a day." },
      { bg: "bg-treat", art: ["still-water-essence", "quiet-night-oil", "butter-balm-cream"], eyebrow: "Honest by design",
        h: "Personal, not prescriptive.", p: "Your notes and preferences shape what you see. ButterSkin never diagnoses skin or promises results. This is a fictional concept app." }
    ][n - 1];
    return { title: `Welcome ${n} of 3`, full: true, html: `
      <div class="onb"><div class="visual ${slides.bg}" aria-hidden="true">${slides.art.map(id => `<img src="assets/packaging/${id}-scene.svg" alt="">`).join("")}</div>
      <div class="copy"><img src="assets/logo-lockup.svg" alt="ButterSkin" style="height:34px;width:auto;align-self:flex-start">
        <div class="eyebrow" style="margin-top:12px">${slides.eyebrow}</div><h1 tabindex="-1">${slides.h}</h1><p class="lede">${slides.p}</p>
        <div class="dots" role="img" aria-label="Step ${n} of 3">${[1, 2, 3].map(i => `<i class="${i === n ? "on" : ""}"></i>`).join("")}</div>
        <div class="row" style="margin-top:12px;flex-wrap:wrap">
          <a class="btn primary" href="${n < 3 ? "#/welcome/" + (n + 1) : "#/setup"}">${n < 3 ? "Continue" : "Set up my space"}</a>
          <a class="btn text" href="#/home">Skip to the app</a></div>
        <p class="cap muted" style="margin-top:8px">Concept app · fictional products and people · not medical advice</p></div></div>` };
  };

  SCREENS.setup = () => ({ title: "Set up", full: true, html: `
    <div class="page" style="max-width:640px;padding:32px 18px 48px">
      <img src="assets/logo-lockup.svg" alt="ButterSkin" style="height:30px;width:auto">
      <div class="eyebrow" style="margin-top:28px">A starting point</div><h1 tabindex="-1">Tell us a little about your skin</h1>
      <p class="lede">Optional. This only changes which products appear first. It is not a diagnosis, and you can change it any time.</p>
      <form id="setupForm" class="card" style="margin-top:22px" novalidate>
        ${radioGroup("skin_type", "Skin type", D.user.skin_types, S.profile.skin_type)}
        ${radioGroup("focus", "What would you like to focus on?", D.user.focus_options, S.profile.focus)}
        <div class="row" style="flex-wrap:wrap"><button class="btn primary" type="submit">Continue</button>
          <a class="btn text" href="#/home">Skip for now</a></div></form></div>` });

  function radioGroup(name, legend, options, value) {
    return `<fieldset><legend>${legend}</legend><div class="chips">${options.map(o =>
      `<label class="radio-chip"><input type="radio" name="${name}" value="${esc(o)}"${o === value ? " checked" : ""}><span>${esc(o)}</span></label>`).join("")}</div></fieldset>`;
  }

  SCREENS.home = () => {
    const am = D.routines.AM, done = am.filter(s => S.done.AM.has(s.id)).length;
    const picks = D.products.filter(p => p.focus.includes(S.profile.focus)).slice(0, 4);
    const next = am.find(s => !S.done.AM.has(s.id));
    return { title: "Home", nav: "home", html: `
      <div class="between" style="align-items:flex-end;flex-wrap:wrap">
        <div><div class="eyebrow">${D.demo_weekday}, ${fmtDate(D.demo_date)}</div><h1 tabindex="-1">Good morning, ${esc(D.user.name)}</h1>
          <p class="lede">A softer routine starts with small, thoughtful steps.</p></div></div>
      <section class="hero" style="margin-top:22px" aria-labelledby="todayH">
        <div><div class="eyebrow">Today · morning</div><h2 id="todayH" style="margin:6px 0 10px">${done} of ${am.length} steps done</h2>
          <div class="progress" role="img" aria-label="${done} of ${am.length} morning steps done"><span style="width:${done / am.length * 100}%"></span></div>
          <p class="small" style="color:var(--bs-text-secondary);margin:12px 0 16px">${next ? "Next: " + esc(next.name) + ". Skipping a step is fine." : "Morning steps are done for today."}</p>
          <a class="btn primary" href="#/routine">Open my routine ${icon("arrow")}</a></div>
        <div class="art" aria-hidden="true">${["dewdrop-hydration-serum", "soft-cloud-moisturiser", "daylight-spf-50"].map(id => `<img src="assets/packaging/${id}-scene.svg" alt="">`).join("")}</div>
      </section>
      <div class="grid2" style="margin-top:18px">
        <section class="card" aria-labelledby="ciH"><h2 id="ciH" class="h3">How does your skin feel today?</h2>
          <p class="small muted" style="margin:6px 0 14px">One tap adds a note to your journal. Nothing is scored.</p>
          <div class="chips" role="group" aria-labelledby="ciH">${D.moods.map(m => `<button class="chip" data-checkin="${esc(m)}" aria-pressed="${S.checkin === m}">${esc(m)}</button>`).join("")}</div></section>
        <section class="card" aria-labelledby="shH"><div class="between"><h2 id="shH" class="h3">Your shelf</h2><a class="btn text" href="#/shelf">Open shelf</a></div>
          <p class="small muted" style="margin:6px 0 14px">${S.saved.size ? S.saved.size + " saved product" + (S.saved.size > 1 ? "s" : "") + " to look at again." : "Nothing saved yet."}</p>
          <div class="row">${[...S.saved].slice(0, 3).map(id => `<div class="thumb bg-${P[id].category}">${pack(P[id])}</div>`).join("")}</div></section>
      </div>
      <div class="section-h"><h2>For a ${esc(S.profile.focus.toLowerCase())} focus</h2><a href="#/discover?focus=1">See all</a></div>
      <div class="rail">${picks.map(productCard).join("")}</div>` };
  };

  SCREENS.routine = r => {
    const t = r.q.get("time") === "PM" ? "PM" : "AM";
    const list = D.routines[t], done = list.filter(s => S.done[t].has(s.id)).length;
    return { title: "My routine", nav: "routine", html: `
      <div class="eyebrow">Your daily ritual</div><h1 tabindex="-1">Small steps, softer days.</h1>
      <p class="lede">Tick what you did. Skipped steps are not counted against you, and nothing carries over to tomorrow.</p>
      <div class="between" style="margin:22px 0 14px;flex-wrap:wrap">
        <div class="tabs" role="tablist" aria-label="Time of day">
          <a role="tab" href="#/routine" aria-selected="${t === "AM"}" ${t === "AM" ? 'aria-current="true"' : ""}>${icon("sun")}Morning</a>
          <a role="tab" href="#/routine?time=PM" aria-selected="${t === "PM"}" ${t === "PM" ? 'aria-current="true"' : ""}>${icon("moon")}Evening</a></div>
        <span class="pill ${done === list.length ? "done" : ""}" aria-live="polite">${done} of ${list.length} done</span></div>
      <section class="card" role="tabpanel" aria-label="${t === "AM" ? "Morning" : "Evening"} steps">
        <ul class="steps">${list.map(s => {
          const p = s.product ? P[s.product] : null, on = S.done[t].has(s.id);
          return `<li class="step"><span class="check"><input type="checkbox" id="c-${s.id}" data-step="${s.id}" data-time="${t}"${on ? " checked" : ""}><span class="box" aria-hidden="true">${icon("check")}</span></span>
            <div class="thumb ${p ? "bg-" + p.category : "pause"}" aria-hidden="true">${p ? pack(p) : icon("leaf")}</div>
            <div><label class="t" for="c-${s.id}">${esc(s.name)}${s.optional ? ' <span class="cap muted">(optional)</span>' : ""}</label>
              <div class="s">${p ? `<a href="#/product/${p.id}">${esc(p.name)}</a>` : "A moment for yourself"}</div></div>
            <span class="pill">${s.minutes} min</span></li>`;
        }).join("")}</ul></section>
      <div class="row" style="margin-top:16px;flex-wrap:wrap;gap:16px">
        <p class="small muted" style="margin:0;flex:1;min-width:240px">${done === list.length ? "All done for this " + (t === "AM" ? "morning" : "evening") + ". Nice and easy." : "Do what feels right today."}</p>
        <button class="btn ghost" data-reset="${t}">Clear today's ticks</button></div>` };
  };

  SCREENS.discover = r => {
    const cat = r.q.get("cat") || "all", q = (r.q.get("q") || "").trim(), focus = r.q.get("focus") === "1";
    const res = D.products.filter(p => (cat === "all" || p.category === cat) && (!focus || p.focus.includes(S.profile.focus)) &&
      (!q || (p.name + " " + p.about + " " + p.ingredients.map(i => i[0]).join(" ")).toLowerCase().includes(q.toLowerCase())));
    const qs = (o) => { const u = new URLSearchParams({ cat, q, focus: focus ? "1" : "" }); Object.entries(o).forEach(([k, v]) => u.set(k, v));
      [...u.keys()].forEach(k => { if (!u.get(k) || u.get(k) === "all") u.delete(k); }); const s = u.toString(); return "#/discover" + (s ? "?" + s : ""); };
    return { title: "Discover", nav: "discover", html: `
      <div class="eyebrow">The ButterSkin edit</div><h1 tabindex="-1">Find your kind of gentle.</h1>
      <p class="lede">Eight fictional essentials. Each one shows where it fits in a routine, never what it will "fix".</p>
      <form class="search" role="search" style="margin-top:22px" data-search>
        <label class="sr" for="q">Search products and ingredients</label>${icon("search")}
        <input class="input" id="q" name="q" type="search" value="${esc(q)}" placeholder="Search products or ingredients" autocomplete="off"></form>
      <div class="between" style="margin:14px 0 18px;flex-wrap:wrap">
        <div class="chips" role="group" aria-label="Category">${[["all", "All"]].concat(D.categories.map(c => [c.id, c.name])).map(([id, n]) =>
          `<a class="chip" href="${qs({ cat: id })}" aria-pressed="${cat === id}" role="button">${n}</a>`).join("")}</div>
        <a class="switch" role="switch" aria-checked="${focus}" href="${qs({ focus: focus ? "" : "1" })}"><span class="track" aria-hidden="true"></span>Suits my ${esc(S.profile.focus.toLowerCase())} focus</a></div>
      <p class="small muted" aria-live="polite" style="margin:0 0 12px">${res.length} product${res.length === 1 ? "" : "s"}${q ? ` for “${esc(q)}”` : ""}</p>
      ${res.length ? `<div class="pgrid">${res.map(productCard).join("")}</div>` :
        `<div class="card">${empty("Nothing matches yet", `No concept products match${q ? " “" + esc(q) + "”" : ""} with these filters. Try another word or clear the filters.`, "Clear filters", "#/discover", "still-water-essence")}</div>`}` };
  };

  SCREENS.shelf = r => {
    const ids = r.q.get("demo") === "empty" ? [] : [...S.saved];
    return { title: "Your shelf", nav: "home", html: `
      <div class="eyebrow">Saved for later</div><h1 tabindex="-1">Your shelf</h1>
      <p class="lede">Products you want to look at again. Saving is not buying, and nothing here is a recommendation.</p>
      <div style="margin-top:22px">${ids.length ? `<div class="pgrid">${ids.map(id => productCard(P[id])).join("")}</div>` :
        `<div class="card">${empty("Your shelf is empty", "Tap the heart on any product to keep it here while you think.", "Browse products", "#/discover", "butter-balm-cream")}</div>`}</div>` };
  };

  SCREENS.journal = r => {
    const list = r.q.get("demo") === "empty" ? [] : S.journal;
    return { title: "Skin journal", nav: "journal", html: `
      <div class="between" style="align-items:flex-end;flex-wrap:wrap"><div><div class="eyebrow">Notice, don't judge</div><h1 tabindex="-1">Skin journal</h1>
        <p class="lede">Short notes about how your skin felt. Only you see them, and they are never scored.</p></div>
        <a class="btn primary" href="#/journal/new">${icon("plus")}New note</a></div>
      <section class="card" style="margin-top:22px" aria-label="Journal entries">${list.length ? list.map(j => `
        <article class="entry"><div class="d">${fmtDate(j.date).split(" ")[0]}<small>${fmtDate(j.date).split(" ")[1]}</small></div>
          <div><span class="pill">${esc(j.mood)}</span><p style="margin:8px 0 0">${esc(j.note)}</p></div></article>`).join("") :
        empty("No notes yet", "When you feel like it, jot down a line about your skin. Patterns are easier to notice over time.", "Write a first note", "#/journal/new", "quiet-night-oil")}</section>
      <div class="notice" style="margin-top:16px">${icon("info")}<span>If something worries you, such as pain, swelling or a rash that doesn't settle, talk to a doctor or dermatologist. This journal is not a medical record.</span></div>` };
  };

  SCREENS.journalNew = r => {
    const err = r.q.get("demo") === "error";
    return { title: "New journal note", nav: "journal", html: `
      <a class="btn text" href="#/journal" style="margin-left:-6px">${icon("back")}Journal</a>
      <h1 tabindex="-1">New note</h1><p class="lede">Today, ${fmtDate(D.demo_date)}. Short is fine.</p>
      <form id="noteForm" class="card" style="margin-top:20px;max-width:680px" novalidate>
        ${radioGroup("mood", "How does your skin feel?", D.moods, S.checkin || "Calm")}
        <label class="field" for="note">Note</label>
        <textarea class="input" id="note" name="note" maxlength="280" aria-describedby="noteHint${err ? " noteErr" : ""}"${err ? ' aria-invalid="true"' : ""} placeholder="What did you notice today?"></textarea>
        <div class="hint" id="noteHint"><span data-count>0</span> of 280 characters</div>
        <div id="noteErr" class="err" role="alert"${err ? "" : " hidden"}>${icon("info")}Write a few words before saving, or go back without saving.</div>
        <div class="row" style="margin-top:18px;flex-wrap:wrap"><button class="btn primary" type="submit">Save note</button><a class="btn text" href="#/journal">Cancel</a></div>
      </form>` };
  };

  SCREENS.profile = () => ({ title: "Profile", nav: "profile", html: `
    <div class="eyebrow">Get to know your skin</div><h1 tabindex="-1">Your preferences</h1>
    <p class="lede">These only change which products appear first. They are not a diagnosis.</p>
    <div class="grid2" style="margin-top:22px;align-items:start">
      <form id="profileForm" class="card" novalidate>
        ${radioGroup("skin_type", "Skin type", D.user.skin_types, S.profile.skin_type)}
        ${radioGroup("focus", "Focus", D.user.focus_options, S.profile.focus)}
        <button class="btn primary" type="submit">Save preferences</button></form>
      <div class="stack">
        <a class="card between" href="#/shelf" style="text-decoration:none"><span><b>Your shelf</b><br><span class="small muted">${S.saved.size} saved</span></span>${icon("chev")}</a>
        <a class="card between" href="#/journal" style="text-decoration:none"><span><b>Skin journal</b><br><span class="small muted">${S.journal.length} notes</span></span>${icon("chev")}</a>
        <a class="card between" href="#/about" style="text-decoration:none"><span><b>About this concept</b><br><span class="small muted">What is real, what is not</span></span>${icon("chev")}</a>
        <button class="btn ghost" data-restart>Restart the demo</button></div></div>` });

  SCREENS.about = () => ({ title: "About this concept", nav: "profile", html: `
    <a class="btn text" href="#/profile" style="margin-left:-6px">${icon("back")}Profile</a>
    <h1 tabindex="-1">About this concept</h1>
    <div class="stack" style="max-width:720px;margin-top:16px">
      <div class="card"><h2 class="h3">What ButterSkin is</h2><p>A self-initiated design concept for a calm skincare companion app, created for a design portfolio.</p></div>
      <div class="card"><h2 class="h3">What it is not</h2><p>Not a real brand, shop or medical tool. Products, formulations, prices, people and journal entries are fictional. Ingredient notes describe what an ingredient is commonly used for, not what a product does. Nothing is sold, stored or sent.</p></div>
      <div class="card"><h2 class="h3">Credits</h2><p>Concept &amp; art direction: Purnananda Mishra · AI-assisted design and production</p>
        <p class="small muted">Typefaces: Playfair Display and DM Sans, SIL Open Font License 1.1. Illustrations and packaging are original to this concept.</p></div></div>` });

  /* ---------- product dialog ---------- */
  let lastFocusSel = null;
  function openProduct(id) {
    const p = P[id]; if (!p) return;
    const saved = S.saved.has(p.id), inAM = D.routines.AM.find(s => s.product === p.id), inPM = D.routines.PM.find(s => s.product === p.id);
    $("#dialog").innerHTML = `
      <div class="shot bg-${p.category}">${pack(p, true)}</div>
      <div class="body"><button class="close" data-close aria-label="Close">${icon("close")}</button>
        <div class="eyebrow">${esc(CAT[p.category].name)} · concept product</div>
        <h2 id="dlgTitle">${esc(p.name)}</h2>
        <div class="row" style="flex-wrap:wrap;gap:8px"><span class="price">${price(p.price)}</span><span class="muted small">· ${esc(p.size)} · ${esc(p.texture)}</span></div>
        <p>${esc(p.about)}</p>
        <h3 class="h3" style="margin-top:18px">Where it fits</h3>
        <p class="small" style="margin:6px 0">${inAM || inPM ? `In your ${inAM ? "morning" : "evening"} routine: “${esc((inAM || inPM).name)}”.` : "Not in your routine."} ${esc(p.how)}</p>
        <h3 class="h3" style="margin-top:18px">Key ingredients <span class="cap muted">(concept formulation)</span></h3>
        <ul class="ing">${p.ingredients.map(i => `<li><b>${esc(i[0])}</b>: ${esc(i[1])}</li>`).join("")}</ul>
        <div class="notice" style="margin-top:16px">${icon("info")}<span>Fictional product for a design concept. With any real product, patch test first and stop if it irritates.</span></div>
        <div class="row" style="margin-top:18px;flex-wrap:wrap"><button class="btn primary" data-save="${p.id}" aria-pressed="${saved}">${icon("heart")}${saved ? "Saved to shelf" : "Save to shelf"}</button>
          <button class="btn text" data-close>Close</button></div></div>`;
    $("#scrim").classList.add("open");
    $("#app").inert = true;
    $("#dialog .close").focus();
  }
  function closeProduct(restore = true) {
    if (!$("#scrim").classList.contains("open")) return;
    $("#scrim").classList.remove("open"); $("#app").inert = false;
    const el = restore && lastFocusSel && $(lastFocusSel); if (el) el.focus();
  }

  /* ---------- render ---------- */
  function render() {
    const r = parse();
    const key = keyOf(r);
    if (key === "product") {
      // product route: the previous screen (or Discover, for a direct link) stays underneath with the dialog open
      const ur = parseHash(render._under || "#/discover");
      draw(keyOf(ur), ur);
      openProduct(r.parts[1]);
      document.title = "ButterSkin · " + (P[r.parts[1]] ? P[r.parts[1]].name : "Product");
      return;
    }
    closeProduct(false);
    render._under = location.hash || "#/welcome/1";
    draw(key, r);
  }
  function draw(key, r) {
    const fn = SCREENS[key] || SCREENS.home;
    const v = fn(r);
    document.title = "ButterSkin · " + v.title;
    document.body.classList.toggle("full", !!v.full);
    $("#side").hidden = !!v.full; $("#topbar").hidden = !!v.full; $("#tabbar").hidden = !!v.full;
    $("#view").innerHTML = `<div class="page">${v.html}</div>` + (v.full ? "" :
      `<p class="credit">ButterSkin is a fictional, self-initiated concept. Products, prices and routines are illustrative, not medical advice.<br>Concept &amp; art direction: Purnananda Mishra · AI-assisted design and production</p>`);
    $$("[data-nav]").forEach(a => a.dataset.nav === v.nav ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current"));
    wire();
  }

  function wire() {
    const sf = $("#setupForm"), pf = $("#profileForm"), nf = $("#noteForm"), search = $("[data-search]");
    const readPrefs = f => { const fd = new FormData(f); S.profile.skin_type = fd.get("skin_type") || S.profile.skin_type; S.profile.focus = fd.get("focus") || S.profile.focus; };
    if (sf) sf.addEventListener("submit", e => { e.preventDefault(); readPrefs(sf); go("#/home"); toast("Preferences saved for this session"); });
    if (pf) pf.addEventListener("submit", e => { e.preventDefault(); readPrefs(pf); toast("Preferences saved for this session"); render(); });
    if (search) search.addEventListener("submit", e => { e.preventDefault(); const u = new URLSearchParams(parse().q); const v = $("#q").value.trim(); v ? u.set("q", v) : u.delete("q"); go("#/discover" + (u.toString() ? "?" + u : "")); });
    if (nf) {
      const ta = $("#note"), cnt = $("[data-count]", nf), er = $("#noteErr");
      const upd = () => { cnt.textContent = ta.value.length; };
      ta.addEventListener("input", () => { upd(); if (ta.value.trim()) { ta.removeAttribute("aria-invalid"); er.hidden = true; ta.setAttribute("aria-describedby", "noteHint"); } }); upd();
      nf.addEventListener("submit", e => {
        e.preventDefault();
        if (!ta.value.trim()) { ta.setAttribute("aria-invalid", "true"); ta.setAttribute("aria-describedby", "noteHint noteErr"); er.hidden = false; ta.focus(); return; }
        S.journal.unshift({ date: D.demo_date, mood: new FormData(nf).get("mood"), note: ta.value.trim() });
        go("#/journal"); toast("Note saved for this session");
      });
    }
  }

  /* ---------- global events ---------- */
  document.addEventListener("click", e => {
    const t = e.target.closest("[data-save],[data-checkin],[data-reset],[data-restart],[data-close],a[href^='#/product/']");
    if (!t) return;
    if (t.matches("a[href^='#/product/']")) { lastFocusSel = `#view a[href="${t.getAttribute("href")}"]`; return; }
    if (t.dataset.close !== undefined) { e.preventDefault(); location.hash = render._under || "#/discover"; return; }
    if (t.dataset.save) {
      const id = t.dataset.save, had = S.saved.has(id); had ? S.saved.delete(id) : S.saved.add(id);
      toast(had ? "Removed from your shelf" : "Saved to your shelf");
      if ($("#scrim").classList.contains("open")) { const ur = parseHash(render._under || "#/discover"); $("#app").inert = false; draw(keyOf(ur), ur); openProduct(id); const b = $("#dialog [data-save]"); b && b.focus(); }
      else { const sel = `[data-save="${id}"]`; render(); const again = $(sel); again && again.focus(); }
      return;
    }
    if (t.dataset.checkin) {
      S.checkin = t.dataset.checkin;
      const today = S.journal.find(j => j.date === D.demo_date && j.auto);
      today ? (today.mood = S.checkin) : S.journal.unshift({ date: D.demo_date, mood: S.checkin, note: "Quick check-in from Home.", auto: true });
      toast(`Noted: ${S.checkin}. Added to your journal.`); render(); const b = $(`[data-checkin="${CSS.escape(S.checkin)}"]`); b && b.focus(); return;
    }
    if (t.dataset.reset) { S.done[t.dataset.reset].clear(); toast("Ticks cleared for today"); render(); return; }
    if (t.dataset.restart !== undefined) { S = fresh(); go("#/welcome/1"); toast("Demo restarted"); }
  });
  document.addEventListener("change", e => {
    const c = e.target.closest("input[data-step]"); if (!c) return;
    const set = S.done[c.dataset.time]; c.checked ? set.add(c.dataset.step) : set.delete(c.dataset.step);
    const id = c.id; render(); const again = document.getElementById(id); again && again.focus();
  });
  document.addEventListener("keydown", e => {
    if (!$("#scrim").classList.contains("open")) return;
    if (e.key === "Escape") { e.preventDefault(); location.hash = render._under || "#/discover"; return; }
    if (e.key === "Tab") {
      const f = $$("#dialog button, #dialog a[href], #dialog input");
      const a = f[0], z = f[f.length - 1];
      if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
      else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
    }
  });
  $("#scrim").addEventListener("click", e => { if (e.target.id === "scrim") location.hash = render._under || "#/discover"; });
  window.addEventListener("hashchange", () => {
    const wasProduct = !!$("#scrim.open");
    render();
    if (!parse().parts[0] || parse().parts[0] !== "product") {
      const back = wasProduct && lastFocusSel && $(lastFocusSel); if (back) { back.focus(); return; }
      const h = $("#view h1"); h && h.focus({ preventScroll: false });
      window.scrollTo(0, 0);
    }
  });
  render();
})();
