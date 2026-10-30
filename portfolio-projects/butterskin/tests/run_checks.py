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
CREDIT = "Concept & art direction: Purnananda Mishra · AI-assisted design and production"
RESULTS = []


def check(group, name, ok, detail=""):
    RESULTS.append({"group": group, "check": name, "pass": bool(ok), "detail": detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)})
    print("PASS" if ok else "FAIL", "|", group, "|", name, "|", (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False))[:200])


def rel(p):
    return os.path.relpath(p, ROOT)


ROUTES = ["#/welcome/1", "#/welcome/2", "#/welcome/3", "#/setup", "#/home", "#/routine", "#/routine?time=PM", "#/discover",
          "#/discover?cat=treat", "#/discover?focus=1", "#/discover?q=retinol", "#/shelf", "#/shelf?demo=empty", "#/journal",
          "#/journal?demo=empty", "#/journal/new", "#/journal/new?demo=error", "#/profile", "#/about", "#/product/butter-balm-cream"]

# ====================================================================== 1. required files
REQUIRED = ["README.md", "data/products.json", "prototype/index.html", "prototype/app.js", "prototype/styles.css", "prototype/assets/data.js",
            "prototype/assets/tokens.css", "prototype/assets/logo-lockup.svg", "prototype/assets/logo-mark.svg",
            "prototype/assets/fonts/DMSans-OFL.txt", "prototype/assets/fonts/PlayfairDisplay-OFL.txt",
            "design/tokens/tokens.json", "design/tokens/tokens.css", "design/brand/brand-guidelines.md",
            "design/brand/logo/butterskin-mark.svg", "design/brand/logo/butterskin-lockup-light.svg", "design/brand/logo/butterskin-lockup-dark.svg",
            "design/brand/logo/butterskin-wordmark.svg", "design/brand/app-icon/app-icon-1024.svg", "design/brand/packaging/family-lineup.svg",
            "behance/case-study.md", "behance/captions.md", "behance/project-description.md",
            "documentation/file-inventory.md", "documentation/known-limitations.md", "documentation/screen-inventory.md",
            "tools/brand.py", "tools/build_data.py", "tools/export_screens.py", "tools/boards.py", "tests/vendor/axe-core-LICENSE.txt"]
missing = [f for f in REQUIRED if not os.path.exists(f"{ROOT}/{f}")]
check("Files", "All required project files exist", not missing, missing or f"{len(REQUIRED)} files")
pk = [p["id"] for p in DATA["products"] if not (os.path.exists(f"{ROOT}/prototype/assets/packaging/{p['id']}.svg") and os.path.exists(f"{ROOT}/design/brand/packaging/{p['id']}.svg"))]
check("Files", "Every product in data has packaging art (prototype + design)", not pk, pk or f"{len(DATA['products'])} products")

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
for r in re.findall(r"assets/packaging/\$\{[^}]+\}(-scene)?\.svg", open(f"{ROOT}/prototype/app.js").read()):
    pass
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
    for m in re.finditer(r"Concept\s*(?:&amp;|&)\s*(?:art direction|design):[^<\n*\"`]*?production", open(f).read()):
        variants.add(html.unescape(m.group(0)))
