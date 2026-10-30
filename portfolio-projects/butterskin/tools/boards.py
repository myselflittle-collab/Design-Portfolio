"""Builds device mockups (design/mockups) and Behance boards (behance/slides) and exports them at 2x.
Run from the butterskin folder after tools/export_screens.py:  python3 tools/boards.py"""
import json, os, shutil
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f"{ROOT}/data/products.json"))
TOK = json.load(open(f"{ROOT}/design/tokens/tokens.json"))
RES = json.load(open(f"{ROOT}/tests/results.json")) if os.path.exists(f"{ROOT}/tests/results.json") else []
CREDIT = "Concept &amp; art direction: Purnananda Mishra · AI-assisted design and production"
UP = "../../"


def ok(name_part):
    r = [x for x in RES if name_part in x["check"]]
    return r and all(x["pass"] for x in r)


CSS = f"""
@import url('{UP}prototype/assets/tokens.css');
@font-face{{font-family:'DM Sans';font-weight:400;src:url('{UP}prototype/assets/fonts/dm-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'DM Sans';font-weight:500;src:url('{UP}prototype/assets/fonts/dm-sans-latin-500-normal.woff2')}}
@font-face{{font-family:'DM Sans';font-weight:700;src:url('{UP}prototype/assets/fonts/dm-sans-latin-700-normal.woff2')}}
@font-face{{font-family:'DM Sans';font-weight:400;src:url('{UP}prototype/assets/fonts/dm-sans-latin-ext-400-normal.woff2');unicode-range:U+20B9}}
@font-face{{font-family:'Playfair Display';font-weight:500;src:url('{UP}prototype/assets/fonts/playfair-display-latin-500-normal.woff2')}}
@font-face{{font-family:'Playfair Display';font-weight:500;font-style:italic;src:url('{UP}prototype/assets/fonts/playfair-display-latin-500-italic.woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1600px;background:var(--bs-paper-50);color:var(--bs-ink-900);font-family:'DM Sans',sans-serif;-webkit-font-smoothing:antialiased}}
.b{{position:relative;width:1600px;padding:96px 104px 128px;overflow:hidden}}
.ey{{font:700 17px/22px 'DM Sans';letter-spacing:.16em;text-transform:uppercase;color:var(--bs-olive-600)}}
h1{{font:500 76px/82px 'Playfair Display';letter-spacing:-.025em}}
h2{{font:500 58px/64px 'Playfair Display';letter-spacing:-.02em;margin-top:16px}}
h3{{font:500 30px/36px 'Playfair Display'}}
p,li{{font:400 23px/35px 'DM Sans';color:var(--bs-ink-700)}}
.lede{{font-size:27px;line-height:41px;max-width:1120px;margin-top:20px}}
.sm{{font-size:20px;line-height:30px}}
em{{font-family:'Playfair Display';font-style:italic}}
.card{{background:var(--bs-paper-0);border:1px solid var(--bs-paper-200);border-radius:30px;padding:36px}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}.g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}}.g4{{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}}
.ftr{{position:absolute;left:104px;right:104px;bottom:44px;display:flex;justify-content:space-between;font:400 17px/24px 'DM Sans';color:var(--bs-ink-600)}}
.tag{{display:inline-flex;align-items:center;height:42px;padding:0 18px;border-radius:999px;background:var(--bs-olive-800);color:var(--bs-paper-0);font:700 16px/1 'DM Sans';letter-spacing:.06em;text-transform:uppercase}}
.tag.soft{{background:var(--bs-paper-0);color:var(--bs-ink-900)}}
.phone{{flex:none;border-radius:calc(var(--w) * .14);background:#26291F;padding:calc(var(--w) * .028);box-shadow:0 40px 80px rgba(38,41,31,.22);width:var(--w)}}
.phone img{{display:block;width:100%;border-radius:calc(var(--w) * .115)}}
.browser{{border-radius:22px;background:#fff;box-shadow:0 40px 80px rgba(38,41,31,.18);overflow:hidden;border:1px solid var(--bs-paper-200)}}
.browser .bar{{height:40px;background:var(--bs-paper-100);display:flex;align-items:center;gap:8px;padding:0 16px}}
.browser .bar i{{width:12px;height:12px;border-radius:50%;background:var(--bs-paper-200)}}
.browser img{{display:block;width:100%}}
.cap{{font:600 21px/28px 'DM Sans';color:var(--bs-ink-900);margin-top:22px}}.cap span{{display:block;font-weight:400;color:var(--bs-ink-700);font-size:19px;line-height:27px;margin-top:4px}}
.dis{{border:2px dashed var(--bs-olive-600);background:var(--bs-butter-100);border-radius:24px;padding:28px 32px}}
table{{border-collapse:collapse;width:100%}}td,th{{text-align:left;padding:13px 0;border-bottom:1px solid var(--bs-paper-200);font:400 21px/29px 'DM Sans'}}
th{{font:700 16px/22px 'DM Sans';letter-spacing:.12em;text-transform:uppercase;color:var(--bs-ink-600)}}td.r{{text-align:right}}
.sw{{border-radius:20px;height:150px;padding:16px 18px;display:flex;flex-direction:column;justify-content:space-between;font:500 18px/24px 'DM Sans'}}
"""


