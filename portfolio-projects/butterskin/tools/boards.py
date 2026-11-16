"""Builds the Behance boards (behance/slides → exports/behance) and device mockups (design/mockups → exports/mockups) at 2x.
Botanical Luxury direction. Run from the butterskin folder after tools/export_screens.py:  python3 tools/boards.py"""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f"{ROOT}/data/products.json"))
TOK = json.load(open(f"{ROOT}/design/tokens/tokens.json"))
P = {p["id"]: p for p in D["products"]}
ORDER = ["cloud-milk-cleanser", "soft-gel-cleanser", "still-water-essence", "dewdrop-hydration-serum", "quiet-night-oil", "butter-balm-cream", "soft-cloud-moisturiser", "daylight-spf-50"]
CREDIT = "Concept &amp; art direction: Purnananda Mishra"
UP = "../../"
R = f"{UP}design/brand/packaging/renders"
LOGO = f"{UP}design/brand/logo"

CSS = f"""
@import url('{UP}prototype/assets/tokens.css');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1600px;color:var(--bs-charcoal-900);font-family:var(--bs-font-text);-webkit-font-smoothing:antialiased}}
.b{{position:relative;width:1600px;padding:96px 104px 132px;overflow:hidden}}
.ey{{font:500 17px/22px var(--bs-font-text);letter-spacing:.22em;text-transform:uppercase;color:var(--bs-champagne-700)}}
.ey::before{{content:"";display:inline-block;width:40px;height:1px;background:var(--bs-champagne-400);vertical-align:middle;margin-right:16px}}
h1{{font:400 84px/90px var(--bs-font-display);letter-spacing:-.01em;color:var(--bs-emerald-900)}}
h2{{font:400 58px/66px var(--bs-font-display);letter-spacing:-.01em;margin-top:18px;color:var(--bs-emerald-900)}}
h3{{font:400 30px/36px var(--bs-font-display);color:var(--bs-emerald-900)}}
p,li{{font:400 22px/34px var(--bs-font-text);color:var(--bs-charcoal-700)}}
.lede{{font-size:26px;line-height:40px;max-width:1120px;margin-top:20px}}
.sm{{font-size:19px;line-height:29px}}
em{{font-family:var(--bs-font-display);font-style:italic}}
b{{font-weight:600;color:var(--bs-charcoal-900)}}
.card{{background:var(--bs-ivory-0);border:1px solid var(--bs-ivory-200);border-radius:4px;padding:36px}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}.g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}}.g4{{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}}
.ftr{{position:absolute;left:104px;right:104px;bottom:44px;display:flex;justify-content:space-between;font:400 17px/24px var(--bs-font-text);color:var(--bs-charcoal-600);border-top:1px solid var(--bs-ivory-200);padding-top:18px}}
.dark .ftr{{color:var(--bs-champagne-200);border-color:rgba(239,227,200,.25)}}
.dark h1,.dark h2,.dark h3{{color:var(--bs-ivory-50)}}.dark p,.dark li{{color:var(--bs-ivory-100)}}.dark .ey{{color:var(--bs-champagne-400)}}.dark b{{color:var(--bs-ivory-0)}}
.tag{{display:inline-flex;align-items:center;height:44px;padding:0 20px;border-radius:2px;background:var(--bs-ivory-50);color:var(--bs-emerald-900);font:600 16px/1 var(--bs-font-text);letter-spacing:.14em;text-transform:uppercase}}
.tag.line{{background:transparent;color:var(--bs-ivory-50);border:1px solid var(--bs-champagne-400)}}
.phone{{flex:none;border-radius:calc(var(--w) * .14);background:#1F2A24;padding:calc(var(--w) * .028);box-shadow:0 40px 80px rgba(10,55,41,.22);width:var(--w)}}
.phone img{{display:block;width:100%;border-radius:calc(var(--w) * .115)}}
.browser{{border-radius:10px;background:#fff;box-shadow:0 40px 80px rgba(10,55,41,.16);overflow:hidden;border:1px solid var(--bs-ivory-200)}}
.browser .bar{{height:40px;background:var(--bs-ivory-100);display:flex;align-items:center;gap:8px;padding:0 16px}}
.browser .bar i{{width:12px;height:12px;border-radius:50%;background:var(--bs-ivory-200)}}
.browser img{{display:block;width:100%}}
.cap{{font:500 21px/28px var(--bs-font-text);color:var(--bs-charcoal-900);margin-top:20px}}.cap span{{display:block;font-weight:400;color:var(--bs-charcoal-700);font-size:18px;line-height:26px;margin-top:4px}}
.dark .cap{{color:var(--bs-ivory-50)}}.dark .cap span{{color:var(--bs-ivory-100)}}
.dis{{border:1px solid var(--bs-champagne-400);background:var(--bs-champagne-200);border-radius:4px;padding:28px 32px}}
.photo{{display:block;width:100%;border-radius:4px}}
.num{{font:400 20px/1 var(--bs-font-display);color:var(--bs-champagne-700);letter-spacing:.1em}}
.arrow{{align-self:center;font:400 40px var(--bs-font-display);color:var(--bs-champagne-700);margin:0 4px}}
.sw{{border-radius:4px;height:230px;padding:18px 20px;display:flex;flex-direction:column;justify-content:space-between;font:500 18px/24px var(--bs-font-text)}}
.bleed{{position:absolute;inset:0}}.bleed img{{width:100%;height:100%;object-fit:cover}}
"""

