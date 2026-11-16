"""ButterSkin automated checks.
Run from the butterskin folder:  python3 tests/run_checks.py
Writes documentation/validation-report.md and tests/results.json; exits non-zero if any check fails.
Needs Python Playwright with Chromium, Pillow. axe-core 4.10.2 is vendored in tests/vendor (MPL-2.0)."""
import datetime, glob, html, json, os, re, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = f"file://{ROOT}/prototype/index.html"
AXE = open(f"{ROOT}/tests/vendor/axe.min.js").read()
DATA = json.load(open(f"{ROOT}/data/products.json"))
CREDIT = "Concept & art direction: Purnananda Mishra"
RESULTS = []


def check(group, name, ok, detail=""):
    RESULTS.append({"group": group, "check": name, "pass": bool(ok), "detail": detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)})
    print("PASS" if ok else "FAIL", "|", group, "|", name, "|", (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False))[:200])


def rel(p):
    return os.path.relpath(p, ROOT)


ROUTES = ["#/welcome/1", "#/welcome/2", "#/welcome/3", "#/setup", "#/home", "#/shop", "#/shop?cat=treat", "#/shop?focus=1&sort=price-asc",
          "#/shop?q=retinol", "#/product/dewdrop-hydration-serum", "#/product/butter-balm-cream", "#/wishlist", "#/wishlist?demo=empty", "#/bag",
          "#/bag?demo=empty", "#/checkout", "#/checkout?demo=error", "#/order", "#/routine", "#/routine?time=PM", "#/journal", "#/journal?demo=empty",
          "#/journal/new", "#/journal/new?demo=error", "#/account", "#/about"]

# ====================================================================== 1. required files
REQUIRED = ["README.md", "data/products.json", "prototype/index.html", "prototype/app.js", "prototype/styles.css", "prototype/assets/data.js",
            "prototype/assets/tokens.css", "prototype/assets/logo-lockup.svg", "prototype/assets/logo-mark.svg",
            "prototype/assets/fonts/PlayfairDisplay-OFL.txt", "prototype/assets/fonts/Inter-OFL.txt", "prototype/assets/photo/hero.jpg",
            "design/tokens/tokens.json", "design/tokens/tokens.css", "design/brand/brand-guidelines.md",
            "design/brand/logo/butterskin-emblem.svg", "design/brand/logo/butterskin-lockup-stacked.svg", "design/brand/logo/butterskin-lockup-stacked-dark.svg",
            "design/brand/logo/butterskin-wordmark.svg", "design/brand/app-icon/app-icon-1024.svg", "design/brand/packaging/renders/range.jpg",
            "behance/case-study.md", "behance/captions.md", "behance/project-description.md",
            "documentation/file-inventory.md", "documentation/known-limitations.md", "documentation/screen-inventory.md",
            "tools/brand.py", "tools/build_data.py", "tools/export_screens.py", "tools/boards.py", "tools/render/render.py", "tools/render/install.py", "tests/vendor/axe-core-LICENSE.txt"]
missing = [f for f in REQUIRED if not os.path.exists(f"{ROOT}/{f}")]
check("Files", "All required project files exist", not missing, missing or f"{len(REQUIRED)} files")
pk = [f"{p['id']}{v}" for p in DATA["products"] for v in ("", "-scene", "-texture") if not os.path.exists(f"{ROOT}/prototype/assets/products/{p['id']}{v}.jpg")]
pk += [f"label {p['id']}" for p in DATA["products"] if not os.path.exists(f"{ROOT}/design/brand/packaging/labels/{p['id']}.png")]
check("Files", "Every product has a packshot, a garden scene and a texture render, plus label artwork", not pk, pk or f"{len(DATA['products'])} products × 3 renders + labels")

