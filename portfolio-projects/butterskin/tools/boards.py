"""Builds device mockups (design/mockups) and Behance boards (behance/slides) and exports them at 2x.
Run from the butterskin folder after tools/export_screens.py:  python3 tools/boards.py"""
import json, os, shutil
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f"{ROOT}/data/products.json"))
TOK = json.load(open(f"{ROOT}/design/tokens/tokens.json"))
CREDIT = "Concept &amp; art direction: Purnananda Mishra · AI-assisted design and production"
UP = "../../"


FONTS = "".join(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url('{UP}prototype/assets/fonts/{f}.woff2'){ur}}}\n" for fam, w, st, f, ur in [
    ("Jost", 400, "normal", "jost-latin-400-normal", ""), ("Jost", 500, "normal", "jost-latin-500-normal", ""), ("Jost", 600, "normal", "jost-latin-600-normal", ""),
    ("Bodoni Moda", 400, "normal", "bodoni-moda-latin-400-normal", ""), ("Bodoni Moda", 500, "normal", "bodoni-moda-latin-500-normal", ""),
    ("Bodoni Moda", 400, "italic", "bodoni-moda-latin-400-italic", ""), ("Rupee", 500, "normal", "dm-sans-latin-ext-500-normal", ";unicode-range:U+20B9")])
CSS = f"""
@import url('{UP}prototype/assets/tokens.css');
{FONTS}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1600px;color:var(--bs-charcoal-900);font-family:'Jost','Rupee',sans-serif;-webkit-font-smoothing:antialiased}}
.b{{position:relative;width:1600px;padding:96px 104px 128px;overflow:hidden}}
.ey{{font:500 17px/22px 'Jost';letter-spacing:.24em;text-transform:uppercase;color:var(--bs-champagne-700)}}
.ey::before{{content:"";display:inline-block;width:40px;height:1px;background:var(--bs-champagne-400);vertical-align:middle;margin-right:16px}}
h1{{font:400 82px/88px 'Bodoni Moda';letter-spacing:-.01em;color:var(--bs-emerald-900)}}
h2{{font:400 60px/68px 'Bodoni Moda';letter-spacing:-.01em;margin-top:18px;color:var(--bs-emerald-900)}}
h3{{font:500 30px/36px 'Bodoni Moda';color:var(--bs-emerald-900)}}
p,li{{font:400 23px/35px 'Jost','Rupee';color:var(--bs-charcoal-700)}}
.lede{{font-size:27px;line-height:41px;max-width:1120px;margin-top:20px}}
.sm{{font-size:20px;line-height:30px}}
em{{font-family:'Bodoni Moda';font-style:italic}}
b{{font-weight:600;color:var(--bs-charcoal-900)}}
.card{{background:var(--bs-porcelain-0);border:1px solid var(--bs-porcelain-200);border-radius:6px;padding:36px}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}.g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}}.g4{{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}}
.ftr{{position:absolute;left:104px;right:104px;bottom:44px;display:flex;justify-content:space-between;font:400 17px/24px 'Jost';color:var(--bs-charcoal-600);border-top:1px solid var(--bs-porcelain-200);padding-top:18px}}
.dark .ftr{{color:var(--bs-champagne-200);border-color:rgba(239,228,204,.25)}}
.dark h1,.dark h2,.dark h3{{color:var(--bs-porcelain-0)}}.dark p,.dark li{{color:var(--bs-porcelain-100)}}.dark .ey{{color:var(--bs-champagne-200)}}
.tag{{display:inline-flex;align-items:center;height:42px;padding:0 18px;border-radius:2px;background:var(--bs-emerald-800);color:var(--bs-porcelain-0);font:500 16px/1 'Jost';letter-spacing:.16em;text-transform:uppercase}}
.tag.soft{{background:transparent;color:var(--bs-emerald-900);border:1px solid var(--bs-champagne-400)}}
.phone{{flex:none;border-radius:calc(var(--w) * .14);background:#262A28;padding:calc(var(--w) * .028);box-shadow:0 40px 80px rgba(15,59,45,.20);width:var(--w)}}
.phone img{{display:block;width:100%;border-radius:calc(var(--w) * .115)}}
.browser{{border-radius:10px;background:#fff;box-shadow:0 40px 80px rgba(15,59,45,.16);overflow:hidden;border:1px solid var(--bs-porcelain-200)}}
.browser .bar{{height:40px;background:var(--bs-porcelain-100);display:flex;align-items:center;gap:8px;padding:0 16px}}
.browser .bar i{{width:12px;height:12px;border-radius:50%;background:var(--bs-porcelain-200)}}
.browser img{{display:block;width:100%}}
.cap{{font:500 21px/28px 'Jost';color:var(--bs-charcoal-900);margin-top:22px}}.cap span{{display:block;font-weight:400;color:var(--bs-charcoal-700);font-size:19px;line-height:27px;margin-top:4px}}
.dis{{border:1px solid var(--bs-champagne-400);background:var(--bs-champagne-200);border-radius:6px;padding:28px 32px}}
.sw{{border-radius:4px;height:160px;padding:16px 18px;display:flex;flex-direction:column;justify-content:space-between;font:500 18px/24px 'Jost'}}
.stage{{background:linear-gradient(180deg,var(--bs-porcelain-100),var(--bs-porcelain-200));border-radius:6px}}
.num{{font:400 19px/1 'Bodoni Moda';color:var(--bs-champagne-700);letter-spacing:.1em}}
.arrow{{align-self:center;font:400 40px 'Bodoni Moda';color:var(--bs-champagne-700);margin:0 6px}}
"""