CANVAS, SAGE, EMER = "var(--bs-ivory-50)", "var(--bs-sage-100)", "var(--bs-emerald-900)"
rs = lambda n: f"₹{n:,}"


def phone(sid, w, folder="mobile"):
    return f'<div class="phone" style="--w:{w}px"><img src="{UP}exports/screens/{folder}/{sid}.png" alt=""></div>'


def browser(sid, w):
    return f'<div class="browser" style="width:{w}px"><div class="bar"><i></i><i></i><i></i></div><img src="{UP}exports/screens/desktop/{sid}-desktop.png" alt=""></div>'


def page(title, body, h, bg=CANVAS):
    dark = " dark" if bg == EMER else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head>
<body style="background:{bg}"><div class="b{dark}" style="height:{h}px;background:{bg}">{body}
<div class="ftr"><span>ButterSkin · self-initiated concept · fictional brand and products · 3D product renders</span><span>{CREDIT}</span></div></div></body></html>"""


def row(items, w, gap=28):
    return f'<div style="display:flex;gap:{gap}px;margin-top:44px">' + "".join(
        f'<div style="flex:1">{phone(s, w)}<div class="cap">{t}<span>{c}</span></div></div>' for s, t, c in items) + "</div>"


B = []

# 1 · cover: full-bleed botanical hero
B.append(("01-cover", 1200, f"""
  <div class="bleed"><img src="{R}/hero.jpg" alt=""></div>
  <div class="bleed" style="background:linear-gradient(90deg,rgba(10,55,41,.95) 0%,rgba(10,55,41,.82) 34%,rgba(10,55,41,.25) 62%,rgba(10,55,41,0) 80%)"></div>
  <div style="position:relative;max-width:640px">
    <img src="{LOGO}/butterskin-lockup-stacked-reverse.svg" alt="ButterSkin" style="height:150px;margin-left:-40px">
    <h1 style="margin-top:44px">Real care<br><em>for real skin.</em></h1>
    <p class="lede" style="max-width:560px">Brand identity, botanical packaging and a shopping app for a fictional skincare label.</p>
    <div style="display:flex;gap:12px;margin-top:34px"><span class="tag">Self-initiated concept</span><span class="tag line">3D product renders</span></div></div>
  <div style="position:absolute;right:96px;top:150px;transform:rotate(3deg)">{phone('05-home', 330)}</div>""", EMER, "Cover"))

# 2 · overview
B.append(("02-overview", 860, f"""
  <div class="ey">Overview</div><h2>A botanical skincare label you can shop in one calm place</h2>
  <div class="g2" style="margin-top:44px;grid-template-columns:1.2fr 1fr">
    <div><p class="lede" style="margin-top:0">ButterSkin is a concept for a premium botanical skincare brand and its own shopping app: discover eight essentials, read what is inside in plain words, build a morning and evening routine, and check out without friction.</p>
      <p style="margin-top:22px">The project covers a new identity, a packaging family rendered in 3D, design tokens, and a responsive shopping prototype with {len(json.load(open(f"{ROOT}/exports/screens/manifest.json")))} mobile screens and states.</p></div>
    <div class="dis"><h3>Concept disclaimer</h3><p class="sm" style="margin-top:12px">ButterSkin is fictional. Products, formulations, prices and journal entries are illustrative. Product images are photorealistic 3D renders, not photographs. The checkout is a demo: nothing is sold or charged. Nothing here is medical advice, and no user research was carried out.</p>
      <p class="sm" style="margin-top:14px"><b>{CREDIT}</b></p></div></div>""", CANVAS, "Overview"))

# 3 · approach
B.append(("03-approach", 860, f"""
  <div class="ey">Design approach · assumptions</div><h2>Botanical, premium and honest to buy from</h2>
  <div class="g3" style="margin-top:44px">
    <div class="card"><div class="num">01</div><h3 style="margin-top:14px">Botanical luxury</h3><p class="sm" style="margin-top:12px">Deep emerald glass, champagne metal and sunlit stone. The brand should feel like a garden, presented like a fine boutique.</p></div>
    <div class="card"><div class="num">02</div><h3 style="margin-top:14px">Honest information</h3><p class="sm" style="margin-top:12px">Key ingredients in plain words and where each product fits. No ratings, certification badges or results claims.</p></div>
    <div class="card"><div class="num">03</div><h3 style="margin-top:14px">Shopping that works</h3><p class="sm" style="margin-top:12px">Prices always visible, Add to bag on every card, a real bag with quantities, and a three-step demo checkout.</p></div></div>
  <p class="sm" style="margin-top:32px;max-width:1100px">These are design assumptions from general observation of skincare retail, not findings from research or testing.</p>""", CANVAS, "Approach"))

# 4 · brand identity
B.append(("04-brand-identity", 1230, f"""
  <div class="ey">Brand identity</div><h2>A line-drawn lotus over a classic serif</h2>
  <div class="g2" style="margin-top:40px;grid-template-columns:1.25fr 1fr">
    <div class="card" style="display:flex;flex-direction:column;justify-content:space-between;height:640px">
      <img src="{LOGO}/butterskin-lockup-stacked.svg" alt="ButterSkin logo" style="height:250px;align-self:center;margin-top:40px">
      <p class="sm">The emblem is an original line drawing: a tall centre petal, two side petals, two low leaves and a water line. BUTTERSKIN is set in Playfair Display capitals, widely spaced, over BOTANICAL SKINCARE in Inter.</p></div>
    <div style="display:grid;grid-template-rows:1fr 1fr;gap:28px;height:640px">
      <div style="border-radius:4px;background:var(--bs-emerald-800);display:grid;place-items:center"><img src="{LOGO}/butterskin-lockup-stacked-reverse.svg" alt="" style="height:190px"></div>
      <div style="display:flex;gap:28px"><div style="flex:1;border-radius:4px;background:var(--bs-sage-200);display:grid;place-items:center"><img src="{UP}design/brand/app-icon/app-icon-rounded-preview.svg" alt="" style="height:160px"></div>
        <div style="flex:1;border-radius:4px;background:var(--bs-ivory-0);border:1px solid var(--bs-ivory-200);display:flex;align-items:center;justify-content:center;gap:24px">
          <img src="{LOGO}/butterskin-emblem.svg" alt="" style="height:96px"><img src="{LOGO}/butterskin-emblem.svg" alt="" style="height:48px"><img src="{LOGO}/butterskin-emblem.svg" alt="" style="height:24px"></div></div></div></div>
  <div class="card" style="margin-top:28px;display:flex;align-items:center;justify-content:center;height:150px"><img src="{LOGO}/butterskin-lockup-horizontal.svg" alt="" style="height:84px"></div>""", CANVAS, "Brand identity"))

# 5 · colour & type
pal = TOK["color"]["core"]
fg = {"ivory.50": "#1F2A24", "sage.500": "#1F2A24", "champagne.400": "#1F2A24"}
sw = "".join(f'<div class="sw" style="background:{c["value"]};color:{fg.get(c["ref"], "#FFFFFF")};{"border:1px solid #E6DFD2" if c["ref"] == "ivory.50" else ""}"><span>{c["name"]}</span><span><b style="color:inherit">{c["value"]}</b><br>{c["role"]}</span></div>' for c in pal)
npass = sum(c["pass"] for c in TOK["contrast"])
B.append(("05-colour-type", 1120, f"""
  <div class="ey">Colour &amp; typography</div><h2>Deep emerald, sage, ivory and champagne</h2>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:20px;margin-top:40px">{sw}</div>
  <p class="sm" style="margin-top:16px">{npass} of {len(TOK["contrast"])} text and control colour pairs meet WCAG AA. Sage and the bright champagne are kept for surfaces and decoration.</p>
  <div class="g2" style="margin-top:28px">
    <div class="card"><div style="font:400 104px/1 var(--bs-font-display);color:var(--bs-emerald-900)">Aa</div><p class="sm" style="margin-top:10px"><b>Playfair Display</b> · logo, headlines, product names · SIL OFL 1.1</p>
      <p style="font:400 38px/46px var(--bs-font-display);color:var(--bs-charcoal-900);margin-top:14px">Dewdrop Hydration Serum</p></div>
    <div class="card"><div style="font:400 104px/1 var(--bs-font-text);color:var(--bs-charcoal-900)">Aa</div><p class="sm" style="margin-top:10px"><b>Inter</b> · interface, body text and labels · SIL OFL 1.1</p>
      <p style="font:600 19px/24px var(--bs-font-text);letter-spacing:.12em;text-transform:uppercase;color:var(--bs-emerald-800);margin-top:22px">Add to bag · {rs(P['dewdrop-hydration-serum']['price'])}</p></div></div>""", CANVAS, "Colour & type"))

# 6 · packaging family
names = "".join(f'<div><b style="font:400 20px/26px var(--bs-font-display);color:var(--bs-emerald-900)">{P[i]["name"]}</b><p class="sm">{P[i]["size"]}</p></div>' for i in ORDER)
B.append(("06-packaging-family", 1330, f"""
  <div class="ey">Packaging design · fictional</div><h2>Eight essentials, one botanical family</h2>
  <p class="lede">Champagne metal on every cap, collar and pump. Deep emerald glass for the serum, frosted glass for treatments, porcelain white and soft-touch tubes for daily care. Every label carries the lotus, the product name, key ingredients and "concept".</p>
  <img class="photo" src="{R}/range.jpg" alt="" style="margin-top:40px">
  <div style="display:grid;grid-template-columns:repeat(8,1fr);gap:14px;margin-top:22px;text-align:center">{names}</div>""", CANVAS, "Packaging family"))

# 7 · packaging details
labs = "".join(f'<div style="background:{"var(--bs-emerald-800)" if i == "dewdrop-hydration-serum" else "var(--bs-ivory-100)"};border-radius:4px;padding:14px;display:grid;place-items:center;height:250px"><img src="{UP}design/brand/packaging/labels/{i}.png" alt="" style="max-height:220px;max-width:100%"></div>' for i in ORDER)
B.append(("07-packaging-details", 1340, f"""
  <div class="ey">Packaging design · details</div><h2>Glass, liquid, champagne metal and print</h2>
  <div class="g2" style="margin-top:40px;grid-template-columns:1.25fr 1fr;align-items:center">
    <img class="photo" src="{R}/detail.jpg" alt="">
    <ol style="margin-left:30px;display:grid;gap:10px"><li><b>Lotus emblem</b> in champagne or emerald</li><li><b>BUTTERSKIN</b> in spaced Playfair capitals</li><li><b>Product name</b> in Playfair, two lines at most</li>
      <li><b>Key ingredients</b> in Inter, described honestly</li><li><b>Size · CONCEPT</b> on every pack</li><li>Brushed champagne caps, collars and pumps</li></ol></div>
  <div style="display:grid;grid-template-columns:repeat(8,1fr);gap:14px;margin-top:36px">{labs}</div>
  <p class="sm" style="margin-top:14px">Flat label artwork for all eight products, printed onto the 3D packs.</p>""", CANVAS, "Packaging details"))

# 8 · botanical photography
sc = "".join(f'<div><img class="photo" src="{R}/scene-{i}.jpg" alt=""><div class="cap">{P[i]["name"]}<span>In the garden</span></div></div>' for i in ["dewdrop-hydration-serum", "soft-gel-cleanser", "quiet-night-oil"])
tx = "".join(f'<div><img class="photo" src="{R}/texture-{i}.jpg" alt=""><div class="cap">{P[i]["name"]}<span>{P[i]["texture"]}</span></div></div>' for i in ["butter-balm-cream", "quiet-night-oil", "soft-gel-cleanser"])
B.append(("08-photography", 1980, f"""
  <div class="ey">Product photography direction · 3D renders</div><h2>Natural sunlight, leaves and stone</h2>
  <p class="lede">Warm side light, travertine, moss and small white flowers for brand moments; quiet ivory packshots for the shop; texture swatches for every formula. All rendered in 3D, because the products are fictional.</p>
  <img class="photo" src="{R}/hero.jpg" alt="" style="margin-top:40px">
  <div class="g3" style="margin-top:28px;grid-template-columns:repeat(6,1fr);gap:20px">{sc}{tx}</div>""", CANVAS, "Photography"))

# 9 · home & discovery
B.append(("09-home-discovery", 1150, f"""
  <div class="ey">Home &amp; discovery</div><h2>Shop by step, by focus, or just browse</h2>
  {row([('05-home', 'Home', 'Sunlit hero, brand facts and shop by step.'), ('06-shop', 'Shop all', 'Photo, ingredients, price, wishlist and Add to bag on every card.'),
        ('07-shop-treat', 'Category', 'Underline tabs for the four routine steps.'), ('08-shop-focus', 'Focus &amp; sort', 'Filter to your skin focus; sort by price.')], 320)}""", SAGE, "Home & discovery"))

# 10 · product detail & ingredients
bb = P["butter-balm-cream"]
ing = "".join(f'<li><b>{n}</b>: {d}</li>' for n, d in bb["ingredients"])
tri = "".join(f'<img src="{UP}prototype/assets/products/butter-balm-cream{v}.jpg" alt="" style="width:100%;border-radius:4px">' for v in ("", "-scene", "-texture"))
B.append(("10-product-ingredients", 1240, f"""
  <div class="ey">Product details &amp; ingredients</div><h2>Everything you need before you buy</h2>
  <div class="g2" style="margin-top:44px;grid-template-columns:1.1fr 1fr;align-items:start">
    <div style="display:flex;gap:28px">{phone('10-product', 320)}{phone('11-product-ingredients', 320)}</div>
    <div><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">{tri}</div>
      <p class="sm" style="margin-top:12px">Every product page switches between the packshot, a garden scene and a texture swatch.</p>
      <div class="card" style="margin-top:28px"><h3>{bb["name"]}, in plain words</h3><ul style="margin:14px 0 0 28px">{ing}</ul>
        <p class="sm" style="margin-top:14px">What each ingredient is commonly used for. No efficacy claims.</p></div></div></div>""", CANVAS, "Product & ingredients"))

# 11 · routines & personalisation
B.append(("11-routines-personal", 1150, f"""
  <div class="ey">Skincare routines &amp; personalisation</div><h2>Morning, evening and a gentle journal</h2>
  {row([('04-personalise', 'Skin profile', 'Two optional questions. "Not sure" is allowed.'), ('20-routine-am', 'Morning', 'Tick what you did. Skipping is fine.'),
        ('21-routine-pm', 'Evening', 'Shop this routine adds only what is missing.'), ('22-journal', 'Journal', 'Short private notes, never scored.')], 320)}""", SAGE, "Routines & personalisation"))

# 12 · shopping
steps = [("12-added-to-bag", "Added to bag"), ("13-bag", "Bag"), ("15-checkout", "Delivery"), ("17-order", "Confirmed")]
flow = "".join(f'<div style="flex:none;width:300px">{phone(s, 300)}<div class="cap">{l}</div></div>' + ('<div class="arrow">→</div>' if i < len(steps) - 1 else "") for i, (s, l) in enumerate(steps))
B.append(("12-shopping", 1230, f"""
  <div class="ey">Shopping experience</div><h2>From product to demo order in four steps</h2>
  <p class="lede">A confirmation dialog after Add to bag, a bag with quantity controls and free delivery over {rs(D['shop']['free_delivery_over'])}, a short delivery form with clear errors, and a confirmation that says plainly: no order is placed and nothing is charged.</p>
  <div style="display:flex;gap:10px;margin-top:44px;justify-content:space-between">{flow}</div>""", CANVAS, "Shopping"))

# 13 · states
B.append(("13-states", 1050, f"""
  <div class="ey">Empty, error and saved states</div><h2>Every dead end has a way forward</h2>
  {row([('09-shop-no-results', 'No results', 'Say what happened, offer Clear filters.'), ('14-bag-empty', 'Empty bag', 'One sentence, one action.'),
        ('16-checkout-error', 'Delivery errors', 'A linked summary and messages on each field.'), ('18-wishlist', 'Wishlist', 'Saved products, ready to add.'),
        ('27-home-checkin', 'Check-in', 'A quiet confirmation, no score.')], 252, 24)}""", CANVAS, "States"))

# 14 · responsive
B.append(("14-responsive", 1300, f"""
  <div class="ey">Mobile &amp; desktop</div><h2>One shop, phone to desktop</h2>
  <p class="lede">Above 900 px a top navigation and wider grids take over; below it, a bottom tab bar. The same code and data power both.</p>
  <div style="position:relative;height:800px;margin-top:40px">
    <div style="position:absolute;left:0;top:0">{browser('05-home', 1120)}</div>
    <div style="position:absolute;right:0;top:110px">{phone('05-home', 300)}</div></div>""", SAGE, "Responsive"))

# 15 · desktop
B.append(("15-desktop", 1540, f"""
  <div class="ey">Desktop screens</div><h2>Shop, product, bag and delivery on a larger screen</h2>
  <div class="g2" style="margin-top:44px;gap:36px">
    <div>{browser('06-shop', 680)}<div class="cap">Shop</div></div><div>{browser('10-product', 680)}<div class="cap">Product details</div></div>
    <div>{browser('13-bag', 680)}<div class="cap">Bag with order summary</div></div><div>{browser('15-checkout', 680)}<div class="cap">Demo checkout</div></div></div>""", CANVAS, "Desktop"))

# 16 · final mockups
B.append(("16-mockups", 1200, f"""
  <div class="bleed"><img src="{R}/range.jpg" alt="" style="filter:blur(2px) brightness(.55)"></div><div class="bleed" style="background:rgba(10,55,41,.55)"></div>
  <div style="position:relative"><div class="ey">Final mockups</div><h2>Emerald, ivory, unhurried</h2></div>
  <div style="position:absolute;left:110px;top:340px;transform:rotate(-4deg)">{phone('07-shop-treat', 300)}</div>
  <div style="position:absolute;left:460px;top:300px">{phone('20-routine-am', 310)}</div>
  <div style="position:absolute;left:820px;top:270px;z-index:2">{phone('10-product', 320)}</div>
  <div style="position:absolute;left:1180px;top:320px;transform:rotate(4deg)">{phone('13-bag', 300)}</div>""", EMER, "Mockups"))

# 17 · credits
B.append(("17-credits", 920, f"""
  <div class="ey">Tools, contribution &amp; limitations</div><h2>How this was made</h2>
  <div class="g3" style="margin-top:40px">
    <div class="card"><h3>Contribution</h3><p style="margin-top:12px"><b>Purnananda Mishra</b>: concept, art direction, choice of direction and review at each stage.</p></div>
    <div class="card"><h3>Tools</h3><ul style="margin:12px 0 0 28px"><li>HTML, CSS, JavaScript</li><li>Python: tokens and logo generation</li><li>Blender Cycles: 3D product renders</li><li>Playwright: screen exports</li><li>Playfair Display &amp; Inter (SIL OFL)</li></ul></div>
    <div class="card"><h3>Limitations</h3><ul style="margin:12px 0 0 28px"><li>Fictional brand, products and prices</li><li>3D renders, not photography</li><li>Demo checkout: nothing is sold</li><li>No user research or usability testing</li><li>No dermatological or regulatory review</li></ul></div></div>""", CANVAS, "Credits"))

MOCK = {
    "mockup-01-hero": (1100, f"""<div class="bleed"><img src="{R}/hero.jpg" alt=""></div>
      <div class="bleed" style="background:linear-gradient(90deg,rgba(10,55,41,.9),rgba(10,55,41,.2) 55%,rgba(10,55,41,0))"></div>
      <div style="position:absolute;left:104px;top:300px"><img src="{LOGO}/butterskin-lockup-stacked-reverse.svg" alt="" style="height:170px"></div>
      <div style="position:absolute;left:880px;top:110px;transform:rotate(-4deg)">{phone('05-home', 290)}</div>
      <div style="position:absolute;left:1190px;top:70px;transform:rotate(3deg)">{phone('10-product', 300)}</div>""", EMER),
    "mockup-02-responsive": (1080, f"""<div style="position:absolute;left:104px;top:100px">{browser('05-home', 1080)}</div><div style="position:absolute;right:104px;top:220px">{phone('05-home', 280)}</div>""", SAGE),
    "mockup-03-brand-world": (1000, f"""<img src="{R}/range.jpg" alt="" style="position:absolute;left:104px;top:100px;width:960px;border-radius:4px">
      <div style="position:absolute;right:120px;top:90px">{phone('06-shop', 320)}</div>""", CANVAS),
}


if __name__ == "__main__":
    SD, EB, MD, EM = f"{ROOT}/behance/slides", f"{ROOT}/exports/behance", f"{ROOT}/design/mockups", f"{ROOT}/exports/mockups"
    for d in (SD, EB, MD, EM):
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            os.remove(f"{d}/{f}")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=2)
        for name, h, body, bg, title in B:
            f = f"{SD}/{name}.html"; open(f, "w").write(page(f"ButterSkin · {title}", body, h, bg))
            pg.goto("file://" + f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400); pg.screenshot(path=f"{EB}/{name}.png", full_page=True)
        for name, (h, body, bg) in MOCK.items():
            f = f"{MD}/{name}.html"; open(f, "w").write(page(f"ButterSkin · {name}", body, h, bg))
            pg.goto("file://" + f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400); pg.screenshot(path=f"{EM}/{name}.png", full_page=True)
        b.close()
    print("boards:", len(B), "mockups:", len(MOCK))