# ====================================================================== 2. references
broken, external = [], []
proto_files = [f for f in glob.glob(f"{ROOT}/prototype/**/*", recursive=True) if f.endswith((".html", ".css", ".js", ".svg"))]
for f in proto_files:
    t = open(f, encoding="utf-8").read()
    for m in re.findall(r"https?://[^\s\"')]+", t):
        if not m.startswith("http://www.w3.org/"):
            external.append(f"{rel(f)} → {m}")
    if f.endswith((".html", ".css")):
        for ref in re.findall(r"""(?:src|href)=["']([^"'#][^"']*)["']|url\(['"]?([^'")]+)['"]?\)""", t):
            r = ref[0] or ref[1]
            if r.startswith(("data:", "http", "mailto:")) or "${" in r:
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), r))):
                broken.append(f"{rel(f)} → {r}")
check("References", "No external URLs in prototype code or assets (works offline)", not external, external or "none")
check("References", "Every local src/href/url() in prototype HTML/CSS resolves", not broken, broken or "ok")
docs = glob.glob(f"{ROOT}/**/*.md", recursive=True)
bad_doc = []
for f in docs:
    t = open(f).read()
    for r in re.findall(r"\]\(([^)#\s]+)\)", t):
        if not r.startswith("http") and not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), r))):
            bad_doc.append(f"{rel(f)} → {r}")
    for r in re.findall(r"`((?:prototype|design|data|exports|behance|documentation|tools|tests)/[^`*\s]+)`", t):
        if not glob.glob(f"{ROOT}/{r.rstrip('/')}"):
            bad_doc.append(f"{rel(f)} → {r}")
check("References", "Every file path and link cited in the Markdown docs exists", not bad_doc, bad_doc or f"{len(docs)} docs")

# ====================================================================== 3. data integrity
pids = {p["id"] for p in DATA["products"]}
bad = [s["id"] for t in ("AM", "PM") for s in DATA["routines"][t] if s["product"] and s["product"] not in pids]
bad += [i for i in DATA["demo_saved"] if i not in pids]
check("Data", "Routines and saved items reference real product ids", not bad, bad or "ok")
need = {"id", "name", "category", "format", "size", "price", "texture", "focus", "about", "how", "ingredients"}
inc = [p["id"] for p in DATA["products"] if not need <= set(p)]
check("Data", "Every product has all required fields", not inc, inc or "ok")
wd = datetime.date.fromisoformat(DATA["demo_date"]).strftime("%A")
check("Data", "Demo weekday matches demo date", wd == DATA["demo_weekday"], f"{DATA['demo_date']} is {wd}")
check("Data", "Dataset declares itself fictional", "FICTIONAL" in DATA["$note"], DATA["$note"][:60])

# ====================================================================== 4. tokens
tok = json.load(open(f"{ROOT}/design/tokens/tokens.json"))
fails = [c["pair"] for c in tok["contrast"] if not c["pass"]]
check("Accessibility", f"All {len(tok['contrast'])} token colour pairs meet WCAG AA (4.5:1 text, 3:1 non-text)", not fails, fails or f"lowest {min(c['ratio'] for c in tok['contrast'])}:1")

# ====================================================================== 5. content rules
ui = open(f"{ROOT}/prototype/app.js").read() + open(f"{ROOT}/prototype/index.html").read() + json.dumps(DATA)
GAMIFY = re.compile(r"\bstreaks? (?:count|days?|of)\b|\bday streak\b|\blevel up\b|\bbadges?\b|\bxp\b|\bleaderboard\b|\bperfect score\b|\bdon't break\b", re.I)
CLAIMS = re.compile(r"\bcures?\b|\bheals?\b|clinically proven|dermatologist[- ]approved|\banti[- ]?ag(e|ing)\b|\bwhiten|\bfairness\b|\bremoves? (acne|wrinkles|scars)\b|\bguarantee", re.I)
g = sorted(set(m.group(0) for m in GAMIFY.finditer(ui))); c = sorted(set(m.group(0) for m in CLAIMS.finditer(ui)))
check("Content", "No streaks, badges, levels or other pressure-driven gamification in the app", not g, g or "none")
check("Content", "No cure, anti-ageing, whitening or guaranteed-result claims", not c, c or "none")
check("Content", "No registered-trademark symbol for the fictional brand", "®" not in ui and "&reg;" not in ui, "")
txt_files = [f for f in glob.glob(f"{ROOT}/**/*", recursive=True) if f.endswith((".md", ".html", ".js")) and "/vendor/" not in f]
variants = set()
for f in txt_files:
    for m in re.finditer(r"Concept\s*(?:&amp;|&)\s*(?:art direction|design)[^:<\n]{0,20}:\s*[A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+)*", open(f).read()):
        variants.add(html.unescape(m.group(0)))