def phone(sid, w, folder="mobile"):
    return f'<div class="phone" style="--w:{w}px"><img src="{UP}exports/screens/{folder}/{sid}.png" alt=""></div>'


def browser(sid, w):
    return f'<div class="browser" style="width:{w}px"><div class="bar"><i></i><i></i><i></i></div><img src="{UP}exports/screens/desktop/{sid}-desktop.png" alt=""></div>'


def page(title, body, h, bg="var(--bs-paper-50)"):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head>
<body style="background:{bg}"><div class="b" style="height:{h}px;background:{bg}">{body}
<div class="ftr"><span>ButterSkin · self-initiated concept · fictional brand and products</span><span>{CREDIT}</span></div></div></body></html>"""


B = []  # (name, height, body, bg, title)
pack = lambda pid, h: f'<img src="{UP}design/brand/packaging/{pid}-scene.svg" alt="" style="height:{h}px;margin:0 -{int(h * .09)}px">'
packs = lambda ids, h: "".join(pack(i, h) for i in ids)

B.append(("01-cover", 1200, f"""
  <img src="{UP}design/brand/logo/butterskin-lockup-light.svg" alt="ButterSkin" style="height:70px">
  <h1 style="margin-top:58px;max-width:640px;font-size:80px;line-height:86px">A skincare app that lets skin <em>be</em> skin.</h1>
  <p class="lede" style="max-width:600px">Brand identity, packaging direction and app design for a calm, honest skincare companion.</p>
  <div style="display:flex;gap:12px;margin-top:34px"><span class="tag">Self-initiated concept</span><span class="tag soft">Fictional brand</span></div>
  <div style="position:absolute;left:790px;top:150px;transform:rotate(-5deg)">{phone('05-home', 350)}</div>
  <div style="position:absolute;left:1130px;top:100px;transform:rotate(4deg);z-index:2">{phone('12-product', 370)}</div>
  <div style="position:absolute;left:104px;bottom:120px;display:flex;align-items:flex-end">{packs(['cloud-milk-cleanser','dewdrop-hydration-serum','butter-balm-cream','daylight-spf-50'], 220)}</div>""",
          "var(--bs-butter-300)", "Cover"))

B.append(("02-overview", 780, f"""
  <div class="ey">Overview</div><h2>Your skin, understood. Not judged.</h2>
  <div class="g2" style="margin-top:44px;grid-template-columns:1.25fr 1fr">
    <div><p class="lede" style="margin-top:0">ButterSkin is a concept for a skincare companion app: keep a simple routine, find everyday essentials and note how your skin feels, without scores, streaks or promises.</p>
      <p style="margin-top:22px">The project covers a brand identity, a packaging system for eight fictional products, design tokens, a responsive prototype with 22 screens and states, automated accessibility and behaviour checks, and this case study.</p></div>
    <div class="dis"><h3>Concept disclaimer</h3><p style="margin-top:12px">ButterSkin is fictional. Products, formulations, prices, people and journal entries are illustrative. Nothing is sold, stored or sent, and nothing here is medical advice. No user research or usability testing was carried out.</p>
      <p class="sm" style="margin-top:16px"><b>{CREDIT}</b></p></div></div>""", "var(--bs-paper-50)", "Overview"))

B.append(("03-problem", 880, f"""
  <div class="ey">The problem · assumptions</div><h2>Skincare apps often sell perfection</h2>
  <div class="g2" style="margin-top:44px">
    <div class="card"><h3>Patterns this concept designs against</h3><ul style="margin:18px 0 0 28px">
      <li>Streaks and scores that turn care into performance</li><li>"Before and after" promises and miracle claims</li>
      <li>Long, intimidating ingredient lists with no context</li><li>Diagnosis-like quizzes that feel clinical</li></ul>
      <p class="sm" style="margin-top:18px">Framed from general product observation, as design assumptions, not research findings.</p></div>
    <div class="card"><h3>Design principles</h3><ol style="margin:18px 0 0 32px">
      <li><b>Skipping is fine.</b> Checklists, never scores</li><li><b>Where it fits,</b> not what it fixes</li>
      <li><b>Personal, not prescriptive.</b> Preferences, not diagnosis</li><li><b>Calm by default.</b> Soft colour, plain words</li>
      <li><b>Honest content.</b> Fictional and concept labels where they matter</li></ol></div></div>""", "var(--bs-paper-50)", "Problem"))

users = [("The routine starter", "Wants three or four steps that are easy to remember.", "“What do I actually need in the morning?”"),
         ("The ingredient-curious", "Reads labels but feels lost in the jargon.", "“What is niacinamide, in plain words?”"),
         ("The gentle tracker", "Notices flare-ups and wants a light way to keep notes.", "“Was my skin drier after that windy weekend?”")]
B.append(("04-users", 820, f"""
  <div class="ey">Representative needs · assumptions</div><h2>Three people, one calm space</h2>
  <p class="lede">Illustrative, assumption-based profiles used to make decisions concrete. They are not research personas, and no interviews were run.</p>
  <div class="g3" style="margin-top:40px">{''.join(f'<div class="card"><h3>{n}</h3><p class="sm" style="margin-top:10px">{d}</p><p style="margin-top:16px;color:var(--bs-olive-800)"><em>{q}</em></p></div>' for n, d, q in users)}</div>""",
          "var(--bs-paper-50)", "Users"))


def flow(title, steps, note):
    items = "".join(f'<div style="flex:none;width:260px">{phone(s, 260)}<div style="font:600 18px/24px DM Sans;margin-top:12px">{l}</div></div>'
                    + (f'<div style="align-self:center;font:500 40px Playfair Display;color:var(--bs-olive-600);margin:0 14px">→</div>' if i < len(steps) - 1 else "") for i, (s, l) in enumerate(steps))
    return f'<div class="card" style="margin-top:24px;padding:28px 32px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3>{title}</h3><span class="sm" style="color:var(--bs-ink-600)">{note}</span></div><div style="display:flex;gap:16px;margin-top:20px">{items}</div></div>'


B.append(("05-flows", 2560, f"""
  <div class="ey">Information architecture &amp; flows</div><h2>Five tabs, three core journeys</h2>
  <p class="lede">Home · Routine · Discover · Journal · Profile. Onboarding and an optional setup come first; the shelf sits behind a heart in the header.</p>
  {flow('First run', [('01-welcome-1', 'Welcome'), ('03-welcome-3', 'Honest by design'), ('04-setup', 'Optional setup'), ('05-home', 'Home')], 'Skippable at every step')}
  {flow('Morning routine', [('05-home', 'Today'), ('06-routine-am', 'Tick what you did'), ('12-product', 'Where it fits'), ('07-routine-pm', 'Evening')], 'No streak, no score')}
  {flow('Notice, don\'t judge', [('22-home-checkin', 'One-tap check-in'), ('16-journal', 'Journal'), ('18-journal-new', 'New note'), ('19-journal-error', 'Gentle validation')], 'Private, session-only')}""",
          "var(--bs-paper-50)", "Flows"))

B.append(("06-identity", 1060, f"""
  <div class="ey">Brand identity</div><h2>A soft pat of butter, holding a b</h2>
  <div class="g2" style="margin-top:40px;grid-template-columns:1.3fr 1fr">
    <div class="card" style="display:flex;flex-direction:column;justify-content:space-between;height:520px">
      <img src="{UP}design/brand/logo/butterskin-lockup-light.svg" alt="ButterSkin logo" style="height:110px;align-self:flex-start;margin-top:30px">
      <p class="sm">The mark is a <b>pat</b>: a soft square with three rounded corners and one tucked corner, tilted 8°, like a pat of butter. Inside, a serif lowercase <em>b</em> from Playfair Display. The wordmark is DM Sans Bold, lowercase and friendly.</p></div>
    <div style="display:grid;grid-template-rows:1fr 1fr;gap:28px;height:520px">
      <div style="border-radius:30px;background:var(--bs-olive-800);display:grid;place-items:center"><img src="{UP}design/brand/logo/butterskin-lockup-dark.svg" alt="" style="height:96px"></div>
      <div style="display:flex;gap:28px"><div style="flex:1;border-radius:30px;background:var(--bs-paper-100);display:grid;place-items:center"><img src="{UP}design/brand/app-icon/app-icon-rounded-preview.svg" alt="" style="height:150px"></div>
        <div style="flex:1;border-radius:30px;background:var(--bs-paper-0);border:1px solid var(--bs-paper-200);display:flex;align-items:center;justify-content:center;gap:26px">
          <img src="{UP}design/brand/logo/butterskin-mark.svg" alt="" style="height:64px"><img src="{UP}design/brand/logo/butterskin-mark.svg" alt="" style="height:36px"><img src="{UP}design/brand/logo/butterskin-mark.svg" alt="" style="height:22px"></div></div></div></div>""",
          "var(--bs-paper-50)", "Identity"))
B[-1] = (B[-1][0], 900) + B[-1][2:]

pal = [("Olive 800", "olive", "800", "#fff", "Actions, packaging caps"), ("Olive 600", "olive", "600", "#fff", "Mark, links, focus"), ("Ink 900", "ink", "900", "#fff", "Text"),
       ("Paper 50", "paper", "50", "#26291F", "Canvas"), ("Butter 300", "butter", "300", "#26291F", "Brand accent · Moisturise"),
       ("Sage 200", "sage", "200", "#26291F", "Cleanse"), ("Clay 200", "clay", "200", "#26291F", "Treat"), ("Sky 200", "sky", "200", "#26291F", "Protect")]
sw = "".join(f'<div class="sw" style="background:{TOK["color"]["palette"][g][k]};color:{fg};{"border:1px solid #E2DACB" if g == "paper" else ""}"><span>{n}</span><span><b>{TOK["color"]["palette"][g][k]}</b><br>{r}</span></div>' for n, g, k, fg, r in pal)
low = min(c["ratio"] for c in TOK["contrast"] if c["min"] >= 4.5)
low_nt = min(c["ratio"] for c in TOK["contrast"] if c["min"] < 4.5)
B.append(("07-colour-type", 1040, f"""
  <div class="ey">Colour &amp; typography</div><h2>Butter paper, botanical olive</h2>
  <div class="g4" style="margin-top:40px">{sw}</div>
  <div class="g2" style="margin-top:28px;grid-template-columns:1fr 1fr">
    <div class="card"><div style="font:500 96px/1 'Playfair Display';color:var(--bs-olive-800)">Aa</div><p class="sm" style="margin-top:10px"><b>Playfair Display</b> · editorial headlines · SIL OFL 1.1</p>
      <p style="font:500 34px/40px 'Playfair Display';color:var(--bs-ink-900);margin-top:14px">Small steps, softer days.</p></div>
    <div class="card"><div style="font:500 96px/1 'DM Sans';color:var(--bs-ink-900)">Aa</div><p class="sm" style="margin-top:10px"><b>DM Sans</b> · interface and reading · SIL OFL 1.1</p>
      <p class="sm" style="margin-top:14px">Category colour always comes with a written label. All {len(TOK['contrast'])} token pairs pass WCAG AA: the lowest text pair is {low}:1, and borders and focus rings are at least {low_nt}:1.</p></div></div>""",
          "var(--bs-paper-50)", "Colour & type"))

B.append(("08-packaging", 980, f"""
  <div class="ey">Packaging direction · fictional</div><h2>Eight concepts, one calm family</h2>
  <p class="lede">Five formats with olive caps and colour coded by category: sage to cleanse, clay to treat, butter to moisturise, sky to protect. Every label carries "concept" next to the size.</p>
  <div style="display:flex;align-items:flex-end;justify-content:center;margin-top:50px;height:420px">{packs([p['id'] for p in D['products']], 330)}</div>""",
          "var(--bs-paper-50)", "Packaging"))

B.append(("09-key-screens", 1120, f"""
  <div class="ey">Key screens</div><h2>Calm at a glance</h2>
  <div style="display:flex;gap:28px;margin-top:44px">{''.join(f'<div style="flex:1">{phone(s, 320)}<div class="cap">{t}<span>{c}</span></div></div>' for s, t, c in [
      ('05-home', 'Home', 'Today\'s routine, a no-score check-in and your shelf.'), ('06-routine-am', 'Routine', 'A checklist. Skipping is fine, and nothing carries over.'),
      ('08-discover', 'Discover', 'Search and filter eight fictional essentials.'), ('16-journal', 'Journal', 'Short private notes, never scored.')])}</div>""",
          "var(--bs-paper-50)", "Key screens"))

B.append(("10-no-pressure", 1000, f"""
  <div class="ey">Decision · no pressure</div><h2>We removed the streak</h2>
  <div class="g2" style="margin-top:40px;grid-template-columns:1fr 1.15fr;align-items:center">
    <div><p class="lede" style="margin-top:0">An earlier draft showed "Routine streak: 4 days". Streaks reward perfection and punish a missed night, which runs against the brand idea.</p>
      <ul style="margin:22px 0 0 28px"><li>Progress is shown for <b>today only</b> and resets quietly</li><li>Optional steps are marked "(optional)"</li><li>The completion message is neutral: "Nice and easy"</li><li>"Clear today's ticks" is always available</li></ul></div>
    <div style="display:flex;gap:24px;justify-content:center">{phone('06-routine-am', 300)}{phone('07-routine-pm', 300)}</div></div>""",
          "var(--bs-sage-100)", "No pressure"))

B.append(("11-honest-products", 1000, f"""
  <div class="ey">Decision · honest product content</div><h2>Where it fits, not what it fixes</h2>
  <div class="g2" style="margin-top:40px;grid-template-columns:1.15fr 1fr;align-items:center">
    <div style="display:flex;gap:24px;justify-content:center">{phone('12-product', 300)}{phone('13-product-spf', 300)}</div>
    <div><ul style="margin:0 0 0 28px"><li>Each product says which routine step it belongs to</li><li>Ingredients are explained in plain words, as what they are <em>commonly used for</em></li>
      <li>"Concept formulation" and "concept product" labels sit right where claims would usually be</li><li>A patch-test note on every product</li></ul>
      <p class="sm" style="margin-top:22px">The dialog is keyboard-complete: focus moves in, Tab stays inside, Escape closes it, and focus returns to the product you came from.</p></div></div>""",
          "var(--bs-butter-100)", "Honest products"))

B.append(("12-personal", 1120, f"""
  <div class="ey">Decision · personal, not prescriptive</div><h2>Preferences, never a diagnosis</h2>
  <div style="display:flex;gap:28px;margin-top:44px">{''.join(f'<div style="flex:1">{phone(s, 320)}<div class="cap">{t}<span>{c}</span></div></div>' for s, t, c in [
      ('04-setup', 'Optional setup', 'Two questions, "Not sure" allowed, skippable.'), ('10-discover-focus', 'Suits my focus', 'Preferences only reorder and filter.'),
      ('18-journal-new', 'New note', 'Mood chips and a short note, 280 characters.'), ('20-profile', 'Profile', 'Change preferences any time; restart the demo.')])}</div>""",
          "var(--bs-paper-50)", "Personal"))

B.append(("13-states", 1020, f"""
  <div class="ey">States</div><h2>Empty, error and confirmation, gently</h2>
  <div style="display:flex;gap:24px;margin-top:44px">{''.join(f'<div style="flex:1">{phone(s, 260)}<div class="cap">{t}<span>{c}</span></div></div>' for s, t, c in [
      ('11-discover-no-results', 'No results', 'Say what happened, offer a way out.'), ('15-shelf-empty', 'Empty shelf', 'One sentence, one action.'),
      ('17-journal-empty', 'Empty journal', 'An invitation, not a nag.'), ('19-journal-error', 'Validation', 'Error text, icon and colour, with focus.'),
      ('22-home-checkin', 'Confirmation', 'A toast, announced to screen readers.')])}</div>""",
          "var(--bs-paper-50)", "States"))

B.append(("14-responsive", 1240, f"""
  <div class="ey">Responsive</div><h2>One prototype, phone to desktop</h2>
  <p class="lede">Below 900 px a bottom tab bar replaces the sidebar, and the product dialog becomes a bottom sheet. The same code and data power both.</p>
  <div style="position:relative;height:760px;margin-top:40px">
    <div style="position:absolute;left:0;top:0">{browser('08-discover', 1120)}</div>
    <div style="position:absolute;right:0;top:110px">{phone('08-discover', 290)}</div></div>""",
          "var(--bs-paper-50)", "Responsive"))

axe_ok = ok("axe-core"); n_checks = len(RES); n_pass = sum(1 for r in RES if r["pass"])
B.append(("15-accessibility", 900, f"""
  <div class="ey">Accessibility &amp; quality checks</div><h2>Checked by machine, honest about the rest</h2>
  <div class="g2" style="margin-top:40px">
    <div class="card"><table><tr><th>Automated check</th><th style="text-align:right">Result</th></tr>
      <tr><td>axe-core 4.10.2 · WCAG 2.2 A/AA · 20 screens × 2 viewports</td><td class="r">{'0 violations' if axe_ok else 'see report'}</td></tr>
      <tr><td>Token colour pairs at AA</td><td class="r">{sum(1 for c in TOK['contrast'] if c['pass'])}/{len(TOK['contrast'])}</td></tr>
      <tr><td>Smallest text in the app</td><td class="r">{'≥ 12 px' if ok('smaller than 12') else 'see report'}</td></tr>
      <tr><td>Dialog keyboard &amp; focus tests</td><td class="r">{'pass' if ok('dialog') or ok('Escape') else 'see report'}</td></tr>
      <tr><td>All checks in the suite</td><td class="r">{n_pass}/{n_checks}</td></tr></table></div>
    <div class="card"><ul style="margin-left:28px"><li>Real checkboxes, radio groups and labels; errors linked to fields</li><li>Skip link, visible focus rings, 44 px touch targets</li>
      <li>Colour never carries meaning alone</li><li>Reduced-motion respected</li></ul>
      <p class="sm" style="margin-top:16px"><b>Not yet done:</b> testing with screen-reader users and with people in general. Tests ran in Chromium only.</p></div></div>""",
          "var(--bs-paper-50)", "Accessibility"))

B.append(("16-mockups", 1180, f"""
  <div class="ey" style="color:var(--bs-olive-800)">Final mockups</div><h2>Soft, clear, unhurried</h2>
  <div style="position:absolute;left:120px;top:330px;transform:rotate(-4deg)">{phone('09-discover-treat', 300)}</div>
  <div style="position:absolute;left:470px;top:290px">{phone('14-shelf', 310)}</div>
  <div style="position:absolute;left:830px;top:260px;z-index:2">{phone('06-routine-am', 320)}</div>
  <div style="position:absolute;left:1190px;top:310px;transform:rotate(4deg)">{phone('16-journal', 300)}</div>""",
          "var(--bs-sage-200)", "Mockups"))

B.append(("17-credits", 880, f"""
  <div class="ey">Tools, contribution &amp; limitations</div><h2>How this was made</h2>
  <div class="g3" style="margin-top:40px">
    <div class="card"><h3>Contribution</h3><p style="margin-top:12px"><b>Purnananda Mishra</b>: concept, art direction, and review at each stage.</p>
      <p style="margin-top:12px"><b>AI-assisted</b>: design production, prototype code, packaging illustration, checks and writing, under that direction.</p></div>
    <div class="card"><h3>Tools</h3><ul style="margin:12px 0 0 28px"><li>HTML, CSS, JavaScript</li><li>Python: tokens, logo and packaging generation</li><li>Playwright + Chromium: exports and tests</li><li>axe-core 4.10.2</li><li>Playfair Display &amp; DM Sans (SIL OFL)</li></ul></div>
    <div class="card"><h3>Limitations</h3><ul style="margin:12px 0 0 28px"><li>Fictional brand, products and data</li><li>No user research or usability testing</li><li>No dermatological, legal or regulatory review</li><li>Session-only prototype, no backend</li><li>Chromium-tested; English only</li></ul></div></div>""",
          "var(--bs-paper-50)", "Credits"))

MOCK = {
    "mockup-01-hero": (1100, f"""<div style="position:absolute;left:104px;top:110px;width:560px"><img src="{UP}design/brand/logo/butterskin-lockup-light.svg" alt="" style="height:60px">
      <p class="lede">Your skin, understood.</p><div style="display:flex;align-items:flex-end;margin-top:60px">{packs(['soft-gel-cleanser','still-water-essence','quiet-night-oil','soft-cloud-moisturiser'], 230)}</div></div>
      <div style="position:absolute;left:760px;top:120px;transform:rotate(-6deg)">{phone('05-home', 300)}</div>
      <div style="position:absolute;left:1080px;top:70px;transform:rotate(4deg)">{phone('08-discover', 320)}</div>""", "var(--bs-butter-300)"),
    "mockup-02-responsive": (1060, f"""<div style="position:absolute;left:104px;top:100px">{browser('05-home', 1080)}</div><div style="position:absolute;right:104px;top:220px">{phone('05-home', 280)}</div>""", "var(--bs-sage-200)"),
    "mockup-03-brand-world": (1000, f"""<div style="position:absolute;left:104px;bottom:150px;display:flex;align-items:flex-end">{packs([p['id'] for p in D['products'][:5]], 320)}</div>
      <div style="position:absolute;right:140px;top:110px">{phone('12-product', 320)}</div>""", "var(--bs-paper-100)"),
}

if __name__ == "__main__":
    SD, EB, MD, EM = f"{ROOT}/behance/slides", f"{ROOT}/exports/behance", f"{ROOT}/design/mockups", f"{ROOT}/exports/mockups"
    for d in (SD, EB, MD, EM):
        os.makedirs(d, exist_ok=True)
    for f in os.listdir(EB):
        os.remove(f"{EB}/{f}")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=2)
        for name, h, body, bg, title in B:
            f = f"{SD}/{name}.html"; open(f, "w").write(page(f"ButterSkin · {title}", body, h, bg))
            pg.goto("file://" + f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300); pg.screenshot(path=f"{EB}/{name}.png", full_page=True)
        for name, (h, body, bg) in MOCK.items():
            f = f"{MD}/{name}.html"; open(f, "w").write(page(f"ButterSkin · {name}", body, h, bg))
            pg.goto("file://" + f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300); pg.screenshot(path=f"{EM}/{name}.png", full_page=True)
        b.close()
    print("boards:", len(B), "mockups:", len(MOCK))
