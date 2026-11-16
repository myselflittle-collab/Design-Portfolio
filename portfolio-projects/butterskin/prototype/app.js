/* ButterSkin prototype · Botanical Luxury. Fictional concept store: nothing is sold, stored or sent.
   All content comes from assets/data.js (generated from data/products.json by tools/build_data.py).
   Routes live in the URL hash, so every screen and state can be opened directly (see documentation/screen-inventory.md). */
(function () {
  "use strict";
  const D = window.BS_DATA;
  const P = Object.fromEntries(D.products.map(p => [p.id, p]));
  const CAT = Object.fromEntries(D.categories.map(c => [c.id, c]));
  const SHOP = D.shop;
  const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const ALIAS = { discover: "shop", shelf: "wishlist", profile: "account" };

  /* ---------- session state (memory only) ---------- */
  const fresh = () => ({
    done: { AM: new Set(D.routines.demo_done_AM), PM: new Set() },
    wish: new Set(D.demo_saved),
    bag: new Map(D.demo_bag.map(b => [b.id, b.qty])),
    journal: D.journal.map(j => Object.assign({}, j)),
    profile: { skin_type: D.user.skin_type, focus: D.user.focus },
    checkin: null, order: null,
    checkout: { name: "", phone: "", address: "", city: "", pin: "", delivery: "standard" }
  });
  let S = fresh();

  /* ---------- helpers ---------- */
  const $ = (s, el) => (el || document).querySelector(s);
  const $$ = (s, el) => [...(el || document).querySelectorAll(s)];
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const icon = (n, cls) => `<svg class="ic${cls ? " " + cls : ""}" aria-hidden="true"><use href="#i-${n}"/></svg>`;
  const inr = n => "₹" + n.toLocaleString("en-IN");
  const fmtDate = iso => { const [, m, d] = iso.split("-").map(Number); return `${d} ${MONTHS[m - 1]}`; };
  const img = (p, kind, alt) => `<img src="assets/products/${p.id}${kind ? "-" + kind : ""}.jpg" width="720" height="900" decoding="async" alt="${alt ? esc(alt) : ""}">`;
  const photo = (f, alt) => `<img src="assets/photo/${f}.jpg" decoding="async" alt="${alt ? esc(alt) : ""}">`;
  const ingLine = p => p.ingredients.slice(0, 2).map(i => i[0]).join(" · ");
  const bagCount = () => [...S.bag.values()].reduce((a, b) => a + b, 0);
  const subtotal = () => [...S.bag].reduce((a, [id, q]) => a + P[id].price * q, 0);
  const deliveryFee = (method) => method === "express" ? 149 : (subtotal() >= SHOP.free_delivery_over ? 0 : SHOP.delivery_fee);
  const toast = msg => { const t = $("#toast"); t.textContent = msg; t.classList.add("show"); clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove("show"), 2600); };
  const parseHash = h => { const [p, q] = (h || "").replace(/^#/, "").split("?"); return { parts: (p || "").split("/").filter(Boolean), q: new URLSearchParams(q || "") }; };
  const go = h => { location.hash = h; };

  /* ---------- shared pieces ---------- */
  const wishBtn = (p, cls = "") => {
    const on = S.wish.has(p.id);
    return `<button class="icon-btn wish ${cls}" data-wish="${p.id}" aria-pressed="${on}" aria-label="${on ? "Remove " + esc(p.name) + " from wishlist" : "Save " + esc(p.name) + " to wishlist"}">${icon("heart")}</button>`;
  };
  function card(p) {
    return `<article class="pcard">
      <div class="media bg-${p.category}">${img(p, "", p.name + ", 3D render of concept packaging")}<span class="tag">Concept</span>${wishBtn(p)}</div>
      <div class="body"><span class="cat">${esc(CAT[p.category].name)}</span>
        <a class="name" href="#/product/${p.id}">${esc(p.name)}</a>
        <span class="desc">${esc(p.short)}</span><span class="ingl">${esc(ingLine(p))}</span>
        <div class="meta"><span class="price">${inr(p.price)}</span><span class="size">${esc(p.size)}</span></div>
        <button class="btn btn-primary btn-full add" id="add-${p.id}" data-add="${p.id}">${icon("bag")}Add to bag</button></div>
    </article>`;
  }
  function empty(title, text, action, href, art) {
    return `<div class="empty">${art ? `<div class="media bg-${P[art].category}">${img(P[art])}</div>` : ""}
      <h2>${title}</h2><p class="muted" style="max-width:420px;margin:0 auto 22px">${text}</p>${action ? `<a class="btn btn-primary" href="${href}">${action}</a>` : ""}</div>`;
  }
  const options = (name, legend, list, value) => `<fieldset><legend>${legend}</legend><div class="options">${list.map(o =>
    `<label class="opt"><input type="radio" name="${name}" value="${esc(o)}"${o === value ? " checked" : ""}><span>${esc(o)}</span></label>`).join("")}</div></fieldset>`;
  const qtyControl = (id, q, ctx) => `<div class="qty${ctx === "line" ? " sm" : ""}" role="group" aria-label="Quantity">
      <button type="button" data-qty="${ctx}" data-id="${id}" data-d="-1" aria-label="Decrease quantity"${q <= 1 ? " disabled" : ""}>${icon("minus", "sm")}</button>
      <output aria-live="polite" aria-label="Quantity ${q}">${q}</output>
      <button type="button" data-qty="${ctx}" data-id="${id}" data-d="1" aria-label="Increase quantity"${q >= SHOP.max_qty ? " disabled" : ""}>${icon("plus", "sm")}</button></div>`;

  /* ---------- screens ---------- */
  const V = {};

  V.welcome = r => {
    const n = Math.min(3, Math.max(1, Number(r.parts[1] || 1)));
    const s = [
      { pic: "hero", e: "Welcome to ButterSkin", h: "Botanical skincare,<br><em class=\"serif-i\">quietly considered.</em>",
        p: "Shop a small edit of everyday essentials, keep a simple routine and notice how your skin feels. This is a fictional concept store: nothing is sold." },
      { pic: "detail", e: "Small steps", h: "Skipping a step<br><em class=\"serif-i\">is fine.</em>",
        p: "Routines are checklists, not scores. There are no streaks to keep and nothing to lose if you miss a night." },
      { pic: "texture", e: "Honest by design", h: "Where it fits,<br><em class=\"serif-i\">not what it fixes.</em>",
        p: "Every product shows its place in a routine and plain-language ingredients. ButterSkin never diagnoses skin or promises results." }][n - 1];
    return { title: `Welcome ${n} of 3`, full: true, html: `<div class="onb"><div class="visual" aria-hidden="true">${s.pic === "texture" ? img(P["butter-balm-cream"], "texture") : photo(s.pic)}</div>
      <div class="copy"><img class="logo" src="assets/logo-lockup.svg" alt="ButterSkin">
        <div class="eyebrow em" style="margin-top:18px">${s.e}</div><h1 tabindex="-1">${s.h}</h1><p class="lede">${s.p}</p>
        <div class="dots" role="img" aria-label="Step ${n} of 3">${[1, 2, 3].map(i => `<i class="${i === n ? "on" : ""}"></i>`).join("")}</div>
        <div class="row" style="margin-top:14px;flex-wrap:wrap;gap:16px"><a class="btn btn-primary" href="${n < 3 ? "#/welcome/" + (n + 1) : "#/setup"}">${n < 3 ? "Continue" : "Personalise"}</a>
          <a class="btn btn-text" href="#/home">Skip to the store</a></div>
        <p class="cap muted" style="margin-top:6px">Concept app · fictional brand, products and people · not medical advice</p></div></div>` };
  };

  V.setup = () => ({ title: "Personalise", full: true, html: `<div style="max-width:680px;margin:0 auto;padding:40px 20px 60px">
    <img src="assets/logo-lockup.svg" alt="ButterSkin" style="height:40px;width:auto">
    <div class="eyebrow em" style="margin-top:32px">Optional · two questions</div><h1 tabindex="-1">Tell us a little about your skin</h1>
    <p class="lede">This only changes which products we show first. It is not a diagnosis, and you can change it any time in Account.</p>
    <form id="prefForm" class="panel" style="margin-top:24px" novalidate>
      ${options("skin_type", "Skin type", D.user.skin_types, S.profile.skin_type)}${options("focus", "Focus", D.user.focus_options, S.profile.focus)}
      <div class="row" style="flex-wrap:wrap;gap:16px"><button class="btn btn-primary" type="submit">Save and continue</button><a class="btn btn-text" href="#/home">Skip for now</a></div></form></div>` });

  V.home = () => {
    const am = D.routines.AM, done = am.filter(s => S.done.AM.has(s.id)).length, next = am.find(s => !S.done.AM.has(s.id));
    const picks = D.products.filter(p => p.focus.includes(S.profile.focus)).slice(0, 4);
    return { title: "Home", nav: "home", html: `
      <section class="hero" aria-labelledby="heroH"><div class="photo">${photo("hero", "ButterSkin products on stone with moss, white flowers and leaves in warm sunlight (3D render)")}</div>
        <div class="copy"><img class="logo" src="assets/logo-lockup-reverse.svg" alt=""><div class="eyebrow">The morning edit · concept</div>
        <h1 id="heroH" tabindex="-1">Real care<br><em class="serif-i">for real skin.</em></h1>
        <p class="lede">Botanical concept formulas and a simple four-step morning ritual.</p>
        <div class="row" style="flex-wrap:wrap;margin-top:10px"><a class="btn btn-primary" href="#/routine">Shop the routine</a><a class="btn btn-secondary" href="#/shop">Browse all</a></div></div></section>
      <div class="values" role="list">${[["leaf", "Concept formulas", "Every product is a design concept, labelled as one."], ["info", "Plain-language ingredients", "What each one is commonly used for, never a promise."],
        ["routine", "Routine first", "Products show where they fit. No scores, no streaks."]].map(([i, b, t]) => `<div role="listitem">${icon(i)}<div><b>${b}</b><span>${t}</span></div></div>`).join("")}</div>
      <div class="section-h"><h2>Shop by step</h2><a href="#/shop">Shop all</a></div>
      <div class="cats">${D.categories.map(c => { const p = D.products.find(x => x.category === c.id);
        return `<a class="cat-tile" href="#/shop?cat=${c.id}"><div class="media bg-${c.id}">${img(p)}</div><div class="t">${c.name}<span>${D.products.filter(x => x.category === c.id).length} products</span></div></a>`; }).join("")}</div>
      <div class="section-h"><h2>For a ${esc(S.profile.focus.toLowerCase())} focus</h2><a href="#/shop?focus=1">See all</a></div>
      <div class="pgrid">${picks.map(card).join("")}</div>
      <div class="today" style="margin-top:48px">
        <section class="panel tint" aria-labelledby="todayH"><div class="eyebrow">Today · ${D.demo_weekday}, ${fmtDate(D.demo_date)}</div>
          <h2 id="todayH" style="margin:8px 0 14px">${done} of ${am.length} morning steps done</h2>
          <div class="progress" role="img" aria-label="${done} of ${am.length} morning steps done"><span style="width:${done / am.length * 100}%"></span></div>
          <p class="small" style="margin:14px 0 18px;color:var(--bs-text-secondary)">${next ? "Next: " + esc(next.name) + ". Skipping a step is fine." : "Morning steps are done for today."}</p>
          <a class="btn btn-secondary" href="#/routine">Open my routine</a></section>
        <section class="panel checkin" aria-labelledby="ciH"><h2 id="ciH">How does your skin feel today?</h2>
          <p class="small muted" style="margin:6px 0 0">One tap adds a note to your journal. Nothing is scored.</p>
          <div class="options" role="group" aria-labelledby="ciH">${D.moods.map(m => `<button class="btn btn-secondary btn-sm" data-checkin="${esc(m)}" aria-pressed="${S.checkin === m}"${S.checkin === m ? ' style="background:var(--bs-emerald-800);color:#fff"' : ""}>${esc(m)}</button>`).join("")}</div></section></div>` };
  };

  V.shop = r => {
    const cat = r.q.get("cat") || "all", q = (r.q.get("q") || "").trim(), focus = r.q.get("focus") === "1", sort = r.q.get("sort") || "featured";
    let res = D.products.filter(p => (cat === "all" || p.category === cat) && (!focus || p.focus.includes(S.profile.focus)) &&
      (!q || (p.name + " " + p.short + " " + p.ingredients.map(i => i[0]).join(" ")).toLowerCase().includes(q.toLowerCase())));
    if (sort === "price-asc") res = res.slice().sort((a, b) => a.price - b.price);
    if (sort === "price-desc") res = res.slice().sort((a, b) => b.price - a.price);
    const qs = o => { const u = new URLSearchParams({ cat, q, focus: focus ? "1" : "", sort }); Object.entries(o).forEach(([k, v]) => u.set(k, v));
      [...u.keys()].forEach(k => { const v = u.get(k); if (!v || v === "all" || v === "featured") u.delete(k); }); return "#/shop" + (u.toString() ? "?" + u : ""); };
    const title = cat === "all" ? "Shop all" : CAT[cat].name;
    return { title: "Shop", nav: "shop", html: `
      <div class="eyebrow em">The ButterSkin edit · fictional</div><h1 tabindex="-1">${title}</h1>
      <p class="lede">Eight concept essentials. Each one shows where it fits in a routine, never what it will “fix”.</p>
      <form class="search" role="search" style="margin:24px 0 8px;max-width:560px" data-search>
        <label class="sr" for="q">Search products and ingredients</label>${icon("search")}
        <input class="input" id="q" name="q" type="search" value="${esc(q)}" placeholder="Search products or ingredients" autocomplete="off"></form>
      <nav class="cattabs" aria-label="Categories">${[["all", "All"]].concat(D.categories.map(c => [c.id, c.name])).map(([id, n]) =>
        `<a href="${qs({ cat: id })}"${cat === id ? ' aria-current="true"' : ""}>${n}</a>`).join("")}</nav>
      <div class="between" style="margin:16px 0 22px;flex-wrap:wrap">
        <p class="small muted" aria-live="polite" style="margin:0">${res.length} product${res.length === 1 ? "" : "s"}${q ? ` for “${esc(q)}”` : ""}</p>
        <div class="row" style="flex-wrap:wrap;gap:20px">
          <a class="switch" role="switch" aria-checked="${focus}" href="${qs({ focus: focus ? "" : "1" })}"><span class="track" aria-hidden="true"></span>Suits my ${esc(S.profile.focus.toLowerCase())} focus</a>
          <div class="row"><label class="small" for="sort">Sort by</label><select class="input" id="sort" data-sort style="width:auto;min-height:44px;padding:8px 12px">
            ${[["featured", "Featured"], ["price-asc", "Price: low to high"], ["price-desc", "Price: high to low"]].map(([v, l]) => `<option value="${v}"${sort === v ? " selected" : ""}>${l}</option>`).join("")}</select></div></div></div>
      ${res.length ? `<div class="pgrid">${res.map(card).join("")}</div>` :
        `<div class="panel">${empty("Nothing matches yet", `No concept products match${q ? " “" + esc(q) + "”" : ""} with these filters. Try another word or clear the filters.`, "Clear filters", "#/shop", "still-water-essence")}</div>`}` };
  };

  let pdpQty = 1, pdpView = "";
  V.product = r => {
    const p = P[r.parts[1]]; if (!p) return V.shop(parseHash("#/shop"));
    if (V.product._last !== p.id) { pdpQty = 1; pdpView = ""; V.product._last = p.id; }
    const inAM = D.routines.AM.find(s => s.product === p.id), inPM = D.routines.PM.find(s => s.product === p.id), wished = S.wish.has(p.id);
    const pairs = D.products.filter(x => x.id !== p.id && x.routine === p.routine).slice(0, 4);
    const views = [["", "Product"], ["scene", "In the garden"], ["texture", "Texture"]];
    return { title: p.name, nav: "shop", html: `
      <nav class="crumbs" aria-label="Breadcrumb"><a href="#/shop">Shop</a> / <a href="#/shop?cat=${p.category}">${CAT[p.category].name}</a> / <span aria-current="page">${esc(p.name)}</span></nav>
      <div class="pdp">
        <div class="gallery"><div class="media main-img bg-${p.category}" id="mainImg">${img(p, pdpView, p.name + (pdpView === "texture" ? " texture swatch, 3D render" : pdpView === "scene" ? " on stone with leaves, 3D render" : ", 3D render of concept packaging"))}<span class="tag">Concept product</span></div>
          <div class="thumbs" role="group" aria-label="Product images">${views.map(([k, l]) => `<button class="bg-${p.category}" data-view="${k}" aria-pressed="${pdpView === k}" aria-label="Show ${l.toLowerCase()} image">${img(p, k)}</button>`).join("")}</div></div>
        <div>
          <div class="eyebrow em">${CAT[p.category].name} · concept product</div>
          <h1 tabindex="-1">${esc(p.name)}</h1>
          <p class="lede">${esc(p.short)}.</p><p class="small muted" style="margin:8px 0 0">Key ingredients: ${esc(p.ingredients.map(i => i[0]).join(" · "))}</p>
          <div class="row" style="margin-top:16px;gap:14px"><span class="price" style="font-size:22px">${inr(p.price)}</span><span class="muted">${esc(p.size)}</span></div>
          <div class="facts"><div><b>Texture</b>${esc(p.texture)}</div><div><b>Routine</b>${inAM ? "Morning" : inPM ? "Evening" : "Either"}</div><div><b>Size</b>${esc(p.size)}</div></div>
          <div class="label" id="qtyLabel">Quantity</div>
          <div class="buy">${qtyControl(p.id, pdpQty, "pdp")}
            <button class="btn btn-primary" id="pdpAdd" data-add="${p.id}" data-qty-from="pdp">${icon("bag")}Add to bag · ${inr(p.price * pdpQty)}</button>
            <button class="btn btn-secondary" data-wish="${p.id}" aria-pressed="${wished}">${icon("heart")}${wished ? "Saved" : "Wishlist"}</button></div>
          <p class="small muted row" style="margin-top:14px;gap:8px">${icon("truck", "sm")}Free delivery over ${inr(SHOP.free_delivery_over)} · demo only, nothing ships</p>
          <div style="margin-top:22px">
            <details class="acc" open><summary>Description</summary><div class="in"><p style="margin:0">${esc(p.about)}</p></div></details>
            <details class="acc"><summary>How to use</summary><div class="in"><p style="margin:0">${esc(p.how)}</p></div></details>
            <details class="acc" open><summary>Key ingredients</summary><div class="in"><p class="cap muted" style="margin:0 0 6px">Concept formulation. Notes describe what an ingredient is commonly used for, not what this product does.</p>
              <ul class="ing">${p.ingredients.map(i => `<li><b>${esc(i[0])}</b><span>${esc(i[1][0].toUpperCase() + i[1].slice(1))}</span></li>`).join("")}</ul></div></details>
            <details class="acc"><summary>Where it fits</summary><div class="in"><p style="margin:0">${inAM || inPM ? `In your ${inAM ? "morning" : "evening"} routine as “${esc((inAM || inPM).name)}”.` : "Not in your routine yet."} Suits a ${p.focus.map(f => esc(f.toLowerCase())).join(", ")} focus.</p>
              <a class="btn btn-text" style="margin-top:8px" href="#/routine${inPM ? "?time=PM" : ""}">See the routine</a></div></details></div>
          <div class="notice" style="margin-top:20px">${icon("info")}<span>Fictional product for a design concept. With any real product, patch test first and stop if it irritates.</span></div>
        </div></div>
      ${pairs.length ? `<div class="section-h"><h2>Pairs well with</h2><a href="#/shop">Shop all</a></div><div class="pgrid">${pairs.map(card).join("")}</div>` : ""}` };
  };

  V.wishlist = r => {
    const ids = r.q.get("demo") === "empty" ? [] : [...S.wish];
    return { title: "Wishlist", nav: "", tool: "wishlist", html: `<div class="eyebrow em">Saved for later</div><h1 tabindex="-1">Wishlist</h1>
      <p class="lede">Products you want to look at again. Saving is not buying, and nothing here is a recommendation.</p>
      <div style="margin-top:28px">${ids.length ? `<div class="pgrid">${ids.map(id => card(P[id])).join("")}</div>` :
        `<div class="panel">${empty("Your wishlist is empty", "Tap the heart on any product to keep it here while you think.", "Browse products", "#/shop", "butter-balm-cream")}</div>`}</div>` };
  };

  V.bag = r => {
    const lines = r.q.get("demo") === "empty" ? [] : [...S.bag];
    if (!lines.length) return { title: "Bag", tool: "bag", html: `<h1 tabindex="-1">Your bag</h1><div class="panel" style="margin-top:20px">${empty("Your bag is empty", "Browse the edit and add anything you'd like to try. This is a demo store, so nothing is charged.", "Shop the edit", "#/shop", "dewdrop-hydration-serum")}</div>` };
    const sub = subtotal(), del = deliveryFee("standard");
    return { title: "Bag", tool: "bag", html: `<h1 tabindex="-1">Your bag <span class="muted" style="font:400 18px var(--bs-font-text)">(${bagCount()} item${bagCount() > 1 ? "s" : ""})</span></h1>
      <div class="bag" style="margin-top:20px"><section aria-label="Items">${lines.map(([id, q]) => { const p = P[id];
        return `<div class="line"><a class="media bg-${p.category}" href="#/product/${id}" tabindex="-1" aria-hidden="true">${img(p)}</a>
          <div><div class="eyebrow">${CAT[p.category].name} · concept</div><a class="nm" href="#/product/${id}">${esc(p.name)}</a><div class="small muted">${esc(p.size)} · ${inr(p.price)} each</div>
            <div class="ctrl">${qtyControl(id, q, "line")}<button class="btn btn-text btn-sm" data-remove="${id}" aria-label="Remove ${esc(p.name)} from bag">Remove</button></div></div>
          <div class="price lp">${inr(p.price * q)}</div></div>`; }).join("")}
        <a class="btn btn-text" style="margin-top:16px" href="#/shop">Continue shopping</a></section>
        <aside class="panel summary" aria-labelledby="sumH"><h2 id="sumH" class="h3">Order summary</h2>
          <div style="margin-top:14px"><div class="sumrow"><span>Subtotal</span><span>${inr(sub)}</span></div>
          <div class="sumrow"><span>Delivery</span><span>${del ? inr(del) : "Free"}</span></div>
          <div class="sumrow total"><span>Total</span><span>${inr(sub + del)}</span></div></div>
          <p class="cap muted">${del ? `Delivery is free on orders over ${inr(SHOP.free_delivery_over)}.` : "Free standard delivery applies."} ${esc(SHOP.currency_note)}</p>
          <a class="btn btn-primary btn-full" href="#/checkout" style="margin-top:8px">Checkout</a></aside></div>` };
  };

  const FIELDS = [["name", "Full name", "text", "name", ""], ["phone", "Mobile number", "tel", "tel", "10 digits, e.g. 90000 00000"],
    ["address", "Address", "text", "street-address", ""], ["city", "City", "text", "address-level2", ""], ["pin", "PIN code", "text", "postal-code", "6 digits"]];
  function validate(c) {
    const e = {};
    if (!c.name.trim()) e.name = "Enter your full name.";
    if (!/^\d{10}$/.test(c.phone.replace(/\s/g, ""))) e.phone = "Enter a 10-digit mobile number.";
    if (!c.address.trim()) e.address = "Enter your address.";
    if (!c.city.trim()) e.city = "Enter your city.";
    if (!/^\d{6}$/.test(c.pin.trim())) e.pin = "Enter a 6-digit PIN code.";
    return e;
  }
  V.checkout = r => {
    if (!S.bag.size) return V.bag(parseHash("#/bag"));
    const c = S.checkout, errs = r.q.get("demo") === "error" ? validate({ name: "", phone: "", address: "", city: "", pin: "" }) : (V.checkout._errs || {});
    const sub = subtotal(), del = deliveryFee(c.delivery), keys = Object.keys(errs);
    const field = ([k, l, t, ac, hint]) => `<div class="${k === "address" ? "full" : ""}"><label class="field" for="f-${k}">${l}</label>
      <input class="input" id="f-${k}" name="${k}" type="${t}" autocomplete="${ac}" value="${esc(r.q.get("demo") === "error" ? "" : c[k])}"${t === "tel" || k === "pin" ? ' inputmode="numeric"' : ""}
        ${errs[k] ? `aria-invalid="true" aria-describedby="e-${k}${hint ? " h-" + k : ""}"` : hint ? `aria-describedby="h-${k}"` : ""}>
      ${hint ? `<div class="hint" id="h-${k}">${hint}</div>` : ""}${errs[k] ? `<div class="err" id="e-${k}">${icon("info")}${errs[k]}</div>` : ""}</div>`;
    return { title: "Checkout", tool: "bag", html: `<div class="steps-bar" aria-label="Checkout steps"><span>1 Bag</span><span class="on" aria-current="step">2 Details</span><span>3 Confirmation</span></div>
      <h1 tabindex="-1">Checkout</h1><p class="lede">Demo checkout: nothing is charged and no order is sent.</p>
      <div class="bag" style="margin-top:24px"><form id="coForm" novalidate>
        ${keys.length ? `<div class="err-summary" id="errSum" role="alert" tabindex="-1"><h2>Please check ${keys.length} field${keys.length > 1 ? "s" : ""}</h2><ul>${keys.map(k => `<li><a href="#f-${k}" data-jump="f-${k}">${errs[k]}</a></li>`).join("")}</ul></div>` : ""}
        <section class="panel"><h2 class="h3" style="margin-bottom:16px">Delivery address</h2><div class="form-grid">${FIELDS.map(field).join("")}</div></section>
        <section class="panel" style="margin-top:18px"><fieldset style="margin:0"><legend class="h3" style="font:500 20px/26px var(--bs-font-display);letter-spacing:0;text-transform:none;color:var(--bs-text-primary);margin-bottom:14px">Delivery</legend>
          <label class="radio-row"><input type="radio" name="delivery" value="standard"${c.delivery === "standard" ? " checked" : ""}><span><b style="font-weight:500">Standard</b><br><span class="small muted">3–5 working days (demo)</span></span><span>${sub >= SHOP.free_delivery_over ? "Free" : inr(SHOP.delivery_fee)}</span></label>
          <label class="radio-row"><input type="radio" name="delivery" value="express"${c.delivery === "express" ? " checked" : ""}><span><b style="font-weight:500">Express</b><br><span class="small muted">Next working day (demo)</span></span><span>${inr(149)}</span></label></fieldset></section>
        <section class="panel" style="margin-top:18px"><fieldset style="margin:0"><legend class="h3" style="font:500 20px/26px var(--bs-font-display);letter-spacing:0;text-transform:none;color:var(--bs-text-primary);margin-bottom:14px">Payment</legend>
          <label class="radio-row"><input type="radio" name="pay" value="demo" checked><span><b style="font-weight:500">Demo payment</b><br><span class="small muted">No payment details are collected and nothing is charged.</span></span><span></span></label></fieldset></section>
        <button class="btn btn-primary btn-full" type="submit" style="margin-top:20px">Place demo order · ${inr(sub + del)}</button></form>
        <aside class="panel summary" aria-labelledby="coSum"><h2 id="coSum" class="h3">In your bag</h2><div style="margin-top:10px">${[...S.bag].map(([id, q]) =>
          `<div class="mini"><div class="media bg-${P[id].category}">${img(P[id])}</div><div><div style="font-weight:500">${esc(P[id].name)}</div><div class="cap muted">Qty ${q} · ${esc(P[id].size)}</div></div><div>${inr(P[id].price * q)}</div></div>`).join("")}</div>
          <div style="margin-top:10px"><div class="sumrow"><span>Subtotal</span><span>${inr(sub)}</span></div><div class="sumrow"><span>Delivery</span><span>${del ? inr(del) : "Free"}</span></div>
          <div class="sumrow total"><span>Total</span><span>${inr(sub + del)}</span></div></div><a class="btn btn-text" href="#/bag">Edit bag</a></aside></div>` };
  };

  V.order = () => {
    const o = S.order || { ref: "BS-DEMO-2810-01", items: D.demo_bag.map(b => [b.id, b.qty]), total: D.demo_bag.reduce((a, b) => a + P[b.id].price * b.qty, 0) + SHOP.delivery_fee, name: "Ananya", sample: true };
    return { title: "Demo order placed", tool: "bag", html: `<div class="steps-bar" aria-label="Checkout steps"><span>1 Bag</span><span>2 Details</span><span class="on" aria-current="step">3 Confirmation</span></div>
      <div class="confirm"><img class="seal" src="assets/logo-mark.svg" alt=""><div class="eyebrow em">Demo order ${esc(o.ref)}${o.sample ? " · sample" : ""}</div>
        <h1 tabindex="-1">Thank you, ${esc(o.name.split(" ")[0])}</h1>
        <p class="lede" style="margin:0 auto">This is where a real store would confirm your order. In this concept, <b>no order has been sent and nothing has been charged.</b></p>
        <div class="panel" style="text-align:left;margin:26px 0">${o.items.map(([id, q]) => `<div class="mini"><div class="media bg-${P[id].category}">${img(P[id])}</div><div><div style="font-weight:500">${esc(P[id].name)}</div><div class="cap muted">Qty ${q}</div></div><div>${inr(P[id].price * q)}</div></div>`).join("")}
          <div class="sumrow total"><span>Total (illustrative)</span><span>${inr(o.total)}</span></div></div>
        <div class="row" style="justify-content:center;flex-wrap:wrap"><a class="btn btn-primary" href="#/routine">Back to my routine</a><a class="btn btn-secondary" href="#/shop">Continue shopping</a></div></div>` };
  };

  V.routine = r => {
    const t = r.q.get("time") === "PM" ? "PM" : "AM", list = D.routines[t], done = list.filter(s => S.done[t].has(s.id)).length;
    const prods = list.filter(s => s.product).map(s => s.product), missing = prods.filter(id => !S.bag.has(id));
    return { title: "My routine", nav: "routine", html: `<div class="between" style="align-items:flex-end;flex-wrap:wrap"><div><div class="eyebrow em">Your daily ritual</div><h1 tabindex="-1">Small steps, softer days.</h1>
      <p class="lede">Tick what you did. Skipped steps aren't counted against you, and nothing carries over to tomorrow.</p></div></div>
      <div class="between" style="margin:26px 0 16px;flex-wrap:wrap">
        <div class="rtabs" role="tablist" aria-label="Time of day"><a role="tab" href="#/routine" aria-selected="${t === "AM"}">${icon("sun", "sm")}Morning</a><a role="tab" href="#/routine?time=PM" aria-selected="${t === "PM"}">${icon("moon", "sm")}Evening</a></div>
        <span class="pill" aria-live="polite" id="progressText">${done} of ${list.length} done</span></div>
      <div class="bag"><section class="panel" role="tabpanel" aria-label="${t === "AM" ? "Morning" : "Evening"} steps"><ul class="steps">${list.map(s => { const p = s.product ? P[s.product] : null, on = S.done[t].has(s.id);
        return `<li class="step"><span class="check"><input type="checkbox" id="c-${s.id}" data-step="${s.id}" data-time="${t}"${on ? " checked" : ""}><span class="box" aria-hidden="true">${icon("check")}</span></span>
          <div class="media thumb ${p ? "bg-" + p.category : "bg-moisturise pause"}" aria-hidden="true">${p ? img(p) : icon("leaf")}</div>
          <div><label class="t" for="c-${s.id}">${esc(s.name)}${s.optional ? ' <span class="cap muted">(optional)</span>' : ""}</label><div class="s">${p ? `<a href="#/product/${p.id}">${esc(p.name)}</a> · ${inr(p.price)}` : "A moment for yourself"}</div></div>
          <span class="pill">${s.minutes} min</span></li>`; }).join("")}</ul>
        <div class="between" style="margin-top:16px;flex-wrap:wrap"><p class="small muted" style="margin:0">${done === list.length ? "All done. Nice and easy." : "Do what feels right today."}</p><button class="btn btn-text btn-sm" data-reset="${t}">Clear today's ticks</button></div></section>
        <aside class="panel tint summary" aria-labelledby="rbH"><h2 id="rbH" class="h3">Shop this routine</h2>
          <p class="small muted" style="margin:8px 0 14px">${prods.length} concept products · ${inr(prods.reduce((a, id) => a + P[id].price, 0))} together</p>
          ${prods.map(id => `<div class="mini"><div class="media bg-${P[id].category}">${img(P[id])}</div><div><a href="#/product/${id}" style="color:inherit;font-weight:500;text-decoration:none">${esc(P[id].name)}</a><div class="cap muted">${S.bag.has(id) ? "In your bag" : esc(P[id].size)}</div></div><div>${inr(P[id].price)}</div></div>`).join("")}
          <button class="btn btn-primary btn-full" style="margin-top:16px" data-add-routine="${t}"${missing.length ? "" : " disabled"}>${missing.length ? `Add ${missing.length} to bag` : "All in your bag"}</button></aside></div>` };
  };

  V.journal = r => {
    const list = r.q.get("demo") === "empty" ? [] : S.journal;
    return { title: "Skin journal", nav: "journal", html: `<div class="between" style="align-items:flex-end;flex-wrap:wrap"><div><div class="eyebrow em">Notice, don't judge</div><h1 tabindex="-1">Skin journal</h1>
      <p class="lede">Short notes about how your skin felt. Only you see them, and they're never scored.</p></div><a class="btn btn-primary" href="#/journal/new">${icon("plus")}New note</a></div>
      <section class="panel" style="margin-top:24px" aria-label="Journal entries">${list.length ? list.map(j => `<article class="entry"><div class="d">${fmtDate(j.date).split(" ")[0]}<small>${fmtDate(j.date).split(" ")[1]}</small></div>
        <div><span class="mood">${esc(j.mood)}</span><p style="margin:10px 0 0">${esc(j.note)}</p></div></article>`).join("") :
        empty("No notes yet", "When you feel like it, jot down a line about your skin. Patterns are easier to notice over time.", "Write a first note", "#/journal/new", "quiet-night-oil")}</section>
      <div class="notice" style="margin-top:18px">${icon("info")}<span>If something worries you, such as pain, swelling or a rash that doesn't settle, talk to a doctor or dermatologist. This journal is not a medical record.</span></div>` };
  };

  V.journalNew = r => {
    const err = r.q.get("demo") === "error";
    return { title: "New journal note", nav: "journal", html: `<a class="btn btn-text" href="#/journal">${icon("back", "sm")}Journal</a>
      <h1 tabindex="-1" style="margin-top:14px">New note</h1><p class="lede">Today, ${fmtDate(D.demo_date)}. Short is fine.</p>
      <form id="noteForm" class="panel" style="margin-top:22px;max-width:720px" novalidate>${options("mood", "How does your skin feel?", D.moods, S.checkin || "Calm")}
        <label class="field" for="note">Note</label>
        <textarea class="input" id="note" name="note" maxlength="280" aria-describedby="noteHint${err ? " noteErr" : ""}"${err ? ' aria-invalid="true"' : ""} placeholder="What did you notice today?"></textarea>
        <div class="hint" id="noteHint"><span data-count>0</span> of 280 characters</div>
        <div id="noteErr" class="err" role="alert"${err ? "" : " hidden"}>${icon("info")}Write a few words before saving, or go back without saving.</div>
        <div class="row" style="margin-top:20px;flex-wrap:wrap;gap:16px"><button class="btn btn-primary" type="submit">Save note</button><a class="btn btn-text" href="#/journal">Cancel</a></div></form>` };
  };

  V.account = () => ({ title: "Account", nav: "account", html: `<div class="eyebrow em">Hello, ${esc(D.user.name)} · demo account</div><h1 tabindex="-1">Account</h1>
    <div class="acct" style="margin-top:24px"><nav class="acct-nav" aria-label="Account">
      <a href="#/wishlist">Wishlist <span class="muted small">${S.wish.size} saved</span></a><a href="#/bag">Shopping bag <span class="muted small">${bagCount()} items</span></a>
      <a href="#/journal">Skin journal <span class="muted small">${S.journal.length} notes</span></a><a href="#/order">Last demo order ${icon("chev", "sm")}</a><a href="#/about">About this concept ${icon("chev", "sm")}</a></nav>
      <div><form id="prefForm" class="panel" novalidate><h2 class="h3" style="margin-bottom:6px">Skin profile</h2><p class="small muted" style="margin:0 0 18px">Preferences only change which products appear first. They are not a diagnosis.</p>
        ${options("skin_type", "Skin type", D.user.skin_types, S.profile.skin_type)}${options("focus", "Focus", D.user.focus_options, S.profile.focus)}
        <button class="btn btn-primary" type="submit">Save preferences</button></form>
        <div class="panel" style="margin-top:18px"><h2 class="h3">Demo</h2><p class="small muted">Restart clears your ticks, wishlist, bag and notes for this session.</p><button class="btn btn-secondary" data-restart>Restart the demo</button></div></div></div>` });

  V.about = () => ({ title: "About this concept", nav: "account", html: `<a class="btn btn-text" href="#/account">${icon("back", "sm")}Account</a><h1 tabindex="-1" style="margin-top:14px">About this concept</h1>
    <div class="stack" style="max-width:760px;margin-top:18px">
      <div class="panel"><h2 class="h3">What ButterSkin is</h2><p>A self-initiated design concept for a botanical skincare brand and its shopping and routine app, created for a design portfolio.</p></div>
      <div class="panel"><h2 class="h3">What it is not</h2><p>Not a real brand, shop or medical tool. Products, formulations, prices, people and journal entries are fictional. Product images are photorealistic 3D renders of modelled packaging, not photographs. Nothing is sold, charged, stored or sent.</p></div>
      <div class="panel"><h2 class="h3">Credits</h2><p>Concept &amp; art direction: Purnananda Mishra</p><p class="small muted">Typefaces: Playfair Display and Inter, SIL Open Font License 1.1. Product renders made with Blender (Cycles).</p></div></div>` });

  /* ---------- added-to-bag dialog ---------- */
  let returnTo = null;
  function openAdded(id, q) {
    const p = P[id];
    $("#dialog").innerHTML = `<button class="icon-btn close" data-close aria-label="Close">${icon("close")}</button>
      <h2 id="dlgTitle" class="row" style="gap:10px">${icon("check")}Added to your bag</h2>
      <div class="added"><div class="media bg-${p.category}">${img(p, "", p.name)}</div><div><div style="font:400 20px/25px var(--bs-font-display)">${esc(p.name)}</div>
        <div class="small muted">${esc(p.size)} · Qty ${q} · ${inr(p.price * q)}</div><div class="small" style="margin-top:6px">Bag subtotal: ${inr(subtotal())}</div></div></div>
      <div class="row" style="flex-wrap:wrap"><a class="btn btn-primary" href="#/bag" data-close-nav>View bag</a><button class="btn btn-secondary" data-close>Continue shopping</button></div>`;
    $("#scrim").classList.add("open"); $("#app").inert = true; $("#dialog [data-close]").focus();
  }
  function closeDialog(restore = true) {
    if (!$("#scrim").classList.contains("open")) return;
    $("#scrim").classList.remove("open"); $("#app").inert = false;
    if (restore && returnTo) { const el = document.getElementById(returnTo); el && el.focus(); }
  }

  /* ---------- render ---------- */
  function render() {
    const r = parseHash(location.hash || "#/welcome/1");
    let key = r.parts[0] || "welcome"; key = ALIAS[key] || key;
    if (key === "journal" && r.parts[1] === "new") key = "journalNew";
    const v = (V[key] || V.home)(r);
    document.title = "ButterSkin · " + v.title;
    const full = !!v.full;
    ["#announce", "#header", "#tabbar", "#credit"].forEach(s => { $(s).hidden = full; });
    $("#view").innerHTML = v.html;
    $("#view").classList.toggle("full", full); $("#view").style.padding = full ? "0" : ""; $("#view").style.maxWidth = full ? "none" : "";
    $$("[data-nav]").forEach(a => a.dataset.nav === v.nav ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current"));
    $$("[data-nav-tool]").forEach(a => a.dataset.navTool === v.tool ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current"));
    const bc = bagCount(), wc = S.wish.size;
    $("#bagCount").textContent = bc || ""; $("#bagCount").hidden = !bc; $("#wishCount").textContent = wc || ""; $("#wishCount").hidden = !wc;
    $('[data-nav-tool="bag"]').setAttribute("aria-label", `Shopping bag, ${bc} item${bc === 1 ? "" : "s"}`);
    $('[data-nav-tool="wishlist"]').setAttribute("aria-label", `Wishlist, ${wc} saved`);
    wire();
  }

  function wire() {
    const pref = $("#prefForm"), note = $("#noteForm"), co = $("#coForm"), search = $("[data-search]"), sort = $("[data-sort]");
    if (pref) pref.addEventListener("submit", e => { e.preventDefault(); const f = new FormData(pref); S.profile.skin_type = f.get("skin_type"); S.profile.focus = f.get("focus");
      toast("Preferences saved for this session"); parseHash(location.hash).parts[0] === "setup" ? go("#/home") : render(); });
    if (search) search.addEventListener("submit", e => { e.preventDefault(); const u = parseHash(location.hash).q; const v = $("#q").value.trim(); v ? u.set("q", v) : u.delete("q"); go("#/shop" + (u.toString() ? "?" + u : "")); });
    if (sort) sort.addEventListener("change", () => { const u = parseHash(location.hash).q; sort.value === "featured" ? u.delete("sort") : u.set("sort", sort.value); go("#/shop" + (u.toString() ? "?" + u : "")); });
    if (note) {
      const ta = $("#note"), cnt = $("[data-count]", note), er = $("#noteErr");
      ta.addEventListener("input", () => { cnt.textContent = ta.value.length; if (ta.value.trim()) { ta.removeAttribute("aria-invalid"); er.hidden = true; ta.setAttribute("aria-describedby", "noteHint"); } });
      note.addEventListener("submit", e => { e.preventDefault();
        if (!ta.value.trim()) { ta.setAttribute("aria-invalid", "true"); ta.setAttribute("aria-describedby", "noteHint noteErr"); er.hidden = false; ta.focus(); return; }
        S.journal.unshift({ date: D.demo_date, mood: new FormData(note).get("mood"), note: ta.value.trim() }); go("#/journal"); toast("Note saved for this session"); });
    }
    if (co) {
      co.addEventListener("input", e => { if (e.target.name && e.target.name in S.checkout) S.checkout[e.target.name] = e.target.value; });
      co.addEventListener("change", e => { if (e.target.name === "delivery") { S.checkout.delivery = e.target.value; V.checkout._errs = V.checkout._errs || {}; render(); const r = $(`input[name=delivery][value=${S.checkout.delivery}]`); r && r.focus(); } });
      co.addEventListener("submit", e => { e.preventDefault(); const errs = validate(S.checkout); V.checkout._errs = errs;
        if (Object.keys(errs).length) { if (parseHash(location.hash).q.get("demo")) { history.replaceState(null, "", "#/checkout"); } render(); const s = $("#errSum"); s && s.focus(); return; }
        V.checkout._errs = {};
        const items = [...S.bag]; S.order = { ref: "BS-DEMO-2810-" + String(Math.floor(10 + Math.random() * 89)), items, total: subtotal() + deliveryFee(S.checkout.delivery), name: S.checkout.name.trim() };
        S.bag.clear(); go("#/order"); toast("Demo order placed. Nothing was charged.");
      });
    }
  }

  /* ---------- events ---------- */
  document.addEventListener("click", e => {
    const skip = e.target.closest('a.skip'); if (skip) { e.preventDefault(); $("#view").focus(); return; }
    const t = e.target.closest("[data-add],[data-wish],[data-qty],[data-remove],[data-view],[data-checkin],[data-reset],[data-add-routine],[data-restart],[data-close],[data-close-nav],[data-jump]");
    if (!t) return;
    if (t.dataset.jump) { e.preventDefault(); const f = document.getElementById(t.dataset.jump); f && f.focus(); return; }
    if (t.dataset.closeNav !== undefined) { closeDialog(false); return; }
    if (t.dataset.close !== undefined) { e.preventDefault(); closeDialog(); return; }
    if (t.dataset.add) {
      const id = t.dataset.add, q = t.dataset.qtyFrom === "pdp" ? pdpQty : 1;
      S.bag.set(id, Math.min(SHOP.max_qty, (S.bag.get(id) || 0) + q)); returnTo = t.id || null; render(); openAdded(id, q); return;
    }
    if (t.dataset.wish) {
      const id = t.dataset.wish, had = S.wish.has(id); had ? S.wish.delete(id) : S.wish.add(id);
      const sel = t.closest(".pcard") ? `.pcard [data-wish="${id}"]` : `[data-wish="${id}"]`; render(); const b = $(sel); b && b.focus();
      toast(had ? "Removed from your wishlist" : "Saved to your wishlist"); return;
    }
    if (t.dataset.qty) {
      const id = t.dataset.id, d = Number(t.dataset.d), dir = d > 0 ? "1" : "-1";
      if (t.dataset.qty === "pdp") pdpQty = Math.min(SHOP.max_qty, Math.max(1, pdpQty + d));
      else S.bag.set(id, Math.min(SHOP.max_qty, Math.max(1, S.bag.get(id) + d)));
      render(); const b = $(`[data-qty="${t.dataset.qty}"][data-id="${id}"][data-d="${dir}"]`) ; (b && !b.disabled ? b : $(`[data-qty="${t.dataset.qty}"][data-id="${id}"]:not([disabled])`))?.focus(); return;
    }
    if (t.dataset.remove) { const p = P[t.dataset.remove]; S.bag.delete(t.dataset.remove); render(); toast(`${p.name} removed from your bag`); const h = $("#view h1"); h && h.focus(); return; }
    if (t.dataset.view !== undefined) { pdpView = t.dataset.view; render(); $(`[data-view="${pdpView}"]`).focus(); return; }
    if (t.dataset.checkin) { S.checkin = t.dataset.checkin; const ex = S.journal.find(j => j.date === D.demo_date && j.auto);
      ex ? (ex.mood = S.checkin) : S.journal.unshift({ date: D.demo_date, mood: S.checkin, note: "Quick check-in from Home.", auto: true });
      render(); $(`[data-checkin="${CSS.escape(S.checkin)}"]`).focus(); toast(`Noted: ${S.checkin}. Added to your journal.`); return; }
    if (t.dataset.reset) { S.done[t.dataset.reset].clear(); render(); toast("Ticks cleared for today"); return; }
    if (t.dataset.addRoutine) { const ids = D.routines[t.dataset.addRoutine].filter(s => s.product && !S.bag.has(s.product)).map(s => s.product);
      ids.forEach(id => S.bag.set(id, 1)); render(); toast(`Added ${ids.length} product${ids.length > 1 ? "s" : ""} to your bag`); const h = $("#rbH"); h && h.focus && (h.tabIndex = -1, h.focus()); return; }
    if (t.dataset.restart !== undefined) { S = fresh(); go("#/welcome/1"); toast("Demo restarted"); }
  });
  document.addEventListener("change", e => { const c = e.target.closest("input[data-step]"); if (!c) return;
    const set = S.done[c.dataset.time]; c.checked ? set.add(c.dataset.step) : set.delete(c.dataset.step); const id = c.id; render(); document.getElementById(id).focus(); });
  document.addEventListener("keydown", e => {
    if (!$("#scrim").classList.contains("open")) return;
    if (e.key === "Escape") { e.preventDefault(); closeDialog(); return; }
    if (e.key === "Tab") { const f = $$("#dialog button, #dialog a[href]"); const a = f[0], z = f[f.length - 1];
      if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
  });
  $("#scrim").addEventListener("click", e => { if (e.target.id === "scrim") closeDialog(); });
  window.addEventListener("hashchange", () => { closeDialog(false); if (!parseHash(location.hash).parts[0] || parseHash(location.hash).parts[0] !== "checkout") V.checkout._errs = {};
    render(); window.scrollTo(0, 0); const h = $("#view h1"); h && h.focus({ preventScroll: true }); });
  render();
})();