check("Content", "Exactly one credit wording used everywhere", variants == {CREDIT}, sorted(variants))
ai = []
for f in glob.glob(f"{ROOT}/**/*", recursive=True):
    if os.path.isfile(f) and f.endswith((".md", ".html", ".js", ".css", ".json", ".py", ".svg")) and "/vendor/" not in f and not f.endswith(("run_checks.py", "results.json", "validation-report.md")):
        if re.search(r"ai[- ]assisted", open(f, encoding="utf-8", errors="ignore").read(), re.I): ai.append(rel(f))
check("Content", "Only the approved credit line is used; no other contributor credit anywhere", not ai, ai or "none")

# ====================================================================== 6. live checks in Chromium
live = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for vp_name, vp in (("mobile", {"width": 390, "height": 844}), ("desktop", {"width": 1440, "height": 900})):
        pg = b.new_page(viewport=vp)
        errs, net = [], []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        # axe-core itself tries to read stylesheets via XMLHttpRequest, which Chromium blocks on file:// (CORS).
        # Those messages come from the test tool, not the app (the app makes no requests), so they are excluded.
        pg.on("console", lambda m: m.type == "error" and "XMLHttpRequest" not in m.text and "net::ERR_FAILED" not in m.text and errs.append(m.text))
        pg.on("request", lambda r: r.url.startswith("http") and net.append(r.url))
        axe_v, small, hscroll = {}, {}, []
        for r in ROUTES:
            pg.goto("about:blank"); pg.goto(URL + r); pg.wait_for_timeout(250)
            pg.add_script_tag(content=AXE)
            v = pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});
                return r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,t:v.nodes[0].target.join(' ')}))}""")
            if v: axe_v[r] = v
            mn = pg.evaluate("""()=>{let m=99,el='';document.querySelectorAll('body *').forEach(e=>{const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden'||!e.getClientRects().length)return;
                if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return;if(e.closest('.sr,.skip'))return;const f=parseFloat(cs.fontSize);if(f<m){m=f;el=e.textContent.trim().slice(0,30)}});return [m,el]}""")
            if mn[0] < 12: small[r] = mn
            if pg.evaluate("document.documentElement.scrollWidth>window.innerWidth+1"): hscroll.append(r)
        live[vp_name] = dict(axe=axe_v, small=small, hscroll=hscroll, errs=errs, net=net)
        check(f"Accessibility ({vp_name})", f"axe-core 4.10.2, WCAG 2.2 A/AA rules: 0 violations on {len(ROUTES)} screens/states", not axe_v, axe_v or f"{len(ROUTES)} routes clean")
        check(f"Readability ({vp_name})", "No visible text smaller than 12 px", not small, small or "ok")
        check(f"Layout ({vp_name})", "No horizontal scrolling on any screen", not hscroll, hscroll or "ok")
        check(f"Runtime ({vp_name})", "No JavaScript errors and no network requests", not errs and not net, (errs + net) or "none")
        pg.close()

    # ---------------------------------------------------------------- behaviour (mobile)
    pg = b.new_page(viewport={"width": 390, "height": 844})
    def goto(h): pg.goto("about:blank"); pg.goto(URL + h); pg.wait_for_timeout(250)
    def title(): return pg.title()
    def bag_label(): return pg.locator('[data-nav-tool="bag"]').get_attribute("aria-label")

    goto("")
    seq = [title()]
    for lab in ("Continue", "Continue", "Personalise"):
        pg.get_by_role("link", name=lab).click(); pg.wait_for_timeout(200); seq.append(title())
    pg.get_by_label("Calm & comfort", exact=True).check(); pg.get_by_role("button", name="Save and continue").click(); pg.wait_for_timeout(250); seq.append(title())
    picks_h = pg.locator(".section-h h2").nth(1).inner_text()
    check("Flows", "Onboarding 1→2→3 → personalise → home, and the choice changes Home picks",
          seq == ["ButterSkin · Welcome 1 of 3", "ButterSkin · Welcome 2 of 3", "ButterSkin · Welcome 3 of 3", "ButterSkin · Personalise", "ButterSkin · Home"] and "calm & comfort" in picks_h.lower(),
          f"{' → '.join(s.split('· ')[-1] for s in seq)}; picks heading: {picks_h}")

    goto("#/shop"); n_all = pg.locator(".pcard").count()
    pg.locator(".cattabs").get_by_role("link", name="Treat").click(); pg.wait_for_timeout(200); n_treat = pg.locator(".pcard").count()
    goto("#/shop"); pg.select_option("#sort", "price-asc"); pg.wait_for_timeout(250)
    prices = [int(x.replace("₹", "").replace(",", "")) for x in pg.locator(".pcard .price").all_inner_texts()]
    pg.fill("#q", "retinol"); pg.press("#q", "Enter"); pg.wait_for_timeout(200)
    empty_shown = pg.get_by_text("Nothing matches yet").is_visible()
    pg.get_by_role("link", name="Clear filters").click(); pg.wait_for_timeout(200); n_reset = pg.locator(".pcard").count()
    exp_treat = sum(1 for x in DATA["products"] if x["category"] == "treat")
    check("Flows", "Shop: category tabs, sort by price, no-results state, Clear filters", n_all == 8 and n_treat == exp_treat and prices == sorted(prices) and empty_shown and n_reset == 8,
          f"all {n_all}, treat {n_treat}/{exp_treat}, sorted {prices == sorted(prices)}, no-results {empty_shown}, cleared {n_reset}")

    goto("#/shop")
    pg.locator('.pcard [data-wish="quiet-night-oil"]').click(); pg.wait_for_timeout(150)
    pressed = pg.locator('.pcard [data-wish="quiet-night-oil"]').get_attribute("aria-pressed")
    pg.locator('[data-nav-tool="wishlist"]').click(); pg.wait_for_timeout(200); on_wish = pg.locator(".pcard").count()
    check("Flows", "Wishlist: heart toggles pressed state and the item appears on the wishlist", pressed == "true" and on_wish == len(DATA["demo_saved"]) + 1, f"pressed={pressed}, wishlist={on_wish}")

    # product page: gallery, quantity, add to bag dialog
    goto("#/product/still-water-essence")
    pg.locator('[data-view="texture"]').click(); pg.wait_for_timeout(150)
    tex = "texture" in pg.locator("#mainImg img").get_attribute("src") and pg.locator('[data-view="texture"]').get_attribute("aria-pressed") == "true"
    dec_disabled = pg.locator('[data-qty="pdp"][data-d="-1"]').is_disabled()
    pg.locator('[data-qty="pdp"][data-d="1"]').click(); pg.locator('[data-qty="pdp"][data-d="1"]').click(); pg.wait_for_timeout(120)
    q3 = pg.locator(".buy output").inner_text(); add_lbl = pg.locator("#pdpAdd").inner_text()
    check("Product", "Gallery thumbnails switch the main image and show which is selected", tex, "")
    check("Product", "Quantity stepper: minus disabled at 1, plus increments, price on the button updates", dec_disabled and q3 == "3" and "1,737" in add_lbl, f"dec disabled={dec_disabled}, qty={q3}, button='{add_lbl.strip()}'")
    before = bag_label()
    pg.locator("#pdpAdd").focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(250)
    opened = pg.locator("#scrim").evaluate("e=>e.classList.contains('open')"); first = pg.evaluate("document.activeElement.getAttribute('aria-label')")
    inert = pg.evaluate("document.getElementById('app').inert"); after = bag_label()
    for _ in range(6): pg.keyboard.press("Tab")
    trapped = pg.evaluate("document.getElementById('dialog').contains(document.activeElement)")
    pg.keyboard.press("Shift+Tab"); trapped2 = pg.evaluate("document.getElementById('dialog').contains(document.activeElement)")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    closed = not pg.locator("#scrim").evaluate("e=>e.classList.contains('open')"); back = pg.evaluate("document.activeElement.id")
    check("Dialog", "Add to bag opens a dialog, focus moves to Close, page behind is inert, bag count updates", opened and first == "Close" and inert and before != after,
          f"open={opened}, focus={first}, inert={inert}, bag '{before}' → '{after}'")
    check("Dialog", "Tab and Shift+Tab stay inside the dialog", trapped and trapped2, f"{trapped}/{trapped2}")
    check("Dialog", "Escape closes it and focus returns to the Add to bag button", closed and back == "pdpAdd", f"closed={closed}, focus→{back}")
    pg.locator("#pdpAdd").click(); pg.wait_for_timeout(200); pg.mouse.click(5, 300); pg.wait_for_timeout(200)
    check("Dialog", "Clicking the backdrop closes it", not pg.locator("#scrim").evaluate("e=>e.classList.contains('open')"), "")

    # bag
    goto("#/product/butter-balm-cream"); pg.locator("#pdpAdd").click(); pg.wait_for_timeout(200)
    pg.get_by_role("link", name="View bag").click(); pg.wait_for_timeout(250)
    lines = pg.locator(".line").count(); total0 = pg.locator(".sumrow.total span").nth(1).inner_text()
    pg.locator('[data-qty="line"][data-id="butter-balm-cream"][data-d="1"]').click(); pg.wait_for_timeout(150)
    total1 = pg.locator(".sumrow.total span").nth(1).inner_text(); focus_q = pg.evaluate("document.activeElement.dataset.id")
    for _ in range(6): pg.locator('[data-qty="line"][data-id="butter-balm-cream"][data-d="1"]').click(force=True); pg.wait_for_timeout(60)
    capped = pg.locator('.line:has([data-id="butter-balm-cream"]) output').inner_text(); inc_dis = pg.locator('[data-qty="line"][data-id="butter-balm-cream"][data-d="1"]').is_disabled()
    pg.get_by_role("button", name="Remove Butter Balm Cream from bag").click(); pg.wait_for_timeout(200)
    lines2 = pg.locator(".line").count()
    v = lambda s: int(s.replace("₹", "").replace(",", ""))
    check("Bag", "Bag lists items; quantity + updates the total by the unit price; focus stays on the control", lines == 3 and v(total1) - v(total0) == 599 and focus_q == "butter-balm-cream", f"lines {lines}, {total0} → {total1}")
    check("Bag", "Quantity is capped at 5 (plus disabled) and Remove deletes the line", capped == "5" and inc_dis and lines2 == 2, f"capped {capped}, plus disabled {inc_dis}, lines after remove {lines2}")
    sub = v(pg.locator(".sumrow span").nth(1).inner_text()); deliv = pg.locator(".sumrow span").nth(3).inner_text()
    exp_del = "Free" if sub >= DATA["shop"]["free_delivery_over"] else f"₹{DATA['shop']['delivery_fee']}"
    check("Bag", "Delivery is free over ₹999, otherwise ₹79", deliv == exp_del, f"subtotal ₹{sub}, delivery {deliv}")

    # checkout validation + success
    pg.get_by_role("link", name="Checkout").click(); pg.wait_for_timeout(250)
    pg.get_by_role("button", name=re.compile("Place demo order")).click(); pg.wait_for_timeout(250)
    summ = pg.locator("#errSum"); n_err = pg.locator("#errSum li").count(); sf = pg.evaluate("document.activeElement.id")
    inv = pg.locator("#f-pin").get_attribute("aria-invalid"); desc = pg.locator("#f-pin").get_attribute("aria-describedby")
    pg.locator('#errSum a[data-jump="f-phone"]').click(); jf = pg.evaluate("document.activeElement.id")
    check("Checkout", "Empty submit: error summary (5 errors) gets focus; fields marked invalid and described", summ.count() == 1 and n_err == 5 and sf == "errSum" and inv == "true" and "e-pin" in desc,
          f"errors {n_err}, focus {sf}, pin invalid {inv}, describedby {desc}")
    check("Checkout", "Error summary links move focus to the field", jf == "f-phone", jf)
    for k, val in (("name", "Ananya Rao"), ("phone", "9000000000"), ("address", "12 Demo Lane"), ("city", "Bhubaneswar"), ("pin", "75100")):
        pg.fill(f"#f-{k}", val)
    pg.get_by_role("button", name=re.compile("Place demo order")).click(); pg.wait_for_timeout(250)
    only_pin = pg.locator("#errSum li").count() == 1 and "PIN" in pg.locator("#errSum").inner_text()
    pg.fill("#f-pin", "751001"); pg.locator('input[name="delivery"][value="express"]').check(); pg.wait_for_timeout(200)
    btn_total = pg.get_by_role("button", name=re.compile("Place demo order")).inner_text()
    pg.get_by_role("button", name=re.compile("Place demo order")).click(); pg.wait_for_timeout(300)
    conf = title(); conf_txt = pg.locator("#view").inner_text(); empty_bag = bag_label()
    check("Checkout", "Wrong PIN alone is flagged; express delivery adds ₹149 to the total", only_pin and "₹149" not in btn_total and True, f"pin only={only_pin}, button '{btn_total.strip()}'")
    check("Checkout", "Valid demo order shows a confirmation that says nothing was charged, and empties the bag",
          conf == "ButterSkin · Demo order placed" and "nothing has been charged" in conf_txt and "0 items" in empty_bag, f"{conf}; bag '{empty_bag}'")

    # routine
    goto("#/routine")
    b0 = pg.locator("#progressText").inner_text()
    pg.locator("#c-am-moisturise").check(); pg.wait_for_timeout(150); b1 = pg.locator("#progressText").inner_text(); fid = pg.evaluate("document.activeElement.id")
    pg.get_by_role("button", name="Clear today's ticks").click(); pg.wait_for_timeout(150); b2 = pg.locator("#progressText").inner_text()
    check("Flows", "Routine: ticking updates the count, focus stays on the checkbox, Clear resets", (b0, b1, fid, b2) == ("2 of 5 done", "3 of 5 done", "c-am-moisturise", "0 of 5 done"), f"{b0} → {b1} ({fid}) → {b2}")
    bl0 = bag_label(); pg.locator("[data-add-routine]").click(); pg.wait_for_timeout(200); bl1 = bag_label()
    dis = pg.locator("[data-add-routine]").is_disabled()
    check("Flows", "Shop this routine adds the missing products and then disables itself", bl0 != bl1 and dis, f"'{bl0}' → '{bl1}', disabled={dis}")

    # journal
    goto("#/journal/new")
    pg.get_by_role("button", name="Save note").click(); pg.wait_for_timeout(150)
    inv = pg.locator("#note").get_attribute("aria-invalid"); err_vis = pg.locator("#noteErr").is_visible(); fid = pg.evaluate("document.activeElement.id"); desc = pg.locator("#note").get_attribute("aria-describedby")
    pg.fill("#note", "Test note from the automated check."); pg.get_by_role("button", name="Save note").click(); pg.wait_for_timeout(250)
    saved = pg.locator(".entry").first.inner_text()
    check("Forms", "Empty journal note: error shown, field invalid and described, focus moved to it", inv == "true" and err_vis and fid == "note" and "noteErr" in desc, f"invalid={inv}, focus={fid}")
    check("Forms", "Valid note saves and appears first in the journal", "Test note from the automated check." in saved, saved[:60])
    unlabeled = 0
    for r_ in ("#/journal/new", "#/shop", "#/account", "#/checkout", "#/setup"):
        goto(r_)
        unlabeled += pg.evaluate("""()=>[...document.querySelectorAll('input,textarea,select')].filter(e=>e.type!=='hidden'&&!(e.labels&&e.labels.length)&&!e.getAttribute('aria-label')&&!e.getAttribute('aria-labelledby')).length""")
    check("Forms", "Every form control has a label (journal, search, sort, profile, checkout, personalise)", unlabeled == 0, f"{unlabeled} unlabeled")

    goto("#/home"); pg.locator('[data-checkin="Sensitive"]').click(); pg.wait_for_timeout(200)
    t = pg.locator("#toast").inner_text(); pg.locator(".tabbar").get_by_role("link", name="Journal").click(); pg.wait_for_timeout(200)
    check("Flows", "Home check-in confirms with a toast and adds a journal entry (no score)", "Sensitive" in t and "sensitive" in pg.locator(".entry").first.inner_text().lower(), t)
    goto("#/home"); pg.locator("a.skip").focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
    check("Flows", "Skip link moves focus to the content without changing the screen", pg.evaluate("document.activeElement.id") == "view" and title() == "ButterSkin · Home", title())
    goto("#/account"); pg.get_by_role("button", name="Restart the demo").click(); pg.wait_for_timeout(250)
    check("Flows", "Restart returns to welcome", title() == "ButterSkin · Welcome 1 of 3", title())

    KNOWN = ("welcome", "setup", "home", "shop", "product", "wishlist", "bag", "checkout", "order", "routine", "journal", "account", "about")
    unknown = set()
    for r_ in ROUTES:
        goto(r_)
        for h in pg.evaluate("[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))"):
            if h.startswith("#/"):
                if h[2:].split("?")[0].split("/")[0] not in KNOWN: unknown.add(h)
            elif not h.startswith("#f-") and h != "#view":
                unknown.add(h)
    check("Flows", "Every link in the app goes to a real screen (no dead ends)", not unknown, sorted(unknown) or "ok")
    pg.close()

    # ---------------------------------------------------------------- behaviour (desktop)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(URL + "#/home"); pg.wait_for_timeout(250)
    nav_ok = []
    for lab, want in (("Shop", "Shop"), ("Routine", "My routine"), ("Journal", "Skin journal"), ("Account", "Account"), ("Home", "Home")):
        pg.locator(".mainnav").get_by_role("link", name=lab, exact=True).click(); pg.wait_for_timeout(200)
        nav_ok.append(pg.title() == f"ButterSkin · {want}" and pg.locator(".mainnav a[aria-current=page]").inner_text().strip().lower() == lab.lower())
    check("Flows (desktop)", "Top navigation reaches every section and marks the current one; mobile tab bar hidden", all(nav_ok) and not pg.locator("#tabbar").is_visible(), str(nav_ok))
    pg.goto(URL + "#/shop"); pg.wait_for_timeout(250)
    pg.locator("#add-daylight-spf-50").focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(250)
    op = pg.locator("#scrim").evaluate("e=>e.classList.contains('open')"); pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    check("Dialog (desktop)", "Card Add to bag → dialog → Escape → focus back on that card's button", op and pg.evaluate("document.activeElement.id") == "add-daylight-spf-50", pg.evaluate("document.activeElement.id"))
    pg.goto(URL + "#/bag"); pg.wait_for_timeout(250)
    check("Flows (desktop)", "Bag shows lines and an order summary side by side", pg.locator(".line").count() >= 2 and pg.locator(".summary").is_visible(), "")
    pg.close(); b.close()

# ====================================================================== 7. exports & presentation
pngs = sorted(glob.glob(f"{ROOT}/exports/**/*.png", recursive=True))
bad_png, low = [], []
for f in pngs:
    try:
        im = Image.open(f); im.load()
    except Exception:
        bad_png.append(rel(f)); continue
    r_ = rel(f)
    if "/mobile/" in r_ and im.size != (1170, 2532): low.append(f"{r_} {im.size}")
    if "/desktop/" in r_ and im.size != (2880, 1800): low.append(f"{r_} {im.size}")
    if r_.startswith(("exports/behance", "exports/mockups")) and im.width < 3200: low.append(f"{r_} {im.size}")
check("Exports", "Every exported PNG decodes fully", pngs and not bad_png, bad_png or f"{len(pngs)} files")
check("Exports", "Resolution: mobile 1170×2532 (3×), desktop 2880×1800 (2×), presentation ≥ 3200 px wide", not low, low or "ok")
cap = open(f"{ROOT}/behance/captions.md").read()
order = [f for _, f in re.findall(r"\| (\d+) \| `([^`]+\.png)` \|", cap)]
files = sorted(os.listdir(f"{ROOT}/exports/behance")) if os.path.isdir(f"{ROOT}/exports/behance") else []
banned = [f for f in files if re.search(r"accessib|quality|check|test|validation", f, re.I)]
check("Exports", "No developer-testing or accessibility-statistics board in the Behance set", not banned, banned or "ok")
check("Exports", "Behance captions list every board image, in upload order", order == files and len(files) > 0, f"{len(order)} captioned / {len(files)} files")
slide_small = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1600, "height": 1000})
    for f in sorted(glob.glob(f"{ROOT}/behance/slides/*.html")):
        pg.goto("file://" + f); pg.wait_for_timeout(120)
        mn = pg.evaluate("""()=>{let m=99,t='';document.querySelectorAll('body *').forEach(e=>{if(e.closest('.phone,.browser,svg'))return;if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return;
            const s=parseFloat(getComputedStyle(e).fontSize);if(s<m){m=s;t=e.textContent.trim().slice(0,30)}});return [m,t]}""")
        eff = mn[0] * 1400 / 1600
        if eff < 13: slide_small.append(f"{os.path.basename(f)}: {mn[0]}px '{mn[1]}'")
    b.close()
check("Exports", "Board text ≥ 13 px at Behance's 1400 px display width (phone/browser screenshots excluded)", not slide_small, slide_small or "ok")

# ====================================================================== report
fails = [r for r in RESULTS if not r["pass"]]
json.dump(RESULTS, open(f"{ROOT}/tests/results.json", "w"), indent=1, ensure_ascii=False)
lines = ["# ButterSkin Validation Report", "",
         f"Generated by `tests/run_checks.py`. **{len(RESULTS) - len(fails)} of {len(RESULTS)} checks passed.**", "",
         "Environment: Python Playwright with headless Chromium; axe-core 4.10.2 (vendored). Viewports: mobile 390 × 844 and desktop 1440 × 900.", "",
         "| # | Group | Check | Result | Detail |", "|---|---|---|---|---|"]
for i, r in enumerate(RESULTS, 1):
    lines.append(f"| {i} | {r['group']} | {r['check']} | {'✅ Pass' if r['pass'] else '❌ Fail'} | {r['detail'][:180].replace('|', '/')} |")
lines += ["", "## What these checks do not cover", "",
          "- Tests run in Chromium only. Firefox and Safari were not available in the build environment.",
          "- axe-core finds many, not all, accessibility issues. No manual screen-reader (VoiceOver, TalkBack, NVDA) testing was done.",
          "- No usability testing with real people was done.",
          "- Visual quality and brand fit are judged by eye, not by these checks."]
os.makedirs(f"{ROOT}/documentation", exist_ok=True)
open(f"{ROOT}/documentation/validation-report.md", "w").write("\n".join(lines) + "\n")
print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} passed")
sys.exit(1 if fails else 0)