CANVAS, SAGE, CHAMP, EMER = "var(--bs-porcelain-50)", "var(--bs-sage-100)", "var(--bs-champagne-200)", "var(--bs-emerald-800)"


def phone(sid, w, folder="mobile"):
    return f'<div class="phone" style="--w:{w}px"><img src="{UP}exports/screens/{folder}/{sid}.png" alt=""></div>'


def browser(sid, w):
    return f'<div class="browser" style="width:{w}px"><div class="bar"><i></i><i></i><i></i></div><img src="{UP}exports/screens/desktop/{sid}-desktop.png" alt=""></div>'


def page(title, body, h, bg=CANVAS):
    dark = " dark" if bg == EMER else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head>
<body style="background:{bg}"><div class="b{dark}" style="height:{h}px;background:{bg}">{body}
<div class="ftr"><span>ButterSkin · self-initiated concept · fictional brand and products</span><span>{CREDIT}</span></div></div></body></html>"""


def row(items, w, gap=28):
    return f'<div style="display:flex;gap:{gap}px;margin-top:44px">' + "".join(
        f'<div style="flex:1">{phone(s, w)}<div class="cap">{t}<span>{c}</span></div></div>' for s, t, c in items) + "</div>"


B = []  # (name, height, body, bg, title)
pack = lambda pid, h, m=.12: f'<img src="{UP}design/brand/packaging/{pid}-scene.svg" alt="" style="height:{h}px;margin:0 -{int(h * m)}px">'
packs = lambda ids, h, m=.12: "".join(pack(i, h, m) for i in ids)
P = {p["id"]: p for p in D["products"]}
rs = lambda n: f"₹{n:,}"

# 1 · cover
B.append(("01-cover", 1200, f"""
  <img src="{UP}design/brand/logo/butterskin-lockup-dark.svg" alt="ButterSkin" style="height:64px">
  <h1 style="margin-top:64px;max-width:660px">Botanical skincare, <em>beautifully</em> simple.</h1>
  <p class="lede" style="max-width:600px">Brand identity, packaging system and a shopping app for a fictional botanical skincare label.</p>
  <div style="display:flex;gap:12px;margin-top:34px"><span class="tag" style="background:var(--bs-champagne-400);color:var(--bs-emerald-900)">Self-initiated concept</span><span class="tag soft" style="color:var(--bs-porcelain-0)">Fictional brand</span></div>
  <div style="position:absolute;left:104px;bottom:120px;display:flex;align-items:flex-end">{packs(['soft-gel-cleanser','dewdrop-hydration-serum','butter-balm-cream','daylight-spf-50'], 250)}</div>
  <div style="position:absolute;left:820px;top:160px;transform:rotate(-4deg)">{phone('05-home', 340)}</div>
  <div style="position:absolute;left:1150px;top:96px;transform:rotate(3deg);z-index:2">{phone('10-product', 360)}</div>""",
          EMER, "Cover"))

# 2 · overview
B.append(("02-overview", 800, f"""
  <div class="ey">Overview</div><h2>A skincare label you can shop in one calm place</h2>
  <div class="g2" style="margin-top:44px;grid-template-columns:1.25fr 1fr">
    <div><p class="lede" style="margin-top:0">ButterSkin is a concept for a premium botanical skincare brand and its own shopping app: discover eight essentials, understand what is inside, build a morning and evening routine, and check out without friction.</p>
      <p style="margin-top:22px">The project covers brand identity, a packaging family, design tokens, and a responsive shopping prototype with {len(json.load(open(f"{ROOT}/exports/screens/manifest.json")))} mobile screens and states.</p></div>
    <div class="dis"><h3>Concept disclaimer</h3><p style="margin-top:12px">ButterSkin is fictional. Products, formulations, prices and journal entries are illustrative. Product images are rendered packaging, not photographs. The checkout is a demo: no order is placed and nothing is charged. Nothing here is medical advice, and no user research was carried out.</p>
      <p class="sm" style="margin-top:16px"><b>{CREDIT}</b></p></div></div>""", CANVAS, "Overview"))

# 3 · approach
B.append(("03-approach", 860, f"""
  <div class="ey">Design approach · assumptions</div><h2>Premium, honest and easy to buy from</h2>
  <div class="g3" style="margin-top:44px">
    <div class="card"><div class="num">01</div><h3 style="margin-top:14px">Commercially credible</h3><p class="sm" style="margin-top:12px">Clear prices, add to bag on every card, a real bag with quantities and a three-step checkout. The shop has to work like a shop.</p></div>
    <div class="card"><div class="num">02</div><h3 style="margin-top:14px">Where it fits, not what it fixes</h3><p class="sm" style="margin-top:12px">Products are placed in a routine step and ingredients are explained in plain words. No miracle claims, ratings or before-and-after.</p></div>
    <div class="card"><div class="num">03</div><h3 style="margin-top:14px">Personal, not prescriptive</h3><p class="sm" style="margin-top:12px">An optional skin profile reorders picks. It never diagnoses, and there are no scores or streaks.</p></div></div>
  <p class="sm" style="margin-top:32px;max-width:1100px">These are design assumptions from general observation of skincare retail, not findings from research or testing.</p>""",
          CANVAS, "Approach"))

# 4 · brand identity
B.append(("04-brand-identity", 1000, f"""
  <div class="ey">Brand identity</div><h2>An emerald seal with a champagne ring</h2>
  <div class="g2" style="margin-top:40px;grid-template-columns:1.3fr 1fr">
    <div class="card" style="display:flex;flex-direction:column;justify-content:space-between;height:600px">
      <img src="{UP}design/brand/logo/butterskin-lockup.svg" alt="ButterSkin logo" style="height:112px;align-self:flex-start;margin-top:40px">
      <p class="sm">The monogram is a <b>seal</b>: an emerald disc, a fine champagne ring and a Bodoni Moda <em>B</em>, like the stamp on an apothecary jar. The wordmark is Jost, set in widely tracked capitals so it reads well on a pump cap or a phone header.</p></div>
    <div style="display:grid;grid-template-rows:1fr 1fr;gap:28px;height:600px">
      <div style="border-radius:6px;background:var(--bs-emerald-800);display:grid;place-items:center"><img src="{UP}design/brand/logo/butterskin-lockup-dark.svg" alt="" style="height:84px"></div>
      <div style="display:flex;gap:28px"><div style="flex:1;border-radius:6px;background:var(--bs-champagne-200);display:grid;place-items:center"><img src="{UP}design/brand/app-icon/app-icon-rounded-preview.svg" alt="" style="height:150px"></div>
        <div style="flex:1;border-radius:6px;background:var(--bs-porcelain-0);border:1px solid var(--bs-porcelain-200);display:flex;align-items:center;justify-content:center;gap:26px">
          <img src="{UP}design/brand/logo/butterskin-monogram.svg" alt="" style="height:72px"><img src="{UP}design/brand/logo/butterskin-monogram-mono.svg" alt="" style="height:44px"><img src="{UP}design/brand/logo/butterskin-monogram.svg" alt="" style="height:26px"></div></div></div></div>""",
          CANVAS, "Brand identity"))

# 5 · colour & type
pal = [("Emerald 800", "emerald", "800", "#fff", "Primary actions, caps"), ("Emerald 900", "emerald", "900", "#fff", "Headlines, dark surfaces"), ("Charcoal 900", "charcoal", "900", "#fff", "Body text"),
       ("Champagne 700", "champagne", "700", "#fff", "Eyebrows, focus ring"), ("Porcelain 50", "porcelain", "50", "#262A28", "Canvas"), ("Sage 200", "sage", "200", "#262A28", "Secondary · Cleanse"),
       ("Champagne 200", "champagne", "200", "#262A28", "Accent · Treat"), ("Mist 200", "mist", "200", "#262A28", "Protect")]
sw = "".join(f'<div class="sw" style="background:{TOK["color"]["palette"][g][k]};color:{fg};{"border:1px solid #E6E1D6" if g in ("porcelain",) else ""}"><span>{n}</span><span><b style="color:inherit">{TOK["color"]["palette"][g][k]}</b><br>{r}</span></div>' for n, g, k, fg, r in pal)
B.append(("05-colour-type", 1060, f"""
  <div class="ey">Colour &amp; typography</div><h2>Porcelain, emerald and a touch of champagne</h2>
  <div class="g4" style="margin-top:40px">{sw}</div>
  <div class="g2" style="margin-top:28px">
    <div class="card"><div style="font:400 96px/1 'Bodoni Moda';color:var(--bs-emerald-900)">Aa</div><p class="sm" style="margin-top:10px"><b>Bodoni Moda</b> · display and product names · SIL OFL 1.1</p>
      <p style="font:400 36px/42px 'Bodoni Moda';color:var(--bs-charcoal-900);margin-top:14px">Dewdrop Hydration Serum</p></div>
    <div class="card"><div style="font:400 96px/1 'Jost';color:var(--bs-charcoal-900)">Aa</div><p class="sm" style="margin-top:10px"><b>Jost</b> · interface, labels and prices · SIL OFL 1.1</p>
      <p style="font:500 18px/24px 'Jost';letter-spacing:.14em;text-transform:uppercase;color:var(--bs-emerald-800);margin-top:16px">Add to bag · {rs(P['dewdrop-hydration-serum']['price'])}</p></div></div>""",
          CANVAS, "Colour & type"))

# 6 · packaging family
B.append(("06-packaging-family", 1000, f"""
  <div class="ey">Packaging design · fictional</div><h2>Eight essentials, one family</h2>
  <p class="lede">Five formats with brushed champagne caps. Body colour follows the routine: frosted glass to cleanse, emerald to treat, porcelain to moisturise and protect. Every label carries "concept" next to the size.</p>
  <div class="stage" style="display:flex;align-items:flex-end;justify-content:center;margin-top:44px;height:470px;padding-bottom:20px">{packs([p['id'] for p in D['products']], 380)}</div>""",
          CANVAS, "Packaging family"))

# 7 · packaging detail
hero = P["dewdrop-hydration-serum"]
tex = "".join(f'<div style="text-align:center"><div style="border-radius:6px;overflow:hidden;background:var(--bs-porcelain-0);border:1px solid var(--bs-porcelain-200)"><img src="{UP}design/brand/packaging/{i}-texture.svg" alt="" style="display:block;width:100%"></div><div class="cap" style="margin-top:12px">{P[i]["name"]}<span>{P[i]["texture"]}</span></div></div>'
              for i in ["cloud-milk-cleanser", "dewdrop-hydration-serum", "butter-balm-cream"])
B.append(("07-packaging-label", 1100, f"""
  <div class="ey">Packaging design · label system</div><h2>One label, read in a second</h2>
  <div class="g2" style="margin-top:40px;grid-template-columns:1fr 1.2fr;align-items:start">
    <div class="stage" style="height:700px;display:grid;place-items:center"><img src="{UP}design/brand/packaging/{hero['id']}.svg" alt="" style="height:600px"></div>
    <div><ol style="margin:0 0 0 30px"><li><b>Brand</b> in tracked capitals at the top</li><li><b>Product name</b> in Bodoni Moda, two lines at most</li>
      <li><b>Routine step</b> in emerald: cleanse, treat, moisturise or protect</li><li><b>Size · CONCEPT</b> on every pack, so nothing reads as a real product</li><li>A fine champagne border, matched to the cap</li></ol>
      <div class="g3" style="gap:20px;margin-top:40px">{tex}</div>
      <p class="sm" style="margin-top:20px">Texture swatches are illustrated, not photographed, and are shown in the app gallery next to each pack.</p></div></div>""",
          SAGE, "Packaging label"))

# 8 · home & discovery
B.append(("08-home-discovery", 1140, f"""
  <div class="ey">Home &amp; discovery</div><h2>Shop by step, by focus, or just browse</h2>
  {row([('05-home', 'Home', 'Featured serum, shop by step and picks for your focus.'), ('06-shop', 'Shop all', 'Image, name, size, price, wishlist and Add to bag on every card.'),
        ('07-shop-treat', 'Category', 'Underline tabs for the four routine steps.'), ('08-shop-focus', 'Focus &amp; sort', 'Filter to your skin focus; sort by price.')], 320)}""",
          CANVAS, "Home & discovery"))

# 9 · product detail & ingredients
ing = "".join(f'<li><b>{n}</b>: {d}</li>' for n, d in P["butter-balm-cream"]["ingredients"])
B.append(("09-product-ingredients", 1140, f"""
  <div class="ey">Product details &amp; ingredients</div><h2>Everything you need before you buy</h2>
  <div class="g2" style="margin-top:44px;grid-template-columns:1.15fr 1fr;align-items:start">
    <div style="display:flex;gap:28px">{phone('10-product', 320)}{phone('11-product-ingredients', 320)}</div>
    <div><ul style="margin:0 0 0 28px"><li>Gallery with pack, in-scene and texture views</li><li>Size, price and a quantity stepper beside a full-width <b>Add to bag</b></li>
      <li>Accordions for how to use, ingredients and the concept note</li><li>"Pairs well with" to complete the routine</li></ul>
      <div class="card" style="margin-top:32px"><h3>Butter Balm Cream, in plain words</h3><ul style="margin:14px 0 0 28px">{ing}</ul>
        <p class="sm" style="margin-top:14px">Described as what each is commonly used for. No efficacy claims.</p></div></div></div>""",
          CANVAS, "Product & ingredients"))

# 10 · routines & personalisation
B.append(("10-routines-personal", 1140, f"""
  <div class="ey">Skincare routines &amp; personalisation</div><h2>Morning, evening and a gentle journal</h2>
  {row([('04-personalise', 'Skin profile', 'Two optional questions. "Not sure" is allowed.'), ('20-routine-am', 'Morning', 'Tick what you did. Skipping is fine.'),
        ('21-routine-pm', 'Evening', 'Shop this routine adds only what is missing.'), ('22-journal', 'Journal', 'Short private notes, never scored.')], 320)}""",
          SAGE, "Routines & personalisation"))

# 11 · shopping
steps = [("12-added-to-bag", "Added"), ("13-bag", "Bag"), ("15-checkout", "Delivery"), ("17-order", "Confirmed")]
flow = "".join(f'<div style="flex:none;width:300px">{phone(s, 300)}<div class="cap">{l}</div></div>' + ('<div class="arrow">→</div>' if i < len(steps) - 1 else "") for i, (s, l) in enumerate(steps))
B.append(("11-shopping", 1220, f"""
  <div class="ey">Shopping experience</div><h2>From product to demo order in four steps</h2>
  <p class="lede">A confirmation dialog after Add to bag, a bag with quantity controls and a free-delivery threshold of {rs(D['shop']['free_delivery_over'])}, a short delivery form with clear errors, and a confirmation that says plainly: no order is placed and nothing is charged.</p>
  <div style="display:flex;gap:10px;margin-top:44px;justify-content:space-between">{flow}</div>""",
          CANVAS, "Shopping"))

# 12 · states
B.append(("12-states", 1040, f"""
  <div class="ey">Empty, error and saved states</div><h2>Every dead end has a way forward</h2>
  {row([('09-shop-no-results', 'No results', 'Say what happened, offer Clear filters.'), ('14-bag-empty', 'Empty bag', 'One sentence, one action.'),
        ('16-checkout-error', 'Checkout errors', 'A linked summary and messages on each field.'), ('18-wishlist', 'Wishlist', 'Saved products, ready to add.'),
        ('27-home-checkin', 'Check-in', 'A quiet confirmation, no score.')], 252, 24)}""",
          CANVAS, "States"))

# 13 · responsive
B.append(("13-responsive", 1300, f"""
  <div class="ey">Mobile &amp; desktop</div><h2>One shop, phone to desktop</h2>
  <p class="lede">Above 900 px a top navigation and wider grids take over; below it, a bottom tab bar. The same code and data power both.</p>
  <div style="position:relative;height:800px;margin-top:40px">
    <div style="position:absolute;left:0;top:0">{browser('10-product', 1120)}</div>
    <div style="position:absolute;right:0;top:120px">{phone('10-product', 300)}</div></div>""",
          CANVAS, "Responsive"))

# 14 · desktop set
B.append(("14-desktop", 1540, f"""
  <div class="ey">Desktop screens</div><h2>Shop, bag and checkout on a larger screen</h2>
  <div class="g2" style="margin-top:44px;gap:36px">
    <div>{browser('06-shop', 680)}<div class="cap">Shop</div></div><div>{browser('13-bag', 680)}<div class="cap">Bag with order summary</div></div>
    <div>{browser('05-home', 680)}<div class="cap">Home</div></div><div>{browser('15-checkout', 680)}<div class="cap">Demo checkout</div></div></div>""",
          SAGE, "Desktop"))

# 15 · final mockups
B.append(("15-mockups", 1200, f"""
  <div class="ey">Final mockups</div><h2>Porcelain, emerald, unhurried</h2>
  <div style="position:absolute;left:110px;top:340px;transform:rotate(-4deg)">{phone('07-shop-treat', 300)}</div>
  <div style="position:absolute;left:460px;top:300px">{phone('20-routine-am', 310)}</div>
  <div style="position:absolute;left:820px;top:270px;z-index:2">{phone('10-product', 320)}</div>
  <div style="position:absolute;left:1180px;top:320px;transform:rotate(4deg)">{phone('13-bag', 300)}</div>""",
          EMER, "Mockups"))

# 16 · credits
B.append(("16-credits", 900, f"""
  <div class="ey">Tools, contribution &amp; limitations</div><h2>How this was made</h2>
  <div class="g3" style="margin-top:40px">
    <div class="card"><h3>Contribution</h3><p style="margin-top:12px"><b>Purnananda Mishra</b>: concept, art direction, and review at each stage.</p>
      <p style="margin-top:12px"><b>AI-assisted</b>: design production, prototype code, packaging illustration and writing, under that direction.</p></div>
    <div class="card"><h3>Tools</h3><ul style="margin:12px 0 0 28px"><li>HTML, CSS, JavaScript</li><li>Python: tokens, logo and packaging generation</li><li>Playwright + Chromium: screen exports</li><li>Bodoni Moda &amp; Jost (SIL OFL)</li></ul></div>
    <div class="card"><h3>Limitations</h3><ul style="margin:12px 0 0 28px"><li>Fictional brand, products and prices</li><li>Rendered packaging, no product photography</li><li>Demo checkout: nothing is sold</li><li>No user research or usability testing</li><li>No dermatological or regulatory review</li></ul></div></div>""",
          CANVAS, "Credits"))

MOCK = {
    "mockup-01-hero": (1100, f"""<div style="position:absolute;left:104px;top:110px;width:600px"><img src="{UP}design/brand/logo/butterskin-lockup-dark.svg" alt="" style="height:58px">
      <p class="lede">Botanical skincare, beautifully simple.</p><div style="display:flex;align-items:flex-end;margin-top:70px">{packs(['cloud-milk-cleanser','still-water-essence','quiet-night-oil','soft-cloud-moisturiser'], 250)}</div></div>
      <div style="position:absolute;left:780px;top:120px;transform:rotate(-5deg)">{phone('05-home', 300)}</div>
      <div style="position:absolute;left:1100px;top:70px;transform:rotate(4deg)">{phone('06-shop', 320)}</div>""", EMER),
    "mockup-02-responsive": (1080, f"""<div style="position:absolute;left:104px;top:100px">{browser('05-home', 1080)}</div><div style="position:absolute;right:104px;top:220px">{phone('05-home', 280)}</div>""", SAGE),
    "mockup-03-brand-world": (1000, f"""<div class="stage" style="position:absolute;left:104px;top:100px;width:860px;height:720px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:30px">{packs([p['id'] for p in D['products'][:5]], 330)}</div>
      <div style="position:absolute;right:130px;top:110px">{phone('10-product', 320)}</div>""", CANVAS),
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