check("Content", "Exactly one credit wording used everywhere", variants == {CREDIT}, sorted(variants))

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

    goto("")
    seq = [title()]
    for lab in ("Continue", "Continue", "Set up my space"):
        pg.get_by_role("link", name=lab).click(); pg.wait_for_timeout(200); seq.append(title())
    pg.get_by_label("Calm & comfort", exact=True).check(); pg.get_by_role("button", name="Continue").click(); pg.wait_for_timeout(250); seq.append(title())
    head = pg.locator("#view h2").nth(2).inner_text() if pg.locator("#view h2").count() > 2 else ""
    focus_h = pg.locator(".section-h h2").inner_text()
    check("Flows", "Onboarding 1→2→3 → setup → home, and setup choice changes Home picks",
          seq == ["ButterSkin · Welcome 1 of 3", "ButterSkin · Welcome 2 of 3", "ButterSkin · Welcome 3 of 3", "ButterSkin · Set up", "ButterSkin · Home"] and "calm & comfort" in focus_h.lower(),
          f"{' → '.join(s.split('· ')[-1] for s in seq)}; picks heading: {focus_h}")

    goto("#/routine")
    before = pg.locator(".pill[aria-live]").inner_text()
    pg.locator("#c-am-moisturise").check(); pg.wait_for_timeout(150); after = pg.locator(".pill[aria-live]").inner_text()
    still_focus = pg.evaluate("document.activeElement.id")
    pg.get_by_role("button", name="Clear today's ticks").click(); pg.wait_for_timeout(150); cleared = pg.locator(".pill[aria-live]").inner_text()
    check("Flows", "Routine: ticking updates the count, focus stays on the checkbox, Clear resets", before == "2 of 5 done" and after == "3 of 5 done" and still_focus == "c-am-moisturise" and cleared == "0 of 5 done",
          f"{before} → {after} (focus {still_focus}) → {cleared}")

    goto("#/discover"); n_all = pg.locator(".pcard").count()
    pg.get_by_role("button", name="Treat").click(); pg.wait_for_timeout(200); n_treat = pg.locator(".pcard").count()
    pg.fill("#q", "retinol"); pg.press("#q", "Enter"); pg.wait_for_timeout(200)
    empty_shown = pg.get_by_text("Nothing matches yet").is_visible()
    pg.get_by_role("link", name="Clear filters").click(); pg.wait_for_timeout(200); n_reset = pg.locator(".pcard").count()
    exp_treat = sum(1 for x in DATA["products"] if x["category"] == "treat")
    check("Flows", "Discover: category filter, no-results state and Clear filters", n_all == 8 and n_treat == exp_treat and empty_shown and n_reset == 8,
          f"all {n_all}, treat {n_treat}/{exp_treat}, no-results shown {empty_shown}, after clear {n_reset}")

    goto("#/discover")
    pg.locator('[data-save="quiet-night-oil"]').click(); pg.wait_for_timeout(150)
    pressed = pg.locator('[data-save="quiet-night-oil"]').get_attribute("aria-pressed")
    pg.get_by_role("link", name="Your shelf").click(); pg.wait_for_timeout(200)
    on_shelf = pg.locator(".pcard").count()
    check("Flows", "Saving a product updates its pressed state and the shelf", pressed == "true" and on_shelf == len(DATA["demo_saved"]) + 1, f"pressed={pressed}, shelf={on_shelf}")

    # dialog keyboard behaviour
    goto("#/discover")
    link = pg.locator('a.open[href="#/product/still-water-essence"]'); link.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(250)
    opened = pg.locator("#scrim").evaluate("e=>e.classList.contains('open')")
    first = pg.evaluate("document.activeElement.getAttribute('aria-label')")
    inert = pg.evaluate("document.getElementById('app').inert")
    for _ in range(6): pg.keyboard.press("Tab")
    trapped = pg.evaluate("document.getElementById('dialog').contains(document.activeElement)")
    pg.keyboard.press("Shift+Tab"); trapped2 = pg.evaluate("document.getElementById('dialog').contains(document.activeElement)")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    closed = not pg.locator("#scrim").evaluate("e=>e.classList.contains('open')")
    returned = pg.evaluate("document.activeElement.getAttribute('href')")
    check("Dialog", "Opens from the keyboard, moves focus inside, makes the page behind inert", opened and first == "Close" and inert, f"open={opened}, focus='{first}', inert={inert}")
    check("Dialog", "Tab and Shift+Tab stay inside the dialog", trapped and trapped2, f"{trapped}/{trapped2}")
    check("Dialog", "Escape closes it and focus returns to the product that opened it", closed and returned == "#/product/still-water-essence", f"closed={closed}, focus→{returned}")
    pg.locator('a.open[href="#/product/still-water-essence"]').click(); pg.wait_for_timeout(250)
    pg.mouse.click(5, 5); pg.wait_for_timeout(250)
    check("Dialog", "Clicking the backdrop closes it", not pg.locator("#scrim").evaluate("e=>e.classList.contains('open')"), "")
    goto("#/product/daylight-spf-50"); deep = pg.locator("#scrim").evaluate("e=>e.classList.contains('open')") and "Daylight" in pg.locator("#dlgTitle").inner_text()
    check("Dialog", "Direct link to a product opens its dialog over Discover", deep, "")

    # journal validation & save
    goto("#/journal/new")
    pg.get_by_role("button", name="Save note").click(); pg.wait_for_timeout(150)
    inv = pg.locator("#note").get_attribute("aria-invalid"); err_vis = pg.locator("#noteErr").is_visible(); fid = pg.evaluate("document.activeElement.id")
    desc = pg.locator("#note").get_attribute("aria-describedby")
    pg.fill("#note", "Test note from the automated check."); pg.get_by_role("button", name="Save note").click(); pg.wait_for_timeout(250)
    saved = pg.locator(".entry").first.inner_text()
    check("Forms", "Empty note: error shown, field marked invalid and described, focus moved to it", inv == "true" and err_vis and fid == "note" and "noteErr" in desc,
          f"invalid={inv}, error visible={err_vis}, focus={fid}, describedby={desc}")
    check("Forms", "Valid note saves and appears first in the journal", "Test note from the automated check." in saved, saved[:60])
    labels = pg.evaluate("()=>0")
    goto("#/journal/new")
    unlabeled = pg.evaluate("""()=>[...document.querySelectorAll('input,textarea,select')].filter(e=>e.type!=='hidden'&&!(e.labels&&e.labels.length)&&!e.getAttribute('aria-label')&&!e.getAttribute('aria-labelledby')).length""")
    goto("#/discover"); unlabeled += pg.evaluate("""()=>[...document.querySelectorAll('input,textarea,select')].filter(e=>!(e.labels&&e.labels.length)&&!e.getAttribute('aria-label')).length""")
    goto("#/profile"); unlabeled += pg.evaluate("""()=>[...document.querySelectorAll('input')].filter(e=>!(e.labels&&e.labels.length)).length""")
    check("Forms", "Every form control has a label (journal, search, preferences)", unlabeled == 0, f"{unlabeled} unlabeled")

    goto("#/home"); pg.locator('[data-checkin="Sensitive"]').click(); pg.wait_for_timeout(200)
    t = pg.locator("#toast").inner_text(); goto2 = None
    pg.get_by_role("link", name="Journal").click(); pg.wait_for_timeout(200)
    first_entry = pg.locator(".entry").first.inner_text()
    check("Flows", "Home check-in confirms with a toast and adds a journal entry (no score)", "Sensitive" in t and "Sensitive" in first_entry, t)
    goto("#/profile"); pg.get_by_role("button", name="Restart the demo").click(); pg.wait_for_timeout(250)
    check("Flows", "Restart returns to welcome", title() == "ButterSkin · Welcome 1 of 3", title())

    # every in-app link leads to a known route
    unknown = set()
    for r in ROUTES:
        goto(r)
        for h in pg.evaluate("[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))"):
            if h.startswith("#/"):
                k = h[2:].split("?")[0].split("/")[0]
                if k not in ("welcome", "setup", "home", "routine", "discover", "product", "shelf", "journal", "profile", "about"): unknown.add(h)
            elif h not in ("#view",):
                unknown.add(h)
    check("Flows", "Every link in the app goes to a real screen (no dead ends)", not unknown, sorted(unknown) or "ok")
    pg.close()

    # ---------------------------------------------------------------- behaviour (desktop)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(URL + "#/home"); pg.wait_for_timeout(250)
    side_ok = []
    for lab, want in (("My routine", "My routine"), ("Discover", "Discover"), ("Skin journal", "Skin journal"), ("Profile", "Profile"), ("Home", "Home")):
        pg.locator("#side").get_by_role("link", name=lab, exact=True).click(); pg.wait_for_timeout(200)
        side_ok.append(pg.title() == f"ButterSkin · {want}" and pg.locator("#side a[aria-current=page]").inner_text().strip() == lab)
    tabbar_hidden = not pg.locator("#tabbar").is_visible()
    check("Flows (desktop)", "Sidebar reaches every tab and marks the current one; mobile tab bar hidden", all(side_ok) and tabbar_hidden, f"{side_ok}, tabbar hidden={tabbar_hidden}")
    pg.locator("#side").get_by_role("link", name="Discover", exact=True).click(); pg.wait_for_timeout(200)
    a = pg.locator('a.open[href="#/product/quiet-night-oil"]'); a.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(250)
    op = pg.locator("#scrim").evaluate("e=>e.classList.contains('open')"); fo = pg.evaluate("document.activeElement.getAttribute('aria-label')")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    back = pg.evaluate("document.activeElement.getAttribute('href')")
    check("Dialog (desktop)", "Keyboard open → focus on Close → Escape → focus back on the product", op and fo == "Close" and back == "#/product/quiet-night-oil", f"open={op}, focus={fo}, back={back}")
    pg.goto(URL + "#/routine"); pg.wait_for_timeout(250)
    pg.locator("#c-am-protect").check(); pg.wait_for_timeout(150)
    check("Flows (desktop)", "Routine checkbox works at desktop width", pg.locator(".pill[aria-live]").inner_text() == "3 of 5 done", pg.locator(".pill[aria-live]").inner_text())
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
